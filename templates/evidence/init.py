#!/usr/bin/env python3
"""
Initialize evidence graph
Creates directory structure and empty entities.json
"""

import sys
from pathlib import Path

# Ensure stdout can print UTF-8 symbols (checkmarks) - Windows consoles
# default to a codepage (e.g. cp1252) that can't encode them.
try:
    sys.stdout.reconfigure(encoding='utf-8', errors='replace')
except (AttributeError, ValueError):
    pass

# Add the knowledge-graph-kit root (the directory containing core/) to path.
# Walks upward so this works both in-place (templates/evidence/init.py) and
# after copying to a project directory per the README's Manual Setup.
kit_root = Path(__file__).resolve().parent
while not (kit_root / 'core').is_dir():
    if kit_root.parent == kit_root:
        raise RuntimeError("Could not locate the knowledge-graph-kit 'core' package")
    kit_root = kit_root.parent
sys.path.insert(0, str(kit_root))

from core.graph_manager import GraphManager


def init_evidence_graph():
    """Initialize evidence graph"""
    print("Initializing Evidence Graph")
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

    # Save initial entities.json (also writes _data/visual_config.json)
    gm.save()
    print(f"✓ Created: {gm.entities_path}")
    print(f"✓ Created: {gm.config.get_visual_config_file_path()}")

    # Print stats
    stats = gm.graph_data['metadata']
    print(f"\n{'=' * 50}")
    print(f"Graph initialized!")
    print(f"Domain: {stats['domain']}")
    print(f"Version: {stats['version']}")
    print(f"\nEntity types:")
    for category, config in gm.config.get_entity_types().items():
        label = gm.config.get_entity_label(category, plural=True)
        print(f"  - {label}")

    print(f"\nClaim statuses: supported, refuted, qualified, retired, corrected, open, untested")
    print(f"Epistemic edges: supports, refutes, qualifies, corrects, retires, supersedes, tests")

    print(f"\nNext steps:")
    print(f"  1. Add claims, runs and sources using GraphManager")
    print(f"  2. Or merge from an existing entities.json")
    print(f"  3. Add metadata['phases'] so the timeline scrubber has phases")
    print(f"  4. Start viewer: python server.py")
    print(f"{'=' * 50}\n")


if __name__ == "__main__":
    init_evidence_graph()
