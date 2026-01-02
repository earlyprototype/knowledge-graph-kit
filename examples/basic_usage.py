"""
Basic usage examples for Knowledge Graph Kit
"""
import sys
import os

# Add parent directory to path to import core modules
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from core.graph_manager import GraphManager


def research_example():
    """Example: Building a research knowledge graph"""
    print("Research Graph Example")
    print("-" * 50)
    
    gm = GraphManager(config_path='../templates/research/config.yaml')
    
    # Add a concept
    gm.add_entity('primary', {
        'id': 'design-thinking',
        'label': 'Design Thinking',
        'type': 'methodology',
        'description': 'User-centered, iterative innovation process',
        'aliases': ['DT', 'design thinking process'],
        'source_papers': ['paper-001']
    })
    
    # Add a researcher
    gm.add_entity('contributors', {
        'id': 'doe-jane',
        'name': 'Jane Doe',
        'affiliation': 'University of Example',
        'contributions': ['Design thinking methodology', 'Innovation frameworks']
    })
    
    # Add a paper
    gm.add_entity('sources', {
        'id': 'paper-001',
        'title': 'Design Thinking in Practice',
        'authors': ['Jane Doe'],
        'year': 2024,
        'type': 'empirical-study',
        'key_concepts': ['design-thinking'],
        'status': 'analyzed'
    })
    
    # Add relationships
    gm.add_relationship('design-thinking', 'human-centered-design', 'relates-to')
    gm.add_relationship('doe-jane', 'design-thinking', 'theorized')
    
    gm.save()
    print(f"Stats: {gm.get_stats()}")
    print("✓ Research graph created")


def systems_example():
    """Example: Mapping system architecture"""
    print("\nSystems Architecture Example")
    print("-" * 50)
    
    gm = GraphManager(config_path='../templates/systems/config.yaml')
    
    # Add a microservice
    gm.add_entity('primary', {
        'id': 'auth-service',
        'label': 'Authentication Service',
        'type': 'service',
        'description': 'Handles user authentication and sessions',
        'version': 'v2.1.0',
        'status': 'active',
        'tech_stack': ['Node.js', 'Express', 'Redis', 'PostgreSQL']
    })
    
    # Add a database
    gm.add_entity('primary', {
        'id': 'user-db',
        'label': 'User Database',
        'type': 'data-store',
        'description': 'PostgreSQL database storing user data',
        'version': 'PostgreSQL 14',
        'status': 'active'
    })
    
    # Add a team
    gm.add_entity('contributors', {
        'id': 'platform-team',
        'name': 'Platform Engineering',
        'department': 'Engineering',
        'responsibilities': ['Authentication', 'Infrastructure'],
        'owned_components': ['auth-service', 'user-db']
    })
    
    # Add dependencies
    gm.add_relationship('auth-service', 'user-db', 'depends-on',
                       description='Reads/writes user authentication data')
    gm.add_relationship('auth-service', 'platform-team', 'owned-by')
    
    gm.save()
    print(f"Stats: {gm.get_stats()}")
    print("✓ Systems graph created")


def ecosystem_example():
    """Example: Mapping stakeholder ecosystem"""
    print("\nEcosystem Mapping Example")
    print("-" * 50)
    
    gm = GraphManager(config_path='../templates/ecosystem/config.yaml')
    
    # Add an organization
    gm.add_entity('primary', {
        'id': 'tech-accelerator',
        'label': 'Tech Accelerator Inc',
        'type': 'organization',
        'description': 'Provides funding and mentorship to startups',
        'sector': 'Technology',
        'maturity': 'mature',
        'scale': 'national'
    })
    
    # Add a resource
    gm.add_entity('primary', {
        'id': 'seed-funding',
        'label': 'Seed Funding Pool',
        'type': 'resource',
        'description': '£2M annual funding for early-stage startups',
        'sector': 'Finance',
        'maturity': 'mature'
    })
    
    # Add a stakeholder
    gm.add_entity('contributors', {
        'id': 'investor-jane',
        'name': 'Jane Smith',
        'type': 'individual',
        'role': 'Angel Investor',
        'influence_level': 'high',
        'interests': ['AI startups', 'Deep tech']
    })
    
    # Add value flows
    gm.add_relationship('tech-accelerator', 'seed-funding', 'provides-to',
                       description='Distributes funding to startups')
    gm.add_relationship('investor-jane', 'seed-funding', 'funds',
                       description='Contributes capital')
    
    gm.save()
    print(f"Stats: {gm.get_stats()}")
    print("✓ Ecosystem graph created")


if __name__ == "__main__":
    print("\nKnowledge Graph Kit - Usage Examples")
    print("=" * 50)
    
    # Run examples
    research_example()
    systems_example()
    ecosystem_example()
    
    print("\n" + "=" * 50)
    print("✓ All examples completed")
    print("\nNote: Examples use config from templates/ directory")
    print("In your projects, use: GraphManager('config.yaml')")
