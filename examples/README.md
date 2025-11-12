# Knowledge Graph Kit Examples

This directory contains practical examples demonstrating how to use the Knowledge Graph Kit.

## Available Examples

### 📊 Systems Mapping Example: Knowledge Graph Kit

**Location:** `systems-map-example/`

A meta-example that uses the Systems Mapping template to document the Knowledge Graph Kit codebase itself!

**What it demonstrates:**
- How to map a software project's architecture
- Component dependencies and data flows
- Team ownership and documentation tracking
- Systems thinking applied to code

**Quick Start:**
```bash
cd systems-map-example
python build_map.py
python server.py
```

Then open http://localhost:8000

[View detailed documentation →](systems-map-example/EXAMPLE_README.md)

**Graph Statistics:**
- 20 Components (modules, services, templates, etc.)
- 39 Relationships (dependencies, data flows, ownership)
- 1 Team
- 3 Documentation sources

---

## Code Examples

### Basic Usage

Simple example showing core GraphManager usage:

**Location:** `basic_usage.py`

```bash
python examples/basic_usage.py
```

---

## Creating Your Own Examples

Want to contribute an example? Great! Here's what makes a good example:

### ✅ Good Examples Include:
- Clear purpose and use case
- Complete, runnable code
- Sample data or data generation script
- README explaining what it demonstrates
- Comments explaining key concepts

### 📝 Example Template Structure:
```
examples/
  your-example/
    ├── README.md              # What this demonstrates
    ├── build_map.py           # Data generation script
    ├── config.yaml            # Configuration
    ├── data/                  # Generated data
    │   └── entities.json
    └── viewer.html            # Viewer (if customized)
```

### 💡 Example Ideas:
- **Research Example**: Literature review of a specific field
- **Team Org Chart**: Company/team structure with projects
- **Product Roadmap**: Features and dependencies
- **Learning Path**: Course prerequisites and topics
- **Recipe Network**: Ingredients and cooking techniques
- **Movie/Book Universe**: Characters and relationships

---

## Learning Path

### 1. **Start with Basic Usage**
   - Run `python examples/basic_usage.py`
   - Understand the core API

### 2. **Explore the Systems Map Example**
   - See a complete, real-world graph
   - Understand component relationships

### 3. **Choose a Template**
   - Pick based on your use case
   - Read the template README

### 4. **Build Your Graph**
   - Start with 5-10 core entities
   - Add relationships
   - Iterate and expand

---

## Contributing Examples

We welcome example contributions! Please:

1. Fork the repository
2. Create your example in `examples/your-example/`
3. Include a clear README
4. Submit a pull request

Good examples help others learn - thank you for contributing!

