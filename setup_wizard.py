#!/usr/bin/env python3
"""
Knowledge Graph Kit - Interactive Setup Wizard
Walks you through template selection, configuration, and server setup
"""

import sys
import os
import shutil
import json
from pathlib import Path
from getpass import getpass


def print_header(text):
    """Print formatted header"""
    print("\n" + "=" * 60)
    print(f"  {text}")
    print("=" * 60 + "\n")


def print_box(text):
    """Print text in a box"""
    lines = text.split('\n')
    width = max(len(line) for line in lines) + 4
    print("\n┌" + "─" * (width - 2) + "┐")
    for line in lines:
        print(f"│ {line.ljust(width - 4)} │")
    print("└" + "─" * (width - 2) + "┘\n")


def get_input(prompt, options=None, default=None):
    """Get user input with validation"""
    while True:
        if default:
            user_input = input(f"{prompt} [{default}]: ").strip() or default
        else:
            user_input = input(f"{prompt}: ").strip()
        
        if options and user_input not in options:
            print(f"Invalid choice. Please choose from: {', '.join(options)}")
            continue
        
        return user_input


def get_yes_no(prompt, default='n'):
    """Get yes/no answer"""
    choice = get_input(f"{prompt} (y/n)", default=default).lower()
    return choice in ['y', 'yes']


def select_template():
    """Template selection menu"""
    print_header("Step 1: Choose Your Template")
    
    print("Available templates:\n")
    print("1. Research     - Academic papers, concepts, researchers")
    print("2. Systems      - Software architecture, microservices, teams")
    print("3. Ecosystem    - Stakeholders, organizations, value flows")
    print("4. Generic      - Blank canvas (customize everything)")
    print()
    
    choice = get_input("Select template (1-4)", options=['1', '2', '3', '4'])
    
    templates = {
        '1': ('research', 'Research'),
        '2': ('systems', 'Systems Architecture'),
        '3': ('ecosystem', 'Ecosystem Mapping'),
        '4': ('generic', 'Generic (Customizable)')
    }
    
    return templates[choice]


def customize_generic():
    """Customize generic template"""
    print_header("Generic Template Customization")
    
    print("Let's customize your knowledge graph...\n")
    
    # Domain name
    domain = get_input("What domain are you mapping? (e.g., 'project-dependencies', 'team-structure')", 
                      default="custom")
    
    # Primary entities
    print("\n--- Primary Entities ---")
    print("These are the main things in your graph (e.g., components, modules, ideas)")
    primary_name = get_input("What do you call the primary entities?", default="elements")
    primary_label = get_input("Display label (singular)", default=primary_name.title())
    
    print(f"\nEntity types for {primary_label} (comma-separated):")
    print("Example: service, module, library")
    types_input = get_input("Types", default="type-a, type-b, type-c")
    primary_types = [t.strip() for t in types_input.split(',')]
    
    # Contributors
    print("\n--- Contributor Entities ---")
    print("Who/what owns or contributes to the primary entities?")
    contributor_name = get_input("What do you call contributors?", default="actors")
    contributor_label = get_input("Display label (singular)", default=contributor_name.title())
    
    # Sources
    print("\n--- Source Entities ---")
    print("What documents/sources provide information?")
    source_name = get_input("What do you call sources?", default="documents")
    source_label = get_input("Display label (singular)", default=source_name.title())
    
    # Relationships
    print("\n--- Relationships ---")
    print("How do entities relate? (comma-separated)")
    print("Example: depends-on, uses, provides-to")
    rel_input = get_input("Relationship types", 
                         default="connects-to, depends-on, uses")
    relationships = [r.strip() for r in rel_input.split(',')]
    
    return {
        'domain': domain,
        'primary': {
            'name': primary_name,
            'label': primary_label,
            'types': primary_types
        },
        'contributors': {
            'name': contributor_name,
            'label': contributor_label
        },
        'sources': {
            'name': source_name,
            'label': source_label
        },
        'relationships': relationships
    }


def setup_gemini():
    """Setup Gemini integration"""
    print_header("Step 2: Gemini AI Integration")
    
    print("Gemini provides AI chat with knowledge graph context.\n")
    print("Features:")
    print("  • Ask questions about your graph")
    print("  • Find connections and patterns")
    print("  • Get insights and suggestions")
    print()
    
    if not get_yes_no("Enable Gemini AI chat?", default='y'):
        return None
    
    print("\nYou'll need a Google AI API key (free tier available)")
    print("Get one at: https://makersuite.google.com/app/apikey")
    print()
    
    api_key = getpass("Enter your Gemini API key (hidden): ").strip()
    
    if not api_key:
        print("⚠️  No API key provided. You can add it later in gemini_config.json")
        return None
    
    model = get_input("Gemini model", default="gemini-2.0-flash-exp")
    
    return {
        'api_key': api_key,
        'model': model
    }


