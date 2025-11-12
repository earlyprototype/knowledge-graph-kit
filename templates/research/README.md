# Research Template

Knowledge graph optimized for academic research, systematic literature reviews, and paper analysis.

## Entities

### Concepts (Primary)
Methodologies, frameworks, principles, technologies, and theories extracted from papers.

**Types:**
- methodology
- approach
- principle
- framework
- technology
- process
- theory

**Fields:**
- `id`: Unique identifier (lowercase-hyphenated)
- `label`: Display name
- `type`: One of the types above
- `description`: Clear description
- `aliases`: Alternative names, acronyms
- `source_papers`: Papers that mention this concept
- `related_to`: Related concept IDs
- `components`: Sub-concept IDs (for frameworks)

### Researchers (Contributors)
Authors and key figures in the research.

**Fields:**
- `id`: Unique identifier (usually lastname-initial)
- `name`: Full name
- `affiliation`: Institution
- `contributions`: Key contributions
- `key_papers`: Papers they authored
- `mentioned_in`: Papers that cite them

### Papers (Sources)
Research papers, both analyzed and cited.

**Fields:**
- `id`: Unique identifier (usually paper-slug)
- `title`: Full paper title
- `authors`: List of author names
- `year`: Publication year
- `type`: Paper type (see config.yaml)
- `key_concepts`: Main concepts from paper
- `cites`: Other papers this paper references
- `status`: analyzed | reading | to-read

## Relationships

- `extends`: Concept A extends concept B
- `builds-on`: Research builds on prior work
- `challenges`: Concept/paper challenges another
- `integrates-with`: Concepts work together
- `requires`: Concept requires another
- `enables`: Concept enables another
- `popularized`: Researcher popularized concept
- `theorized`: Researcher theorized concept

## Workflow

### 1. Analyze Paper
Extract concepts, researchers, and relationships during systematic analysis.

### 2. Add to Graph
```python
from core.graph_manager import GraphManager

gm = GraphManager('config.yaml')

# Add concept
gm.add_entity('primary', {
    'id': 'design-thinking',
    'label': 'Design Thinking',
    'type': 'methodology',
    'description': 'User-centered, iterative innovation process',
    'aliases': ['DT', 'design thinking process'],
    'source_papers': ['paper-001'],
    'related_to': ['human-centered-design']
})

# Add paper
gm.add_entity('sources', {
    'id': 'paper-001',
    'title': 'Design Thinking in Practice',
    'authors': ['Smith, J.', 'Jones, M.'],
    'year': 2024,
    'type': 'empirical-study',
    'key_concepts': ['design-thinking', 'innovation'],
    'status': 'analyzed'
})

# Add relationship
gm.add_relationship('design-thinking', 'human-centered-design', 'relates-to')

gm.save()
```

### 3. Visualize
```powershell
python server.py
```
Opens interactive viewer at http://localhost:8000

## Integration with Paper Analysis

If using SPEC framework or similar systematic analysis:

1. **Phase 5 (Contribution)**: Extract concepts and add to graph
2. **Phase 7 (Citations)**: Add cited papers as "to-read"
3. **Phase 8 (Integration)**: Update relationships and cross-references

## Gemini AI Integration (Optional)

To enable AI chat with graph context:

1. Create `gemini_config.json`:
```json
{
  "api_key": "your-gemini-api-key",
  "model": "gemini-2.0-flash-exp"
}
```

2. Update `config.yaml`:
```yaml
gemini_context:
  enabled: true
```

3. AI will have access to:
   - All concepts and relationships
   - Paper metadata
   - Researcher information
   - Can help find connections and gaps

## Tips

- Use consistent ID format: `lowercase-with-hyphens`
- Always track provenance via `source_papers`
- Mark cited papers as "to-read" for reading pipeline
- Update `source_papers` when concept appears in new paper
- Use `related_to` for informal connections, `relationships` for formal ones

## Example: Literature Review Workflow

```powershell
# 1. Initialize graph
python init.py

# 2. Analyze first paper → extract entities → add to graph
# 3. Analyze second paper → merge with existing graph
# 4. Continue for all papers

# 5. Explore accumulated knowledge
python server.py

# 6. Use viewer to:
#    - Identify concept clusters
#    - Find bridging concepts
#    - Spot research gaps
#    - Trace concept evolution
#    - Build theoretical framework
```

