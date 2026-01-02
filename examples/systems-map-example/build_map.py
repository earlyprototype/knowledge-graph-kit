#!/usr/bin/env python3
"""
Build a systems map of the Knowledge Graph Kit codebase itself.
This is a meta-example showing how to use the Systems Mapping template
to document a software project.
"""

import sys
import os

# Add parent directory to path to import core modules
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))

from core.graph_manager import GraphManager

def build_knowledge_graph_kit_map():
    """Build a systems map of the Knowledge Graph Kit project."""
    
    gm = GraphManager(config_path='config.yaml')
    
    print("Building Knowledge Graph Kit systems map...")
    
    # ========================================
    # CORE COMPONENTS
    # ========================================
    
    print("  Adding core components...")
    
    gm.add_entity('primary', {
        'id': 'graph-manager',
        'label': 'Graph Manager',
        'type': 'module',
        'description': 'Core module for managing knowledge graph entities and relationships',
        'version': '1.0',
        'status': 'active',
        'tech_stack': ['Python'],
        'source_documents': ['readme', 'core-architecture']
    })
    
    gm.add_entity('primary', {
        'id': 'config-loader',
        'label': 'Config Loader',
        'type': 'module',
        'description': 'YAML configuration file parser and validator',
        'version': '1.0',
        'status': 'active',
        'tech_stack': ['Python', 'PyYAML'],
        'source_documents': ['readme']
    })
    
    gm.add_entity('primary', {
        'id': 'http-server',
        'label': 'HTTP Server',
        'type': 'service',
        'description': 'Lightweight HTTP server for serving the visualization interface',
        'version': '1.0',
        'status': 'active',
        'tech_stack': ['Python', 'http.server'],
        'source_documents': ['readme']
    })
    
    gm.add_entity('primary', {
        'id': 'gemini-api-server',
        'label': 'Gemini API Server',
        'type': 'service',
        'description': 'Optional AI chat server integrating Google Gemini API',
        'version': '1.0',
        'status': 'active',
        'tech_stack': ['Python', 'Google Generative AI'],
        'source_documents': ['readme']
    })
    
    # ========================================
    # SETUP & INITIALIZATION
    # ========================================
    
    print("  Adding setup components...")
    
    gm.add_entity('primary', {
        'id': 'setup-wizard',
        'label': 'Setup Wizard',
        'type': 'tool',
        'description': 'Interactive command-line wizard for project initialization',
        'version': '1.0',
        'status': 'active',
        'tech_stack': ['Python'],
        'source_documents': ['readme']
    })
    
    gm.add_entity('primary', {
        'id': 'init-script',
        'label': 'Initialization Script',
        'type': 'tool',
        'description': 'Template-specific initialization script for creating data directories',
        'version': '1.0',
        'status': 'active',
        'tech_stack': ['Python'],
        'source_documents': []
    })
    
    # ========================================
    # TEMPLATES
    # ========================================
    
    print("  Adding template subsystems...")
    
    gm.add_entity('primary', {
        'id': 'research-template',
        'label': 'Research Template',
        'type': 'subsystem',
        'description': 'Pre-configured template for academic research and literature mapping',
        'version': '1.0',
        'status': 'active',
        'tech_stack': [],
        'source_documents': ['templates-doc', 'research-readme']
    })
    
    gm.add_entity('primary', {
        'id': 'systems-template',
        'label': 'Systems Mapping Template',
        'type': 'subsystem',
        'description': 'Pre-configured template for systems thinking and complex systems analysis',
        'version': '1.0',
        'status': 'active',
        'tech_stack': [],
        'source_documents': ['templates-doc', 'systems-readme']
    })
    
    gm.add_entity('primary', {
        'id': 'ecosystem-template',
        'label': 'Ecosystem Template',
        'type': 'subsystem',
        'description': 'Pre-configured template for stakeholder and ecosystem mapping',
        'version': '1.0',
        'status': 'active',
        'tech_stack': [],
        'source_documents': ['templates-doc', 'ecosystem-readme']
    })
    
    gm.add_entity('primary', {
        'id': 'generic-template',
        'label': 'Generic Template',
        'type': 'subsystem',
        'description': 'Customizable template for any domain-specific knowledge graph',
        'version': '1.0',
        'status': 'active',
        'tech_stack': [],
        'source_documents': ['templates-doc', 'generic-readme']
    })
    
    # ========================================
    # UI COMPONENTS
    # ========================================
    
    print("  Adding UI components...")
    
    gm.add_entity('primary', {
        'id': 'viewer-interface',
        'label': 'Web Viewer Interface',
        'type': 'interface',
        'description': 'Interactive HTML/JavaScript visualization interface using vis.js',
        'version': '1.0',
        'status': 'active',
        'tech_stack': ['HTML', 'JavaScript', 'vis.js', 'CSS'],
        'source_documents': ['readme']
    })
    
    # ========================================
    # DATA STORAGE
    # ========================================
    
    print("  Adding data components...")
    
    gm.add_entity('primary', {
        'id': 'entities-json',
        'label': 'Entities JSON Store',
        'type': 'data-store',
        'description': 'JSON file storing all graph entities and relationships',
        'version': '1.0',
        'status': 'active',
        'tech_stack': ['JSON'],
        'source_documents': []
    })
    
    gm.add_entity('primary', {
        'id': 'config-yaml',
        'label': 'Configuration YAML',
        'type': 'data-store',
        'description': 'YAML configuration defining entity types, relationships, and visualization',
        'version': '1.0',
        'status': 'active',
        'tech_stack': ['YAML'],
        'source_documents': ['readme']
    })
    
    # ========================================
    # EXTERNAL DEPENDENCIES
    # ========================================
    
    print("  Adding external dependencies...")
    
    gm.add_entity('primary', {
        'id': 'pyyaml',
        'label': 'PyYAML Library',
        'type': 'external-system',
        'description': 'Python YAML parser and emitter',
        'version': '6.0+',
        'status': 'active',
        'tech_stack': ['Python'],
        'source_documents': []
    })
    
    gm.add_entity('primary', {
        'id': 'google-gen-ai',
        'label': 'Google Generative AI SDK',
        'type': 'external-system',
        'description': 'Python SDK for Google Gemini API',
        'version': '0.3.0+',
        'status': 'active',
        'tech_stack': ['Python'],
        'source_documents': []
    })
    
    gm.add_entity('primary', {
        'id': 'visjs',
        'label': 'vis.js Network Library',
        'type': 'external-system',
        'description': 'JavaScript library for network visualization',
        'version': '9.1.0+',
        'status': 'active',
        'tech_stack': ['JavaScript'],
        'source_documents': []
    })
    
    # ========================================
    # TEAM
    # ========================================
    
    print("  Adding team information...")
    
    gm.add_entity('contributors', {
        'id': 'dev-team',
        'name': 'Development Team',
        'department': 'Engineering',
        'responsibilities': ['Core functionality', 'Templates', 'Documentation'],
        'owned_components': [
            'graph-manager', 'config-loader', 'http-server', 
            'setup-wizard', 'viewer-interface'
        ],
        'contact': 'github.com/earlyprototype/knowledge-graph-kit'
    })
    
    # ========================================
    # DOCUMENTATION
    # ========================================
    
    print("  Adding documentation...")
    
    gm.add_entity('sources', {
        'id': 'readme',
        'title': 'Main README',
        'authors': ['Development Team'],
        'last_updated': '2024-11-12',
        'type': 'system-document',
        'key_components': [
            'graph-manager', 'config-loader', 'setup-wizard',
            'research-template', 'systems-template', 'ecosystem-template', 'generic-template'
        ],
        'status': 'current'
    })
    
    gm.add_entity('sources', {
        'id': 'templates-doc',
        'title': 'Templates Documentation',
        'authors': ['Development Team'],
        'last_updated': '2024-11-12',
        'type': 'system-document',
        'key_components': [
            'research-template', 'systems-template', 'ecosystem-template', 'generic-template'
        ],
        'status': 'current'
    })
    
    gm.add_entity('sources', {
        'id': 'systems-readme',
        'title': 'Systems Template README',
        'authors': ['Development Team'],
        'last_updated': '2024-11-12',
        'type': 'system-document',
        'key_components': ['systems-template'],
        'status': 'current'
    })
    
    # ========================================
    # RELATIONSHIPS - Dependencies
    # ========================================
    
    print("  Adding relationships...")
    
    # Graph Manager dependencies
    gm.add_relationship('graph-manager', 'config-loader', 'depends-on',
                       description='Loads configuration to understand entity schema')
    gm.add_relationship('graph-manager', 'entities-json', 'consumes-data-from',
                       description='Reads and writes entity data')
    gm.add_relationship('graph-manager', 'pyyaml', 'depends-on',
                       description='Uses PyYAML for configuration parsing')
    
    # Config Loader dependencies
    gm.add_relationship('config-loader', 'config-yaml', 'consumes-data-from',
                       description='Reads YAML configuration')
    gm.add_relationship('config-loader', 'pyyaml', 'depends-on',
                       description='Uses PyYAML library')
    
    # Server dependencies
    gm.add_relationship('http-server', 'viewer-interface', 'deployed-on',
                       description='Serves the HTML viewer interface')
    gm.add_relationship('http-server', 'entities-json', 'consumes-data-from',
                       description='Serves entity data to frontend')
    
    # Gemini API Server dependencies
    gm.add_relationship('gemini-api-server', 'google-gen-ai', 'depends-on',
                       description='Uses Gemini SDK for AI chat')
    gm.add_relationship('gemini-api-server', 'entities-json', 'consumes-data-from',
                       description='Reads graph data for context')
    
    # Setup Wizard dependencies
    gm.add_relationship('setup-wizard', 'research-template', 'integrates-with',
                       description='Can initialize from research template')
    gm.add_relationship('setup-wizard', 'systems-template', 'integrates-with',
                       description='Can initialize from systems template')
    gm.add_relationship('setup-wizard', 'ecosystem-template', 'integrates-with',
                       description='Can initialize from ecosystem template')
    gm.add_relationship('setup-wizard', 'generic-template', 'integrates-with',
                       description='Can initialize from generic template')
    gm.add_relationship('setup-wizard', 'init-script', 'calls',
                       description='Executes template initialization')
    
    # Viewer dependencies
    gm.add_relationship('viewer-interface', 'visjs', 'depends-on',
                       description='Uses vis.js for graph visualization')
    gm.add_relationship('viewer-interface', 'gemini-api-server', 'calls',
                       description='Optional AI chat integration')
    
    # Template relationships
    for template_id in ['research-template', 'systems-template', 'ecosystem-template', 'generic-template']:
        gm.add_relationship(template_id, 'config-yaml', 'consumes-data-from',
                           description='Contains template-specific configuration')
        gm.add_relationship(template_id, 'viewer-interface', 'integrates-with',
                           description='Includes viewer interface')
        gm.add_relationship(template_id, 'init-script', 'integrates-with',
                           description='Includes initialization script')
    
    # Ownership relationships
    for component in ['graph-manager', 'config-loader', 'http-server', 'setup-wizard', 'viewer-interface']:
        gm.add_relationship(component, 'dev-team', 'owned-by')
    
    # Documentation relationships
    gm.add_relationship('graph-manager', 'readme', 'documented-in')
    gm.add_relationship('config-loader', 'readme', 'documented-in')
    gm.add_relationship('http-server', 'readme', 'documented-in')
    gm.add_relationship('setup-wizard', 'readme', 'documented-in')
    gm.add_relationship('systems-template', 'systems-readme', 'documented-in')
    gm.add_relationship('systems-template', 'templates-doc', 'documented-in')
    
    # ========================================
    # SAVE
    # ========================================
    
    print("  Saving graph...")
    gm.save()
    
    print("\n[SUCCESS] Knowledge Graph Kit systems map created successfully!")
    
    # Count entities across all categories
    total_entities = sum(len(gm.graph_data.get(category, [])) 
                        for category in ['components', 'teams', 'specifications'])
    total_relationships = len(gm.graph_data.get('relationships', []))
    
    print("   - Total entities:", total_entities)
    print("   - Total relationships:", total_relationships)
    print("\nTo view the map, run:")
    print("   python examples/server.py --directory examples/systems-map-example")
    print("\nThen open: http://localhost:8000/viewer.html")

if __name__ == '__main__':
    build_knowledge_graph_kit_map()
