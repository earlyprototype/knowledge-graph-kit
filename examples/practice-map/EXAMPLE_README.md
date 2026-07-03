# Practice Map: earlyprototype's Public Project Ecosystem

This is a **meta-example** showing how to use the Ecosystem Mapping template to
map a real portfolio — in this case, the public GitHub projects and practice
areas of `earlyprototype`, the author of this kit.

## What's Mapped

### Elements (15 total)

**Practice-area hubs (3)** — modelled as `process` elements:
- Service design
- AI systems
- Research & play

**Public projects (12)** — modelled as `technology` elements, each a real
public repository:
- `knowledge-graph-kit` — this kit
- `FabLatticeGPT`
- `wargame` ("FALSE FLAG")
- `kanbanger`
- `thought_bubble`
- NotebookLM MCP servers
- `hunch_kit`
- `early-prototype` (Claude Code plugin marketplace)
- `lia-workflow-specs`
- `meTube`
- `plasticFlowers`
- `lucier-gpt2-activ-tensor-reson-experiments` ("Activation Tensor Resonance")

### Relationships (19)

- **`enables`** (17) — each project links to the practice area(s) it builds
  out
- **`influences`** (1) — `thought_bubble` visualises Activation Tensor
  Resonance's experiments as an interactive mind-map
- **`regulates`** (1) — `kanbanger` governs how `early-prototype` (plugin
  marketplace) tasks move through review

### Stakeholders / Insights

None populated in this instance — the Ecosystem template supports them
(interviews, reports, individual contributors), but this map only needed the
`elements` + `relationships` layer to show how the author's projects relate to
their practice areas.

## How to Use This Example

### 1. Build the Map

```bash
cd examples/practice-map
python build_practice_map.py
```

This regenerates `_data/entities.json` and `_data/visual_config.json` from
`config.yaml`.

### 2. View the Map

```bash
python server.py
```

Then open: **http://localhost:8000/viewer.html**

### 3. Explore

- **Click a practice-area hub** (e.g. "AI systems") — see every project that
  builds it out
- **Click a project node** — read its description and see which practice
  areas it feeds
- **Search** for a project or practice area by name

## Visualization

This instance uses a restrained, non-default palette (set in `config.yaml`
under `visualization`):

- **Deep teal** (`#0F5257`), size 38 — practice-area hubs (`process`)
- **Steel blue** (`#5B7DB1`), size 24 — projects (`technology`)
- Physics tuned for a calmer, less bouncy layout (`gravitationalConstant:
  -8000`, `springLength: 220`, `damping: 0.12`)

`GraphManager.save()` exports these settings to `_data/visual_config.json`,
which `viewer.html` fetches at load time and overlays on its built-in
defaults — so changes to `config.yaml`'s `visualization` block take effect
without touching the viewer itself.

## What This Demonstrates

- **Ecosystem Mapping applied to a personal practice** — not a company or
  research field, but one person's portfolio of public tools
- **Config-driven visual identity** — a knowledge graph that looks
  intentional (a specific palette and layout) rather than using template
  defaults
- **A real, small graph** — 15 elements and 19 relationships is enough to be
  genuinely explorable without being overwhelming

## Key Takeaways

**Start small** — this map covers 12 projects and 3 practice areas. That's a
deliberately narrow, curated slice, not an attempt to catalogue everything.

**Public data only** — every project element here corresponds to a public
GitHub repository. This map is designed to be shown publicly (it backs the
kit's own [live demo](../../README.md)) and deliberately excludes anything
private.

**Use it as a template** — swap in your own practice areas and public
projects to map your own portfolio the same way.
