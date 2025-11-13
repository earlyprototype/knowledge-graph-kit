# Systems Mapping Example: Knowledge Graph Kit

This is a **meta-example** showing how to use the Systems Mapping template to document a software project - in this case, the Knowledge Graph Kit itself!

## What's Mapped

This systems map documents the Knowledge Graph Kit codebase structure, including:

### Components (21 total)
- **Core Modules**: Graph Manager, Config Loader
- **Services**: HTTP Server, Gemini API Server
- **Tools**: Setup Wizard, Initialization Scripts
- **Templates**: Research, Systems, Ecosystem, Generic
- **UI**: Web Viewer Interface
- **Data Stores**: entities.json, config.yaml
- **External Dependencies**: PyYAML, Google Gen AI, vis.js

### Relationships
- **Dependencies**: Which components depend on others
- **Data Flow**: Where data is read/written
- **Integration**: How components work together
- **Ownership**: Team responsibility
- **Documentation**: What's documented where

### Documentation
- Main README
- Template documentation
- Specific template READMEs

## How to Use This Example

### 1. Build the Map

```bash
cd examples/systems-map-example
python build_map.py
```

This will:
- Create the `data/` directory
- Generate `entities.json` with the complete systems map
- Output statistics about the graph

### 2. View the Map

```bash
python server.py
```

Then open: **http://localhost:8000/viewer.html**

(The server should auto-open this in your browser)

### 3. Explore the System

Try these interactions:
- **Click on "Graph Manager"** - see its dependencies (Config Loader, PyYAML)
- **Click on "Setup Wizard"** - see how it connects to all templates
- **Click on "HTTP Server"** - see the data flow to the viewer
- **Search for "template"** - find all template subsystems
- **Click on "Development Team"** - see all owned components

### 4. Optional: Enable AI Chat

If you want to ask questions about the system:

1. Copy `gemini_config.template.json` to `gemini_config.json`
2. Add your Gemini API key
3. Run: `python start_server.py`
4. Open: **http://localhost:8000/viewer.html**
5. Ask questions like:
   - "What depends on the Graph Manager?"
   - "Show me the data flow in this system"
   - "What are the external dependencies?"
   - "Which components are owned by the dev team?"

## What This Demonstrates

### For Software Projects
This example shows how to use Systems Mapping for:
- **Dependency tracking** - understand what depends on what
- **Architecture documentation** - visual system overview
- **Impact analysis** - see what's affected by changes
- **Onboarding** - help new developers understand the system
- **Technical debt tracking** - identify deprecated components

### Systems Thinking Concepts
- **Components** as system elements
- **Relationships** showing connections and flows
- **Subsystems** (templates) as modular units
- **External dependencies** as boundary elements
- **Teams** showing responsibility structure

## Extending This Example

### Add More Detail
```python
# Add more granular components
gm.add_entity('primary', {
    'id': 'yaml-validator',
    'label': 'YAML Validator',
    'type': 'module',
    'description': 'Validates YAML configuration schema',
    # ...
})
```

### Track Version History
```python
# Add version information
gm.add_entity('primary', {
    'id': 'graph-manager',
    'version': '1.1',  # Updated version
    'status': 'active',
    # ...
})
```

### Add API Documentation
```python
# Document APIs
gm.add_entity('sources', {
    'id': 'api-spec-graph-manager',
    'title': 'Graph Manager API Specification',
    'type': 'specification',
    # ...
})
```

### Map Git History
You could extend this to track:
- Commit frequency per component
- Contributors per component
- Change patterns and hotspots

## Real-World Applications

Use this approach for:

1. **Microservices Architecture**
   - Map service dependencies
   - Track API contracts
   - Ownership per team

2. **Monolith Refactoring**
   - Document current state
   - Plan extraction strategy
   - Track migration progress

3. **Open Source Projects**
   - Help contributors understand structure
   - Document subsystem ownership
   - Track deprecated features

4. **System Integration**
   - Map data flows between systems
   - Track external dependencies
   - Document integration points

## Key Takeaways

✅ **Start Simple** - This example has 21 components. Start with 5-10 key ones.

✅ **Iterate** - Add detail as you discover dependencies

✅ **Keep Updated** - Run the build script after major changes

✅ **Use It** - Reference the map during planning and design discussions

✅ **Extend It** - Add custom attributes relevant to your domain

---

**This example was automatically generated to demonstrate the Systems Mapping template. It represents a snapshot of the Knowledge Graph Kit codebase structure.**

