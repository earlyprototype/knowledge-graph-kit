#!/usr/bin/env python3
"""
Build a "practice map" of earlyprototype's public GitHub practice using the
Ecosystem Mapping template. Mirrors the structure of
examples/systems-map-example/build_map.py (the kit's own documented
worked example).

Hubs are modelled as ecosystem 'process' elements (practice areas / ways of
working). Projects are modelled as ecosystem 'technology' elements (public
repos/tools). Both types are chosen because they are valid entries in this
template's config.yaml entity_types.primary.types AND because they are the
only two ecosystem-relevant types that also have a real color mapping in
viewer.html's hardcoded COLORS constant (see report to caller for details
on the config.yaml <-> viewer.html color mismatch found in this template).
"""

import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))

from core.graph_manager import GraphManager


def build_practice_map():
    gm = GraphManager(config_path='config.yaml')

    print("Building earlyprototype practice map (Ecosystem template)...")

    # ========================================
    # THEME HUBS  (type: process)
    # ========================================
    print("  Adding theme hubs...")

    gm.add_entity('primary', {
        'id': 'service-design',
        'label': 'Service design',
        'type': 'process',
        'description': 'Practice area: designing tools, workflows and interfaces that make complex work usable for people.'
    })

    gm.add_entity('primary', {
        'id': 'ai-systems',
        'label': 'AI systems',
        'type': 'process',
        'description': 'Practice area: agentic tools, MCP servers and AI-integrated workflows.'
    })

    gm.add_entity('primary', {
        'id': 'research-play',
        'label': 'Research & play',
        'type': 'process',
        'description': 'Practice area: open-ended experiments probing how models and ideas behave off the well-trodden path.'
    })

    # ========================================
    # PROJECT NODES  (type: technology)
    # ========================================
    print("  Adding project nodes...")

    gm.add_entity('primary', {
        'id': 'knowledge-graph-kit',
        'label': 'knowledge-graph-kit',
        'type': 'technology',
        'description': "Configurable LLM-integrated knowledge graph toolkit with templates for Research, Systems Map and Ecosystem Mapping — the tool that generated this map.",
        'url': 'https://github.com/earlyprototype/knowledge-graph-kit'
    })

    gm.add_entity('primary', {
        'id': 'fablattice-gpt',
        'label': 'FabLatticeGPT',
        'type': 'technology',
        'description': 'OpenAI-Accelerator-inspired custom GPT that structures FabLab users’ prototyping plans before they touch the machines.',
        'url': 'https://github.com/earlyprototype/FabLatticeGPT'
    })

    gm.add_entity('primary', {
        'id': 'false-flag',
        'label': 'FALSE FLAG',
        'type': 'technology',
        'description': 'LLM-driven political-military crisis simulation with AI cabinet advisors and free-form, adjudicated decision-making.',
        'url': 'https://github.com/earlyprototype/false-flag'
    })

    gm.add_entity('primary', {
        'id': 'kanbanger',
        'label': 'kanbanger',
        'type': 'technology',
        'description': 'MCP-driven kanban for mixed human/agent work, with a server-enforced human-approval gate before any task is marked done.',
        'url': 'https://github.com/earlyprototype/kanbanger'
    })

    gm.add_entity('primary', {
        'id': 'thought-bubble',
        'label': 'thought_bubble',
        'type': 'technology',
        'description': 'Turns dense documents into a visual webpage with logical flow.',
        'url': 'https://github.com/earlyprototype/thought_bubble'
    })

    gm.add_entity('primary', {
        'id': 'notebooklm-mcps',
        'label': 'NotebookLM MCPs',
        'type': 'technology',
        'description': 'MCP servers putting Google NotebookLM into agent workflows, including a workflow-tuned "diet" companion server.',
        'url': 'https://github.com/earlyprototype/notebooklm-py-MCP'
    })

    gm.add_entity('primary', {
        'id': 'hunch-kit',
        'label': 'hunch_kit',
        'type': 'technology',
        'description': 'Structured experimentation framework with human-in-the-loop evaluation and provider-agnostic execution for testing hunches.',
        'url': 'https://github.com/earlyprototype/hunch_kit'
    })

    gm.add_entity('primary', {
        'id': 'plugin-marketplace',
        'label': 'plugin marketplace',
        'type': 'technology',
        'description': "Claude Code plugin marketplace (repo: early-prototype) — install with '/plugin marketplace add'.",
        'url': 'https://github.com/earlyprototype/early-prototype'
    })

    gm.add_entity('primary', {
        'id': 'lia-workflow-specs',
        'label': 'lia-workflow-specs',
        'type': 'technology',
        'description': 'Spec-driven framework for deliberate, understanding-first AI development — a counterweight to vibe coding.',
        'url': 'https://github.com/earlyprototype/lia-workflow-specs'
    })

    gm.add_entity('primary', {
        'id': 'metube',
        'label': 'meTube',
        'type': 'technology',
        'description': 'YouTube content extractor: dual-layer transcripts, auto-extracted entities and interactive HTML reports.',
        'url': 'https://github.com/earlyprototype/meTube'
    })

    gm.add_entity('primary', {
        'id': 'plasticflowers',
        'label': 'plasticFlowers',
        'type': 'technology',
        'description': 'Local-first live mindmap that captures speech and builds an emergent knowledge graph in real time via Gemini.',
        'url': 'https://github.com/earlyprototype/plasticFlowers'
    })

    gm.add_entity('primary', {
        'id': 'activation-tensor-resonance',
        'label': 'Activation Tensor Resonance',
        'type': 'technology',
        'description': "Inspired by Alvin Lucier’s 'I Am Sitting in a Room': GPT-2's activation tensor is excited through iterative feedback until attractor states emerge.",
        'url': 'https://github.com/earlyprototype/lucier-gpt2-activ-tensor-reson-experiments'
    })

    # ========================================
    # RELATIONSHIPS - project to hub (enables)
    # ========================================
    print("  Adding hub relationships...")

    hub_edges = [
        ('knowledge-graph-kit', ['service-design']),
        ('fablattice-gpt', ['service-design', 'ai-systems']),
        ('kanbanger', ['ai-systems', 'service-design']),
        ('thought-bubble', ['ai-systems', 'service-design']),
        ('notebooklm-mcps', ['ai-systems']),
        ('hunch-kit', ['research-play', 'ai-systems']),
        ('plugin-marketplace', ['ai-systems']),
        ('lia-workflow-specs', ['ai-systems']),
        ('metube', ['ai-systems']),
        ('plasticflowers', ['ai-systems', 'research-play']),
        ('false-flag', ['research-play']),
        ('activation-tensor-resonance', ['research-play']),
    ]

    for project_id, hubs in hub_edges:
        for hub_id in hubs:
            gm.add_relationship(project_id, hub_id, 'enables',
                               description='Practices and builds out this area.')

    # ========================================
    # RELATIONSHIPS - cross-links (typed)
    # ========================================
    print("  Adding cross-links...")

    gm.add_relationship('thought-bubble', 'activation-tensor-resonance', 'influences',
                       description="Visualises ATR's activation-tensor experiments as an interactive mind-map.")

    gm.add_relationship('kanbanger', 'plugin-marketplace', 'regulates',
                       description='Governs how plugin-marketplace tasks move through review before being marked done.')

    # ========================================
    # SAVE
    # ========================================
    print("  Saving graph...")
    gm.save()

    total_entities = len(gm.graph_data.get('elements', []))
    total_relationships = len(gm.graph_data.get('relationships', []))

    print("\n[SUCCESS] Practice map created.")
    print("   - Elements:", total_entities)
    print("   - Relationships:", total_relationships)
    print("\nTo view: python server.py --no-browser  then open http://localhost:8000/viewer.html")


if __name__ == '__main__':
    build_practice_map()
