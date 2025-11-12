# Systems Mapping Template

Knowledge graph optimized for systems thinking, mapping complex systems, their components, relationships, and dependencies. Suitable for software systems, organizational systems, or any complex system analysis.

## Entities

### Components (Primary)
System components, services, modules, subsystems, interfaces, and their connections.

**Types:**
- service (services, applications, functions)
- module (internal modules, sub-components)
- subsystem (major system components)
- interface (APIs, interfaces, connection points)
- data-store (data repositories, information flows)
- external-system (external dependencies)
- api (interfaces and protocols)
- library (shared resources)
- tool (supporting systems, infrastructure)

**Fields:**
- `id`: Unique identifier (lowercase-hyphenated)
- `label`: Display name
- `type`: Component type
- `description`: What it does
- `version`: Current version
- `status`: active | deprecated | planned | archived
- `tech_stack`: Technologies used (e.g., ["Node.js", "PostgreSQL"])
- `source_documents`: System documentation, specifications
- `related_to`: Related component IDs
- `components`: Sub-component IDs

### Teams (Contributors)
Teams, departments, working groups, or responsible parties.

**Fields:**
- `id`: Unique identifier
- `name`: Team name
- `department`: Department or division
- `responsibilities`: What they own/maintain
- `owned_components`: Component IDs they own
- `contact`: Contact info (email, Slack, etc.)

### Specifications (Sources)
System documentation, specifications, design documents, diagrams.

**Fields:**
- `id`: Unique identifier
- `title`: Document title
- `authors`: Document authors
- `last_updated`: Date
- `type`: system-document | design-doc | specification | technical-spec | diagram | adr
- `key_components`: Components documented
- `references`: Other spec IDs
- `status`: current | outdated | draft

## Relationships

- `depends-on`: Component A depends on component B
- `integrates-with`: Components integrate/work together
- `calls`: Component A calls component B (API calls, RPC)
- `consumes-data-from`: Component reads data from another
- `produces-data-for`: Component writes data for another
- `deployed-on`: Component deployed on infrastructure
- `monitored-by`: Component monitored by tool
- `owned-by`: Component owned by team
- `extends`: Component extends another
- `implements`: Component implements spec/interface
- `replaces`: Component replaces another (deprecation)
- `communicates-with`: General communication
- `authenticated-by`: Auth mechanism

## Use Cases

### 1. Systems Thinking Analysis
Map complex systems to understand relationships, feedback loops, and emergent behaviors.

### 2. Dependency Mapping
Map all component dependencies to understand system structure.

### 3. Impact Analysis
When changing a component, see what else is affected through the system.

### 4. Ownership Tracking
Know which team or party is responsible for each component.

### 5. System Evolution Planning
Plan changes by understanding dependency chains and system dynamics.

### 6. Documentation Gaps
Find components without proper documentation.

## Example Usage

```python
from core.graph_manager import GraphManager

gm = GraphManager('config.yaml')

# Add microservice
gm.add_entity('primary', {
    'id': 'auth-service',
    'label': 'Authentication Service',
    'type': 'service',
    'description': 'Handles user authentication and session management',
    'version': 'v2.3.1',
    'status': 'active',
    'tech_stack': ['Node.js', 'Express', 'Redis', 'PostgreSQL'],
    'source_documents': ['system-doc-auth', 'spec-005']
})

# Add database
gm.add_entity('primary', {
    'id': 'user-db',
    'label': 'User Database',
    'type': 'data-store',
    'description': 'PostgreSQL database storing user accounts',
    'version': 'PostgreSQL 14',
    'status': 'active',
    'tech_stack': ['PostgreSQL']
})

# Add team
gm.add_entity('contributors', {
    'id': 'platform-team',
    'name': 'Platform Engineering',
    'department': 'Engineering',
    'responsibilities': ['Authentication', 'Authorization', 'User Management'],
    'owned_components': ['auth-service', 'user-db'],
    'contact': 'platform-team@company.com'
})

# Add system documentation
gm.add_entity('sources', {
    'id': 'system-doc-auth',
    'title': 'Authentication Service System Design',
    'authors': ['Jane Smith', 'Platform Team'],
    'last_updated': '2024-11-01',
    'type': 'system-document',
    'key_components': ['auth-service', 'user-db'],
    'status': 'current'
})

# Add dependencies
gm.add_relationship('auth-service', 'user-db', 'consumes-data-from',
                   description='Reads/writes user authentication data')

gm.add_relationship('auth-service', 'platform-team', 'owned-by')

gm.add_relationship('auth-service', 'system-doc-auth', 'documented-in')

gm.save()
```

## Visualization

Once populated, run `python server.py` to visualize:

- **Blue circles** = Services
- **Purple circles** = Modules
- **Green circles** = Subsystems
- **Orange circles** = Interfaces
- **Red circles** = Data stores
- **Grey circles** = External systems
- **Grey boxes** = Teams
- **Yellow diamonds** = Specifications

## Analysis Queries

### Find all dependencies of a service
Click service → Check "depends-on" relationships

### Find services without owners
Filter components → Look for ones without "owned-by" relationship

### Find deprecated components
Filter by `status: deprecated`

### Map data flow
Follow "consumes-data-from" and "produces-data-for" relationships

## Tips

- Use consistent naming: `service-name` not `ServiceName`
- Track versions for easier migration planning
- Link components to system documentation
- Update `status` field when deprecating
- Use `tech_stack` to track technology dependencies
- Document ownership for all critical components

## Integration with Design Documents & Decision Records

Add design documents or ADRs as specifications:
```python
gm.add_entity('sources', {
    'id': 'spec-005',
    'title': 'Design Decision: Session Storage Approach',
    'type': 'design-doc',
    'key_components': ['auth-service'],
    'status': 'current'
})

gm.add_relationship('auth-service', 'spec-005', 'implements')
```

