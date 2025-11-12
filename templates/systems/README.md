# Systems Architecture Template

Knowledge graph optimized for mapping software systems, microservices, components, and their dependencies.

## Entities

### Components (Primary)
Services, modules, subsystems, APIs, data stores, and external integrations.

**Types:**
- service (microservices, applications)
- module (internal modules, libraries)
- subsystem (major system components)
- interface (APIs, interfaces)
- data-store (databases, caches, queues)
- external-system (third-party services)
- api (REST, GraphQL, etc.)
- library (shared libraries)
- tool (dev tools, infrastructure)

**Fields:**
- `id`: Unique identifier (lowercase-hyphenated)
- `label`: Display name
- `type`: Component type
- `description`: What it does
- `version`: Current version
- `status`: active | deprecated | planned | archived
- `tech_stack`: Technologies used (e.g., ["Node.js", "PostgreSQL"])
- `source_documents`: Architecture docs, ADRs
- `related_to`: Related component IDs
- `components`: Sub-component IDs

### Teams (Contributors)
Development teams, platform teams, infrastructure teams.

**Fields:**
- `id`: Unique identifier
- `name`: Team name
- `department`: Department or division
- `responsibilities`: What they own/maintain
- `owned_components`: Component IDs they own
- `contact`: Contact info (email, Slack, etc.)

### Specifications (Sources)
Architecture documents, ADRs, API specs, runbooks, diagrams.

**Fields:**
- `id`: Unique identifier
- `title`: Document title
- `authors`: Document authors
- `last_updated`: Date
- `type`: architecture-document | adr | api-spec | technical-spec | runbook | diagram
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

### 1. Dependency Mapping
Map all service dependencies to understand system architecture.

### 2. Impact Analysis
When changing a component, see what else is affected.

### 3. Ownership Tracking
Know which team owns each component.

### 4. Migration Planning
Plan migrations by understanding dependency chains.

### 5. Documentation Gaps
Find components without architecture docs.

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
    'source_documents': ['arch-doc-auth', 'adr-005']
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

# Add architecture doc
gm.add_entity('sources', {
    'id': 'arch-doc-auth',
    'title': 'Authentication Service Architecture',
    'authors': ['Jane Smith', 'Platform Team'],
    'last_updated': '2024-11-01',
    'type': 'architecture-document',
    'key_components': ['auth-service', 'user-db'],
    'status': 'current'
})

# Add dependencies
gm.add_relationship('auth-service', 'user-db', 'consumes-data-from',
                   description='Reads/writes user authentication data')

gm.add_relationship('auth-service', 'platform-team', 'owned-by')

gm.add_relationship('auth-service', 'arch-doc-auth', 'documented-in')

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
- Link components to architecture docs
- Update `status` field when deprecating
- Use `tech_stack` to track technology dependencies
- Document ownership for all critical components

## Integration with Architecture Decision Records (ADRs)

Add ADRs as specifications:
```python
gm.add_entity('sources', {
    'id': 'adr-005',
    'title': 'ADR-005: Adopt Redis for Session Storage',
    'type': 'adr',
    'key_components': ['auth-service'],
    'status': 'current'
})

gm.add_relationship('auth-service', 'adr-005', 'implements')
```