def create_project(template_id, template_name, custom_config=None, gemini_config=None):
    """Create the knowledge graph project"""
    print_header("Step 3: Project Setup")
    
    # Get project name
    default_name = template_id.replace(' ', '-').lower() + "-kg"
    project_name = get_input("Project directory name", default=default_name)
    project_path = Path(project_name)
    
    if project_path.exists():
        if not get_yes_no(f"⚠️  Directory '{project_name}' exists. Overwrite?", default='n'):
            print("\n❌ Setup cancelled.")
            sys.exit(0)
        shutil.rmtree(project_path)
    
    print(f"\n📁 Creating project: {project_name}")
    
    # Copy template
    template_path = Path(__file__).parent / "templates" / template_id
    shutil.copytree(template_path, project_path)
    print(f"✓ Copied {template_name} template")
    
    # Apply generic customizations
    if custom_config and template_id == 'generic':
        config_file = project_path / "config.yaml"
        apply_generic_customizations(config_file, custom_config)
        print(f"✓ Applied customizations")
    
    # Setup Gemini
    if gemini_config:
        gemini_config_file = project_path / "gemini_config.json"
        with open(gemini_config_file, 'w') as f:
            json.dump(gemini_config, f, indent=2)
        print(f"✓ Configured Gemini AI")
    
    # Initialize graph
    os.chdir(project_path)
    from core.graph_manager import GraphManager
    gm = GraphManager('config.yaml')
    gm.save()
    print(f"✓ Initialized knowledge graph")
    
    return project_path


def apply_generic_customizations(config_file, custom):
    """Apply generic template customizations"""
    import yaml
    
    with open(config_file, 'r') as f:
        config = yaml.safe_load(f)
    
    # Update domain
    config['domain'] = custom['domain']
    
    # Update entity types
    config['entity_types']['primary']['name'] = custom['primary']['name']
    config['entity_types']['primary']['label_singular'] = custom['primary']['label']
    config['entity_types']['primary']['label_plural'] = custom['primary']['label'] + 's'
    config['entity_types']['primary']['types'] = custom['primary']['types']
    
    config['entity_types']['contributors']['name'] = custom['contributors']['name']
    config['entity_types']['contributors']['label_singular'] = custom['contributors']['label']
    config['entity_types']['contributors']['label_plural'] = custom['contributors']['label'] + 's'
    
    config['entity_types']['sources']['name'] = custom['sources']['name']
    config['entity_types']['sources']['label_singular'] = custom['sources']['label']
    config['entity_types']['sources']['label_plural'] = custom['sources']['label'] + 's'
    
    # Update relationships
    config['relationships']['types'] = custom['relationships']
    
    with open(config_file, 'w') as f:
        yaml.dump(config, f, default_flow_style=False, sort_keys=False)


def print_next_steps(project_path, has_gemini):
    """Print next steps"""
    print_header("🎉 Setup Complete!")
    
    print_box(f"""
Knowledge Graph Created: {project_path}

Next Steps:

1. Navigate to project:
   cd {project_path}

2. Add entities (Python API):
   python
   >>> from core.graph_manager import GraphManager
   >>> gm = GraphManager('config.yaml')
   >>> gm.add_entity('primary', {{
   ...     'id': 'my-entity',
   ...     'label': 'My Entity',
   ...     'type': 'type-here',
   ...     'description': 'Description here'
   ... }})
   >>> gm.save()

3. Start viewer:
   {"python start_server.py  # With Gemini chat" if has_gemini else "python server.py"}

4. Open browser:
   http://localhost:8000

{"5. Chat with AI:" if has_gemini else ""}
{"   Click 'Chat with AI' button in viewer" if has_gemini else ""}
""")
    
    print("📚 Documentation:")
    print(f"   - Project README: {project_path}/README.md")
    print(f"   - Main docs: knowledge-graph-kit/README.md")
    print(f"   - Template guide: knowledge-graph-kit/TEMPLATES.md")
    print()


def main():
    """Main setup wizard"""
    print_box("""
╔═══════════════════════════════════════╗
║  Knowledge Graph Kit - Setup Wizard  ║
╚═══════════════════════════════════════╝

Welcome! This wizard will help you:
  • Choose a template
  • Configure Gemini AI (optional)
  • Set up your project
  • Launch servers
""")
    
    try:
        # Step 1: Choose template
        template_id, template_name = select_template()
        
        # Step 1b: Customize generic if needed
        custom_config = None
        if template_id == 'generic':
            custom_config = customize_generic()
        
        # Step 2: Gemini setup
        gemini_config = setup_gemini()
        
        # Step 3: Create project
        project_path = create_project(template_id, template_name, custom_config, gemini_config)
        
        # Done!
        print_next_steps(project_path, gemini_config is not None)
        
        # Ask to start servers
        if get_yes_no("\n🚀 Start servers now?", default='y'):
            os.chdir(project_path)
            if gemini_config:
                print("\n🌐 Starting HTTP server (port 8000)...")
                print("🤖 Starting Gemini API server (port 8001)...")
                os.system("python start_server.py")
            else:
                print("\n🌐 Starting HTTP server (port 8000)...")
                os.system("python server.py")
    
    except KeyboardInterrupt:
        print("\n\n❌ Setup cancelled by user.")
        sys.exit(0)
    except Exception as e:
        print(f"\n\n❌ Error: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)


if __name__ == "__main__":
    # Check if running from correct directory
    if not Path("templates").exists():
        print("❌ Error: Must run from knowledge-graph-kit directory")
        print("Usage: cd knowledge-graph-kit && python setup_wizard.py")
        sys.exit(1)
    
    main()

