# Generic Template

Configurable knowledge graph for any domain. Adapt entity types, relationships, and visualization to your needs.

## Quick Customization Guide

### 1. Choose Your Domain

Edit `config.yaml`:
```yaml
domain: systems  # or ecosystem, project, etc.
```

### 2. Rename Entity Types

```yaml
entity_types:
  primary:
    name: components  # Was: elements
    label_singular: Component
    label_plural: Components
```

**Examples by domain:**

**Systems Mapping:**
- primary: `components` (services, modules, systems)
- contributors: `teams` (dev teams, owners)
- sources: `specifications` (architecture docs, ADRs)

**Ecosystem Analysis:**
- primary: `elements` (organizations, resources, platforms)
- contributors: `stakeholders` (people, institutions)
- sources: `insights` (reports, interviews, analyses)

**Project Dependencies:**
- primary: `modules` (code modules, libraries)
- contributors: `owners` (teams, maintainers)
- sources: `documentation` (READMEs, specs)

### 3. Define Entity Types

```yaml
entity_types:
  primary:
    types:
      - service        # For systems
      - module
      - interface
      - data-store
```

### 4. Define Relationships

```yaml
relationships:
  types:
    - calls            # For systems
    - depends-on
    - deployed-on
    - monitored-by
```

### 5. Set Colors

```yaml
visualization:
  colors:
    service: "#3498db"
    module: "#e74c3c"
    interface: "#2ecc71"
```

## Usage Examples

### Example 1: Systems Architecture Graph

```yaml
# config.yaml
domain: systems
entity_types:
  primary:
    name: components
    types: [service, module, interface, database]
  contributors:
    name: teams
  sources:
    name: specifications

relationships:
  types: [calls, depends-on, consumes-data, deployed-on]
```

```python
# add_component.py
from core.graph_manager import GraphManager

gm = GraphManager('config.yaml')

# Add microservice
gm.add_entity('primary', {
    'id': 'auth-service',
    'label': 'Authentication Service',
    'type': 'service',
    'description': 'Handles user authentication and authorization',
    'related_to': ['user-service']
})

# Add team
gm.add_entity('contributors', {
    'id': 'platform-team',
    'name': 'Platform Team',
    'role': 'Service Owners',
    'key_items': ['auth-service']
})

# Add dependency
gm.add_relationship('auth-service', 'user-db', 'consumes-data')

gm.save()
```

### Example 2: Ecosystem Mapping

```yaml
# config.yaml
domain: ecosystem
entity_types:
  primary:
    name: elements
    types: [organization, platform, resource, process]
  contributors:
    name: stakeholders
  sources:
    name: insights

relationships:
  types: [provides-to, receives-from, influences, funds, competes-with]
```

```python
# map_ecosystem.py
from core.graph_manager import GraphManager

gm = GraphManager('config.yaml')

# Add organization
gm.add_entity('primary', {
    'id': 'startup-accelerator',
    'label': 'Tech Accelerator Inc',
    'type': 'organization',
    'description': 'Provides funding and mentorship to startups'
})

# Add stakeholder
gm.add_entity('contributors', {
    'id': 'investor-jane',
    'name': 'Jane Smith',
    'role': 'Angel Investor',
    'responsibilities': ['Funding', 'Strategic advice']
})

# Add relationship
gm.add_relationship('startup-accelerator', 'investor-jane', 'receives-from',
                   description='Receives investment funding')

gm.save()
```

### Example 3: Project Dependencies

```yaml
# config.yaml
domain: project
entity_types:
  primary:
    name: modules
    types: [library, package, service, tool]
  contributors:
    name: maintainers
  sources:
    name: documentation

relationships:
  types: [depends-on, extends, implements, requires]
```

## Adding Custom Relationship Types

At runtime, add new relationship types via `custom_variables`:

```yaml
custom_variables:
  relationship_types:
    - name: mentors
      label: Mentors
      color: "#4CAF50"
      arrow_style: solid
    - name: collaborates-with
      label: Collaborates With
      color: "#9C27B0"
      arrow_style: dashed
```

## Tips

1. **Start simple** - Define 3-5 entity types max
2. **Clear naming** - Use domain-specific terminology
3. **Track provenance** - Always use `source_documents` field
4. **Consistent IDs** - Use `lowercase-with-hyphens`
5. **Visualize early** - Run server frequently to see structure

## Converting Between Templates

To migrate from generic → research or vice versa:

1. Export your data: `python export.py`
2. Map entity names in JSON
3. Import to new template: `python import.py`

Or use the merge tool:
```python
from core.graph_manager import GraphManager

gm_new = GraphManager('new-config.yaml')
gm_new.merge_from_file('old-entities.json')
gm_new.save()
```

