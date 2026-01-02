"""
Knowledge graph management
Handles CRUD operations on entities and relationships
"""

import json
from pathlib import Path
from datetime import datetime
from typing import Dict, List, Any, Optional
from core.config_loader import GraphConfig


class GraphManager:
    """Manages knowledge graph entities and relationships"""
    
    def __init__(self, config_path: str = "config.yaml"):
        self.config = GraphConfig(config_path)
        self.entities_path = self.config.get_entities_file_path()
        self.graph_data = self._load_or_init()
    
    def _load_or_init(self) -> Dict[str, Any]:
        """Load existing graph or initialize new one"""
        if self.entities_path.exists():
            return self._load_graph()
        else:
            return self._init_graph()
    
    def _load_graph(self) -> Dict[str, Any]:
        """Load graph from JSON file"""
        with open(self.entities_path, 'r', encoding='utf-8') as f:
            return json.load(f)
    
    def _init_graph(self) -> Dict[str, Any]:
        """Initialize new graph structure"""
        graph = {
            'metadata': {
                'domain': self.config.domain,
                'version': self.config.version,
                'created': datetime.now().strftime('%Y-%m-%d'),
                'last_updated': datetime.now().strftime('%Y-%m-%d')
            },
            'relationships': []
        }
        
        # Add entity collections based on config
        for category, config in self.config.get_entity_types().items():
            entity_name = config['name']
            graph[entity_name] = []
        
        return graph
    
    def save(self):
        """Save graph to JSON file"""
        # Ensure directory exists
        self.entities_path.parent.mkdir(parents=True, exist_ok=True)
        
        # Update last_updated timestamp
        self.graph_data['metadata']['last_updated'] = datetime.now().strftime('%Y-%m-%d')
        
        # Save with formatting
        with open(self.entities_path, 'w', encoding='utf-8') as f:
            json.dump(self.graph_data, f, indent=2, ensure_ascii=False)
    
    def add_entity(self, category: str, entity: Dict[str, Any]) -> bool:
        """
        Add entity to graph
        
        Args:
            category: Entity category (primary, contributors, sources)
            entity: Entity data dictionary with 'id' field
        
        Returns:
            True if added, False if already exists
        """
        entity_name = self.config.get_entity_name(category)
        
        if entity_name not in self.graph_data:
            raise ValueError(f"Unknown entity collection: {entity_name}")
        
        # Check for duplicate ID
        existing_ids = {e['id'] for e in self.graph_data[entity_name]}
        if entity['id'] in existing_ids:
            return False
        
        self.graph_data[entity_name].append(entity)
        return True
    
    def update_entity(self, category: str, entity_id: str, updates: Dict[str, Any]) -> bool:
        """Update existing entity"""
        entity_name = self.config.get_entity_name(category)
        
        for entity in self.graph_data[entity_name]:
            if entity['id'] == entity_id:
                entity.update(updates)
                return True
        
        return False
    
    def get_entity(self, category: str, entity_id: str) -> Optional[Dict]:
        """Get entity by ID"""
        entity_name = self.config.get_entity_name(category)
        
        for entity in self.graph_data[entity_name]:
            if entity['id'] == entity_id:
                return entity
        
        return None
    
    def add_relationship(self, from_id: str, to_id: str, rel_type: str, 
                        description: str = "", strength: str = "moderate") -> bool:
        """Add relationship between entities"""
        # Check if relationship already exists
        for rel in self.graph_data['relationships']:
            if (rel['from'] == from_id and 
                rel['to'] == to_id and 
                rel['type'] == rel_type):
                return False
        
        relationship = {
            'from': from_id,
            'to': to_id,
            'type': rel_type,
            'description': description,
            'strength': strength
        }
        
        self.graph_data['relationships'].append(relationship)
        return True
    
    def merge_from_file(self, file_path: str):
        """Merge entities from another JSON file"""
        merge_path = self.config.resolve_path(file_path)
        with open(merge_path, 'r', encoding='utf-8') as f:
            new_data = json.load(f)
        
        self.merge(new_data)
    
    def merge(self, new_data: Dict[str, Any]):
        """
        Merge new graph data into existing graph
        Handles duplicates intelligently
        """
        stats = {'added': {}, 'merged': {}}
        
        # Merge each entity collection
        for category, config in self.config.get_entity_types().items():
            entity_name = config['name']
            
            if entity_name not in new_data:
                continue
            
            stats['added'][entity_name] = 0
            stats['merged'][entity_name] = 0
            
            # Create lookup dict for existing entities
            existing = {e['id']: e for e in self.graph_data[entity_name]}
            
            for new_entity in new_data[entity_name]:
                entity_id = new_entity['id']
                
                if entity_id in existing:
                    # Merge source_papers or similar provenance fields
                    self._merge_entity(existing[entity_id], new_entity)
                    stats['merged'][entity_name] += 1
                else:
                    # Add new entity
                    self.graph_data[entity_name].append(new_entity)
                    stats['added'][entity_name] += 1
        
        # Merge relationships
        stats['added']['relationships'] = 0
        existing_rels = {(r['from'], r['to'], r['type']) for r in self.graph_data['relationships']}
        
        for new_rel in new_data.get('relationships', []):
            key = (new_rel['from'], new_rel['to'], new_rel['type'])
            if key not in existing_rels:
                self.graph_data['relationships'].append(new_rel)
                existing_rels.add(key)
                stats['added']['relationships'] += 1
        
        return stats
    
    def _merge_entity(self, existing: Dict, new: Dict):
        """Merge provenance fields from new entity into existing"""
        # Merge source_papers or similar provenance arrays
        provenance_fields = ['source_papers', 'mentioned_in', 'key_papers']
        
        for field in provenance_fields:
            if field in new:
                if field not in existing:
                    existing[field] = []
                
                for item in new[field]:
                    if item not in existing[field]:
                        existing[field].append(item)
    
    def get_stats(self) -> Dict[str, int]:
        """Get graph statistics"""
        stats = {}
        
        for category, config in self.config.get_entity_types().items():
            entity_name = config['name']
            stats[entity_name] = len(self.graph_data.get(entity_name, []))
        
        stats['relationships'] = len(self.graph_data.get('relationships', []))
        
        return stats
    
    def validate(self) -> List[str]:
        """Validate graph integrity"""
        issues = []
        
        # Collect all entity IDs
        all_ids = set()
        for category, config in self.config.get_entity_types().items():
            entity_name = config['name']
            for entity in self.graph_data.get(entity_name, []):
                all_ids.add(entity['id'])
        
        # Check relationships reference valid entities
        for rel in self.graph_data.get('relationships', []):
            if rel['from'] not in all_ids:
                issues.append(f"Relationship references unknown 'from' ID: {rel['from']}")
            if rel['to'] not in all_ids:
                issues.append(f"Relationship references unknown 'to' ID: {rel['to']}")
        
        return issues
