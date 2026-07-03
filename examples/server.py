#!/usr/bin/env python3
"""
Start HTTP server for viewing research knowledge graph
"""

import sys
from pathlib import Path

# Add the knowledge-graph-kit root (the directory containing core/) to path.
# Walks upward so this works regardless of how deep this file is nested.
kit_root = Path(__file__).resolve().parent
while not (kit_root / 'core').is_dir():
    if kit_root.parent == kit_root:
        raise RuntimeError("Could not locate the knowledge-graph-kit 'core' package")
    kit_root = kit_root.parent
sys.path.insert(0, str(kit_root))

from core.server import start_server

if __name__ == "__main__":
    start_server()

