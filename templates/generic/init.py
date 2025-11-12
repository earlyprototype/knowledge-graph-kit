#!/usr/bin/env python3
"""
Initialize generic knowledge graph
Creates directory structure and empty entities.json
"""

import sys
from pathlib import Path

# Add parent directory to path to import core
sys.path.insert(0, str(Path(__file__).parent.parent.parent))

from core.graph_manager import GraphManager


def init_generic_graph():
    """Initialize generic knowledge graph"""
    print("Initializing Generic Knowledge Graph")
    print("=" * 50)
    
    # Load config and create graph manager
    gm = GraphManager('config.yaml')
    
    # Create directory structure
    paths = gm.config.get_paths()
    for key, path in paths.items():
        if key.endswith('_dir'):
            path_obj = Path(path)
            path_obj.mkdir(parents=True, exist_ok=True)
            print(f"✓ Created: {path_obj}")
    
    # Save initial entities.json
    gm.save()
    print(f"✓ Created: {gm.entities_path}")
    
    # Print configuration summary
    stats = gm.graph_data['metadata']
    print(f"\n{'=' * 50}")
    print(f"Graph initialized!")
    print(f"Domain: {stats['domain']}")
    print(f"Version: {stats['version']}")
    print(f"\nEntity types (edit config.yaml to customize):")
    for category, config in gm.config.get_entity_types().items():
        label = gm.config.get_entity_label(category, plural=True)
        name = gm.config.get_entity_name(category)
        print(f"  - {label} ({name})")
    
    print(f"\nRelationship types:")
    for rel_type in gm.config.get_relationship_types()[:5]:
        print(f"  - {rel_type}")
    if len(gm.config.get_relationship_types()) > 5:
        print(f"  ... and {len(gm.config.get_relationship_types()) - 5} more")
    
    print(f"\n{'=' * 50}")
    print(f"NEXT: Customize config.yaml for your domain")
    print(f"{'=' * 50}")
    print(f"Edit config.yaml to:")
    print(f"  1. Change entity type names")
    print(f"  2. Define entity subtypes")
    print(f"  3. Add domain-specific relationships")
    print(f"  4. Set visualization colors")
    print(f"\nThen:")
    print(f"  - Add entities using graph_manager.py")
    print(f"  - Start viewer: python server.py")
    print(f"{'=' * 50}\n")


if __name__ == "__main__":
    init_generic_graph()

