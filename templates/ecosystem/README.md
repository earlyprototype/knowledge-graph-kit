# Ecosystem Mapping Template

Knowledge graph optimized for mapping stakeholder ecosystems, organizations, resources, and value flows.

## Entities

### Elements (Primary)
Organizations, platforms, resources, processes, capabilities, and market forces in your ecosystem.

**Types:**
- organization (companies, institutions, agencies)
- platform (digital platforms, marketplaces)
- resource (funding, knowledge, infrastructure)
- process (workflows, methodologies, practices)
- capability (skills, competencies, functions)
- value-stream (value creation/delivery chains)
- market (market segments, sectors)
- technology (key technologies in ecosystem)
- policy (regulations, policies, standards)
- infrastructure (physical/digital infrastructure)

**Fields:**
- `id`: Unique identifier
- `label`: Display name
- `type`: Element type
- `description`: What it is/does
- `sector`: Industry sector or domain
- `maturity`: emerging | developing | mature | declining
- `scale`: local | regional | national | global
- `source_insights`: Insight IDs that mention this
- `related_to`: Related element IDs
- `components`: Sub-element IDs

### Stakeholders (Contributors)
People, organizations, institutions, communities involved in ecosystem.

**Fields:**
- `id`: Unique identifier
- `name`: Stakeholder name
- `type`: individual | organization | institution | community | government
- `role`: Role in ecosystem
- `influence_level`: high | medium | low
- `interests`: Key interests and motivations
- `key_elements`: Element IDs they're involved with
- `mentioned_in`: Insight IDs

### Insights (Sources)
Research findings, interviews, observations, reports about the ecosystem.

**Fields:**
- `id`: Unique identifier
- `title`: Insight title
- `source_type`: interview | report | survey | observation | workshop | secondary-research
- `date`: Date collected/published
- `authors`: Who generated the insight
- `key_elements`: Elements mentioned
- `key_findings`: Main findings (array)
- `references`: Other insight IDs
- `status`: validated | preliminary | needs-verification

## Relationships

- `provides-to`: Element A provides value/resource to B
- `receives-from`: Element A receives from B
- `influences`: Element A influences B
- `depends-on`: Element A depends on B
- `competes-with`: Competition relationship
- `partners-with`: Partnership/collaboration
- `funds`: Provides funding
- `regulates`: Regulatory relationship
- `enables`: Element A enables B's operation
- `constrains`: Element A constrains B
- `collaborates-with`: Active collaboration
- `supplies`: Supply chain relationship
- `consumes`: Consumption relationship

## Use Cases

### 1. Stakeholder Mapping
Identify all stakeholders and their relationships.

### 2. Power Analysis
Understand influence and power structures.

### 3. Value Flow Mapping
Trace how value flows through ecosystem.

### 4. Gap Analysis
Find missing elements or relationships.

### 5. Opportunity Identification
Spot collaboration or intervention opportunities.

### 6. Risk Assessment
Identify dependencies and vulnerabilities.

## Example Usage

