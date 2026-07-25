# Template Guide

Five ready-to-use templates for different knowledge graph applications.

---

## 📊 Quick Comparison

| Template | Primary Use Case | Entities | Best For |
|----------|-----------------|----------|----------|
| **Research** | Academic research | Concepts, Researchers, Papers | Literature reviews, systematic analysis |
| **Systems** | Software architecture | Components, Teams, Specifications | Microservices, dependencies |
| **Ecosystem** | Stakeholder analysis | Elements, Stakeholders, Insights | Value flows, power mapping |
| **Evidence** | Claim tracking | Claims, Runs, Sources | Experimental programmes, self-correction audits |
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

## ⚖️ Evidence Template

### Purpose
Experimental programmes and claim tracking: what was believed, what was run, what the run did to the belief.

### Entities

**Claims** (Primary)
- Types: hypothesis, finding, concept
- Statuses: supported, refuted, qualified, retired, corrected, open, untested
- Fields: label, type, status, description, phase, asserted, retired, doc_ref, evidence

**Runs** (Contributors)
- Types: run, model, null-model
- Fields: label, type, description, script, output_dir, n, date

**Sources** (Sources)
- Types: doc, artefact, prior-work
- Fields: title, type, path, description

### Key Relationships

Edges are grouped by what they do, and the viewer styles each group differently:

- **Epistemic** (signed — these change what you believe): `supports`, `refutes`, `qualifies`, `corrects`, `retires`, `supersedes`, `tests`
- **Structural** (neutral plumbing): `produced-by`, `run-on`, `evidenced-by`, `documented-in`
- **Associative** (soft links): `analogous-to`, `breaks-down-at`, `builds-on`, `cites`, `relates-to`

Every relationship carries a required `description` saying *why*, and an optional `asserted` date that drives the timeline.

### Use Cases
- Hypothesis-to-finding chains with the run that settled them
- Self-correction audits — which results corrected or retired which
- Provenance for a published number, back to the script and output directory
- Replaying a programme's understanding as it stood on any given date
- Separating what still stands from what has been superseded

### Viewer extras

Beyond the shared viewer features, the Evidence template adds a timeline scrubber
(with play/pause), status and type filter chips, colour-by-status vs colour-by-type,
and a "copy evidence chain" action that renders a claim's provenance as plain text.

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

### Choose Evidence if:
✅ Tracking claims that can be refuted or corrected  
✅ Recording which experiment produced which result  
✅ Auditing how understanding changed over time  
✅ You need status, not just structure

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

The Evidence template additionally ships a timeline scrubber, status/type filter chips
and canonical status colours and edge styles (see `visualization.status_colors` and
`visualization.edge_styles` in its `config.yaml`).

---

## Further Customization

All templates can be further customized:

- **Add entity subtypes** in `config.yaml`
- **Define custom relationships** in `relationships.types`
- **Change colors** in `visualization.colors`
- **Change status colours** in `visualization.status_colors` (Evidence)
- **Restyle edges per type** in `visualization.edge_styles` (Evidence)
- **Change node shapes** in `visualization.node_shapes` (Evidence)
- **Modify node sizes** in `visualization.node_sizes`
- **Add custom fields** in `entity_types.*.fields`

See template READMEs for detailed customization instructions.
