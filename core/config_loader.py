"""
Configuration loader for knowledge graph templates
Loads and validates YAML config files
"""

import yaml
from pathlib import Path
from typing import Dict, Any, List


class GraphConfig:
    """Loads and provides access to graph configuration"""
    
    def __init__(self, config_path: str = "config.yaml"):
        self.config_path = Path(config_path).resolve()
        self.config = self._load_config()
        self._validate()
    
    def _load_config(self) -> Dict[str, Any]:
        """Load YAML configuration file"""
        if not self.config_path.exists():
            raise FileNotFoundError(f"Config file not found: {self.config_path}")
        
        with open(self.config_path, 'r', encoding='utf-8') as f:
            return yaml.safe_load(f)
    
    def _validate(self):
        """Validate required configuration fields"""
        required = ['domain', 'entity_types', 'paths']
        for field in required:
            if field not in self.config:
                raise ValueError(f"Missing required config field: {field}")
    
    @property
    def domain(self) -> str:
        return self.config['domain']
    
    @property
    def version(self) -> str:
        return self.config.get('version', '1.0')
    
    def get_entity_types(self) -> Dict[str, Dict]:
        """Get all entity type definitions"""
        return self.config['entity_types']
    
    def get_entity_type_config(self, category: str) -> Dict:
        """Get config for specific entity category (primary, contributors, sources)"""
        return self.config['entity_types'].get(category, {})
    
    def get_entity_name(self, category: str) -> str:
        """Get the name of an entity category"""
        return self.get_entity_type_config(category).get('name', category)
    
    def get_entity_label(self, category: str, plural: bool = False) -> str:
        """Get display label for entity category"""
        config = self.get_entity_type_config(category)
        if plural:
            return config.get('label_plural', config.get('name', category))
        return config.get('label_singular', config.get('name', category))
    
    def get_relationship_types(self) -> List[str]:
        """Get all defined relationship types"""
        return self.config.get('relationships', {}).get('types', [])
    
    def get_relationship_config(self, rel_type: str) -> Dict:
        """Get configuration for a specific relationship type"""
        custom = self.config.get('custom_variables', {}).get('relationship_types', [])
        for rel in custom:
            if rel['name'] == rel_type:
                return rel
        return {}
    
    def get_paths(self) -> Dict[str, str]:
        """Get all path configurations"""
        return self.config.get('paths', {})
    
    def get_path(self, key: str) -> str:
        """Get specific path as a string"""
        return self.config['paths'].get(key, '')

    def resolve_path(self, path_str: str) -> Path:
        """Resolve a path relative to the config file's directory"""
        return self.config_path.parent / Path(path_str)
    
    def get_entities_file_path(self) -> Path:
        """Get full path to entities.json"""
        data_dir = self.get_path('data_dir')
        entities_file = self.get_path('entities_file')
        return self.resolve_path(data_dir) / entities_file
    
    def get_gemini_config(self) -> Dict:
        """Get Gemini AI configuration"""
        return self.config.get('gemini_context', {})
    
    def get_visual_config(self) -> Dict:
        """Get visualization configuration"""
        return self.config.get('visualization', {})
    
    def get_color_for_type(self, entity_type: str) -> str:
        """Get color for entity type"""
        colors = self.config.get('visualization', {}).get('colors', {})
        return colors.get(entity_type, '#7f8c8d')


def load_config(config_path: str = "config.yaml") -> GraphConfig:
    """Convenience function to load configuration"""
    return GraphConfig(config_path)