```python
from core.graph_manager import GraphManager

gm = GraphManager('config.yaml')

# Add organization
gm.add_entity('primary', {
    'id': 'startup-accelerator',
    'label': 'Tech Accelerator Inc',
    'type': 'organization',
    'description': 'Provides funding and mentorship to early-stage startups',
    'sector': 'Technology',
    'maturity': 'mature',
    'scale': 'national',
    'source_insights': ['interview-001', 'report-tech-ecosystem']
})

# Add funding resource
gm.add_entity('primary', {
    'id': 'seed-funding-pool',
    'label': 'Seed Funding Pool',
    'type': 'resource',
    'description': '£2M annual funding for startups',
    'sector': 'Finance',
    'maturity': 'mature',
    'scale': 'regional'
})

# Add platform
gm.add_entity('primary', {
    'id': 'innovation-hub',
    'label': 'Regional Innovation Hub',
    'type': 'platform',
    'description': 'Physical space and community for entrepreneurs',
    'sector': 'Technology',
    'maturity': 'developing',
    'scale': 'regional',
    'components': ['coworking-space', 'event-space', 'mentorship-program']
})

# Add stakeholder
gm.add_entity('contributors', {
    'id': 'angel-investor-jane',
    'name': 'Jane Smith',
    'type': 'individual',
    'role': 'Angel Investor',
    'influence_level': 'high',
    'interests': ['AI startups', 'SaaS', 'Deep tech'],
    'key_elements': ['startup-accelerator', 'seed-funding-pool']
})

# Add policy
gm.add_entity('primary', {
    'id': 'innovation-grant-policy',
    'label': 'Government Innovation Grant Scheme',
    'type': 'policy',
    'description': 'Tax incentives and grants for R&D',
    'sector': 'Policy',
    'maturity': 'mature',
    'scale': 'national'
})

# Add insight
gm.add_entity('sources', {
    'id': 'interview-001',
    'title': 'Interview: Tech Accelerator Founders',
    'source_type': 'interview',
    'date': '2024-10-15',
    'authors': ['Research Team'],
    'key_elements': ['startup-accelerator', 'innovation-hub'],
    'key_findings': [
        'Funding gap for pre-seed stage',
        'Need for more technical mentors',
        'Strong demand for workspace'
    ],
    'status': 'validated'
})

# Add relationships
gm.add_relationship('startup-accelerator', 'seed-funding-pool', 'provides-to',
                   description='Distributes seed funding to startups')

gm.add_relationship('angel-investor-jane', 'seed-funding-pool', 'funds',
                   description='Contributes to funding pool')

gm.add_relationship('innovation-grant-policy', 'startup-accelerator', 'enables',
                   description='Government policy enables accelerator operations')

gm.add_relationship('startup-accelerator', 'innovation-hub', 'partners-with',
                   description='Collaboration on space and events')

gm.save()
```

## Visualization

Run `python server.py` to visualize:

- **Blue circles** = Organizations
- **Purple circles** = Platforms
- **Green circles** = Resources
- **Orange circles** = Processes
- **Teal circles** = Capabilities
- **Red circles** = Value streams
- **Dark grey circles** = Markets
- **Orange-red circles** = Policies
- **Grey boxes** = Stakeholders
- **Yellow diamonds** = Insights

## Analysis Approaches

### Stakeholder Power Mapping
1. Filter by `influence_level: high`
2. See what they control/influence
3. Identify power concentrations

### Value Flow Analysis
1. Follow `provides-to` and `receives-from` chains
2. Map complete value streams
3. Identify bottlenecks

### Dependency Analysis
1. Find `depends-on` relationships
2. Identify single points of failure
3. Assess ecosystem resilience

### Gap Identification
1. Look for isolated elements (few connections)
2. Find missing relationship types
3. Identify unserved needs

### Collaboration Opportunities
1. Find elements that don't directly connect but share interests
2. Identify complementary capabilities
3. Spot potential partnerships

## Tips for Ecosystem Mapping

- **Start broad**: Map major players first
- **Track provenance**: Always link to insights
- **Verify influence**: Don't assume, validate with stakeholders
- **Update regularly**: Ecosystems evolve quickly
- **Multi-perspective**: Interview diverse stakeholders
- **Value flows matter**: Follow the money/resources/knowledge
- **Scale appropriately**: Match detail to project scope

## Integration with Research Methods

### After Interviews
```python
# Add stakeholder interviewed
gm.add_entity('contributors', {...})

# Add insights from interview
gm.add_entity('sources', {
    'source_type': 'interview',
    'key_findings': [...],
    ...
})

# Add elements they mentioned
# Add relationships they described
```

### After Document Analysis
```python
gm.add_entity('sources', {
    'source_type': 'secondary-research',
    'references': ['other-report-ids'],
    ...
})
```

### After Workshops
```python
gm.add_entity('sources', {
    'source_type': 'workshop',
    'key_findings': ['Collaboratively identified gaps', ...],
    ...
})
```

## Validation Status

Use `status` field on insights:
- `preliminary`: Initial findings, not yet validated
- `validated`: Confirmed by multiple sources
- `needs-verification`: Conflicting information, needs follow-up

