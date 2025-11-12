# Knowledge Graph Kit

Build, visualize, and explore knowledge graphs with an interactive web interface. Perfect for research synthesis, systems mapping, or stakeholder analysis.

<div align="center">

![Knowledge Graph Kit](img/top.png)

</div>

<div align="center">

![Python](https://img.shields.io/badge/python-3.7+-blue.svg)
![License](https://img.shields.io/badge/license-MIT-green.svg)

[Quick Start](#quick-start) • [Templates](#templates) • [Documentation](#documentation)

</div>

---

## Features

- **🎯 4 Pre-built Templates** - Research, Systems Mapping, Ecosystem Mapping, Generic
- **🎨 Interactive Visualization** - Click, explore, and navigate your knowledge graph
- **🤖 AI Integration** - Optional Gemini chat for insights and exploration
- **📊 Provenance Tracking** - Track where each concept came from
- **🔧 Fully Configurable** - Customize entity types, relationships, and visuals via YAML
- **💻 Simple Setup** - Interactive wizard walks you through everything

---

## Quick Start

### Interactive Setup (Recommended)

```bash
cd knowledge-graph-kit
python setup_wizard.py
```

The wizard will:
1. Help you choose a template
2. Configure AI integration (optional)
3. Set up your project
4. Launch the viewer

**Takes 2-5 minutes.**

### Manual Setup

```bash
# 1. Choose and copy a template
cp -r templates/research ./my-project

# 2. Install dependencies
pip install -r requirements.txt

# 3. Initialize
cd my-project
python init.py

# 4. Start the server
python server.py  # Basic
# or
python start_server.py  # With AI chat
```

Open http://localhost:8000 in your browser.

---

## Templates

Choose the template that fits your use case:

### 🎓 Research
**For:** Academic papers, literature reviews, systematic analysis

**Entities:** Concepts, Researchers, Papers  
**Use Cases:** Literature synthesis, concept mapping, citation networks

### 🏗️ Systems Mapping
**For:** Systems thinking, complex systems analysis, organizational systems

**Entities:** Components, Teams, Specifications  
**Use Cases:** Systems thinking, dependency mapping, impact analysis, systems documentation

### 🌐 Ecosystem Mapping
**For:** Stakeholder analysis, value flows, organizational networks

**Entities:** Elements, Stakeholders, Insights  
**Use Cases:** Ecosystem analysis, power mapping, value chain visualization

### ⚙️ Generic
**For:** Custom domains not covered above

**Entities:** Fully customizable  
**Use Cases:** Anything else - you define the schema

[See full template comparison →](TEMPLATES.md)

---

## Example Usage

```python
from core.graph_manager import GraphManager

# Initialize
gm = GraphManager('config.yaml')

# Add entities
gm.add_entity('primary', {
    'id': 'design-thinking',
    'label': 'Design Thinking',
    'type': 'methodology',
    'description': 'User-centered, iterative innovation process',
    'source_papers': ['paper-001']
})

# Add relationships
gm.add_relationship('design-thinking', 'human-centered-design', 'relates-to')

# Save
gm.save()
```

---

## Viewer Features

<div align="center">

| Feature | Description |
|---------|-------------|
| **Interactive Graph** | Drag, zoom, and explore nodes |
| **Smart Search** | Find entities by name or description |
| **Click-through Navigation** | Navigate between related entities |
| **Show Connections** | Focus on subgraphs |
| **Breadcrumb Trail** | Track your exploration path |
| **Document Panel** | View source documents inline |
| **AI Chat** | Ask questions about your graph (optional) |

</div>

---

## Project Structure

```
your-project/
├── config.yaml              # Configuration
├── data/
│   └── entities.json        # Your knowledge graph
├── viewer.html              # Interactive visualization
├── server.py                # HTTP server
└── README.md                # Template docs
```

---

## Configuration

All templates use YAML configuration:

```yaml
domain: research

entity_types:
  primary:
    name: concepts
    types: [methodology, framework, technology]
  
  contributors:
    name: researchers
  
  sources:
    name: papers

relationships:
  types: [extends, builds-on, challenges]

visualization:
  colors:
    methodology: "#3498db"
    framework: "#9b59b6"
```

[See full configuration guide →](docs/CONFIGURATION.md)

---

## AI Integration (Optional)

Enable Gemini AI chat for:
- Asking questions about your graph
- Finding patterns and connections
- Getting synthesis insights

**Setup:**
1. Get API key from [Google AI Studio](https://makersuite.google.com/app/apikey)
2. Run setup wizard and choose "Enable Gemini"
3. Or manually: copy `gemini_config.template.json` to `gemini_config.json` and add your key

---

## Documentation

- **[Template Comparison](TEMPLATES.md)** - Detailed comparison of all templates
- **[Examples](examples/)** - Code examples for common tasks
- **Template READMEs** - In each template directory

---

## Requirements

- Python 3.7+
- PyYAML
- google-generativeai (for AI features)

```bash
pip install -r requirements.txt
```

---

## Use Cases

### Academic Research
- Build cumulative knowledge from papers
- Track concept evolution across sources
- Identify research gaps
- Generate literature reviews

### Systems Mapping & Thinking
- Map system dependencies and relationships
- Understand complex systems and feedback loops
- Analyze system dynamics and interactions
- Track ownership and specifications

### Ecosystem Analysis
- Map stakeholder relationships
- Analyze power structures
- Trace value flows
- Identify collaboration opportunities

---

## Contributing

Contributions welcome! Please feel free to submit a Pull Request.

---

## License

MIT License - see [LICENSE](LICENSE) for details.

---

## Acknowledgements

Built for researchers, architects, and analysts who need to understand complex, interconnected systems.

