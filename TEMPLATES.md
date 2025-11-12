# Template Guide

Four ready-to-use templates for different knowledge graph applications.

---

## 📊 Quick Comparison

| Template | Primary Use Case | Entities | Best For |
|----------|-----------------|----------|----------|
| **Research** | Academic research | Concepts, Researchers, Papers | Literature reviews, systematic analysis |
| **Systems** | Software architecture | Components, Teams, Specifications | Microservices, dependencies |
| **Ecosystem** | Stakeholder analysis | Elements, Stakeholders, Insights | Value flows, power mapping |
| **Generic** | Custom domains | Fully customizable | Anything else |

---

## 🎓 Research Template

### Purpose
Academic research, literature reviews, systematic paper analysis.

### Entities

**Concepts** (Primary)
- Types: methodology, framework, technology, principle, process, theory
- Fields: description, aliases, source_papers, related_to, components

**Researchers** (Contributors)
- Fields: name, affiliation, contributions, key_papers

**Papers** (Sources)
- Types: systematic-literature-review, empirical-study, theoretical, case-study
- Fields: title, authors, year, key_concepts, cites, status

### Key Relationships
`extends`, `builds-on`, `challenges`, `integrates-with`, `popularized`, `theorized`

### Use Cases
- Systematic literature reviews
- Concept mapping across papers
- Research gap identification
- Citation network analysis
- Theoretical framework building

---

## 🏗️ Systems Architecture Template

### Purpose
Software architecture, microservices mapping, dependency tracking.

### Entities

**Components** (Primary)
- Types: service, module, subsystem, interface, data-store, api, library
- Fields: description, version, status, tech_stack, related_to

**Teams** (Contributors)
- Fields: name, department, responsibilities, owned_components, contact

**Specifications** (Sources)
- Types: architecture-document, adr, api-spec, technical-spec, runbook
- Fields: title, authors, last_updated, key_components, status

### Key Relationships
`depends-on`, `calls`, `integrates-with`, `consumes-data-from`, `deployed-on`, `owned-by`, `monitored-by`

### Use Cases
- Service dependency mapping
- Impact analysis for changes
- Ownership tracking
- Migration planning
- Architecture documentation
- Technology stack visualization

---

## 🌐 Ecosystem Mapping Template

### Purpose
Stakeholder analysis, organizational networks, value flow mapping.

### Entities

**Elements** (Primary)
- Types: organization, platform, resource, process, capability, value-stream, market
- Fields: description, sector, maturity, scale, source_insights

**Stakeholders** (Contributors)
- Types: individual, organization, institution, community, government
- Fields: name, role, influence_level, interests, key_elements

**Insights** (Sources)
- Types: interview, report, survey, observation, workshop
- Fields: title, source_type, date, key_elements, key_findings, status

### Key Relationships
`provides-to`, `receives-from`, `influences`, `partners-with`, `funds`, `regulates`, `competes-with`

### Use Cases
- Stakeholder mapping
- Power analysis
- Value flow tracing
- Gap identification
- Opportunity spotting
- Risk assessment
- Ecosystem health analysis

---

## ⚙️ Generic Template

### Purpose
Custom domains not covered by specific templates.

### Customization

Edit `config.yaml` to define:
- Domain name
- Entity type names and labels
- Entity subtypes
- Relationship types
- Visualization colors

### Example Configurations

**Project Dependencies:**
```yaml
primary: modules (library, package, service)
contributors: maintainers
sources: documentation
relationships: depends-on, extends, implements
```

**Team Structure:**
```yaml
primary: roles (engineer, designer, manager)
contributors: people
sources: org-charts
relationships: reports-to, collaborates-with, manages
```

---

## Choosing a Template

### Choose Research if:
✅ Analyzing academic papers  
✅ Building literature reviews  
✅ Tracking theoretical concepts  
✅ Mapping research lineages

### Choose Systems if:
✅ Mapping microservices  
✅ Documenting architecture  
✅ Planning migrations  
✅ Tracking ownership

### Choose Ecosystem if:
✅ Mapping stakeholders  
✅ Analyzing value flows  
✅ Understanding power structures  
✅ Planning interventions

### Choose Generic if:
✅ Custom domain not listed  
✅ Need flexible schema  
✅ Experimental use case

---

## Switching Templates

You can convert between templates by mapping entity names:

```python
from core.graph_manager import GraphManager

# Load from one template
gm_old = GraphManager('old-template/config.yaml')
old_data = gm_old.graph_data

# Map entity names
mapped_data = {
    'components': old_data['concepts'],        # concepts → components
    'teams': old_data['researchers'],          # researchers → teams
    'specifications': old_data['papers'],      # papers → specifications
    'relationships': old_data['relationships']
}

# Save to new template
gm_new = GraphManager('new-template/config.yaml')
gm_new.merge(mapped_data)
gm_new.save()
```

---

## Template Features

All templates include:

✅ Full interactive viewer  
✅ Markdown document panel  
✅ Multi-tab viewing  
✅ Breadcrumb navigation  
✅ Search and filtering  
✅ Click-through navigation  
✅ Gemini AI integration (optional)  
✅ Config-driven customization  
✅ Provenance tracking

---

## Further Customization

All templates can be further customized:

- **Add entity subtypes** in `config.yaml`
- **Define custom relationships** in `relationships.types`
- **Change colors** in `visualization.colors`
- **Modify node sizes** in `visualization.node_sizes`
- **Add custom fields** in `entity_types.*.fields`

See template READMEs for detailed customization instructions.
