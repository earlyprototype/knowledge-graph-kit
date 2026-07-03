#!/usr/bin/env python3
"""
Start HTTP server for viewing research knowledge graph
"""

import sys
from pathlib import Path

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent.parent.parent))

from core.server import start_server

if __name__ == "__main__":
    start_server()

