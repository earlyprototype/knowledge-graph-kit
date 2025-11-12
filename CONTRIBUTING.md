# Contributing to Knowledge Graph Kit

Thank you for considering contributing! This project aims to make knowledge graph creation accessible and useful for researchers, architects, and analysts.

## How to Contribute

### Reporting Issues

**Bug Reports**
- Use a clear, descriptive title
- Describe the expected vs actual behaviour
- Include steps to reproduce
- Mention your Python version and OS
- Include relevant config files (remove sensitive data like API keys)

**Feature Requests**
- Explain the use case
- Describe the desired behaviour
- Provide examples if possible

### Code Contributions

1. **Fork the repository**

2. **Create a feature branch**
   ```bash
   git checkout -b feature/your-feature-name
   ```

3. **Make your changes**
   - Follow existing code style
   - Add comments for complex logic
   - Update documentation if needed

4. **Test your changes**
   - Test with all templates
   - Verify the wizard still works
   - Check the viewer loads correctly

5. **Commit with clear messages**
   ```bash
   git commit -m "Add: feature description"
   git commit -m "Fix: bug description"
   git commit -m "Update: documentation description"
   ```

6. **Push and create a Pull Request**

## Development Setup

```bash
# Clone your fork
git clone https://github.com/yourusername/knowledge-graph-kit.git
cd knowledge-graph-kit

# Install dependencies
pip install -r requirements.txt

# Test the wizard
python setup_wizard.py

# Test a template
cp -r templates/research ./test-project
cd test-project
python init.py
python server.py
```

## Areas for Contribution

### High Priority
- **New Templates** - Add templates for other domains
- **Export Formats** - Add export to Neo4j, GraphML, etc.
- **Performance** - Optimize for larger graphs (1000+ nodes)
- **Testing** - Add unit tests for core modules

### Good First Issues
- **Documentation** - Improve README, add tutorials
- **Examples** - Add example graphs for each template
- **Bug Fixes** - Check issues labeled "good first issue"
- **UI Improvements** - Enhance viewer interface

### Advanced Contributions
- **Alternative Visualizations** - Add timeline, matrix, or hierarchical views
- **Database Backend** - Add Neo4j or ArangoDB support
- **Collaboration Features** - Multi-user editing
- **Advanced Analytics** - Add graph metrics and analysis

## Code Style

- Follow PEP 8 for Python code
- Use descriptive variable names
- Add docstrings to functions
- Keep functions focused and small
- Use type hints where helpful

## Documentation

When adding features:
- Update relevant template READMEs
- Add examples to main README if widely applicable
- Document configuration options
- Update TEMPLATES.md for template changes

## Testing

Before submitting:
- Test wizard with all templates
- Verify viewer loads and displays correctly
- Test entity adding and relationship creation
- Check Gemini integration works (if applicable)
- Ensure server starts without errors

## Questions?

Open an issue with the "question" label or start a discussion.

## License

By contributing, you agree your contributions will be licensed under the MIT License.

---

Thank you for helping make knowledge graphs more accessible!

