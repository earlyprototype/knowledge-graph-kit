# Evidence Template

Knowledge graph optimized for mapping **research evidence**: claims whose status
changes over time, connected by signed epistemic edges.

Where the `research` template maps what a literature says, this template maps what
you currently believe, why, and when that changed. A claim is not a static node - it
is asserted on a date, tested by runs, supported or refuted by results, sometimes
qualified, corrected, superseded or retired. The graph keeps that history so it can
be replayed.

## Entities

### Claims (Primary)
Hypotheses, findings, concepts and questions - the things that can be true, false, or
not yet known.

**Types:**
- `hypothesis` - a claim you intend to test
- `finding` - a claim a run has produced
- `concept` - a construct the other claims are stated in terms of
- `question` - something the record explicitly leaves open

The four are not interchangeable, and the boundary that matters most in practice is
`question` vs the other two active types:

| Type | Asserts something? | Answer expected from | Typical status |
|---|---|---|---|
| `hypothesis` | Yes - a testable proposition | a run that tests it | `untested` -> `supported` / `refuted` / ... |
| `finding` | Yes - a result already in hand | already answered | `supported`, `qualified`, `corrected` |
| `concept` | No - it is vocabulary | nothing; it is not a question | `open` (i.e. no epistemic status) |
| `question` | No - it *asks* | new work, named by `blocks` / `blocked-by` | `open` while it stands |

A question is not a hypothesis with a question mark on it. "Does the landscape depend
on where the loop is cut?" is a question; "the landscape does not depend on where the
loop is cut" is a hypothesis. If you can state a verdict that would settle it, and you
have committed to a direction, it is a hypothesis. If the record only says the matter
is unsettled, pending, blocked or not attempted, it is a question.

Only emit a question the source actually leaves open, and quote the sentence that
leaves it open in the `description`. A question node you invented is worse than no
question node: it makes fabricated work look like recorded work.

**Fields:**
- `id`: Unique identifier, kebab-case (e.g. `f9-divine-period-2`, `h-fingerprint`, `concept-limit-cycle`, `q-gate-cadence`)
- `label`: Short display name (e.g. `F9: Divine is a period-2 limit cycle`)
- `type`: hypothesis | finding | concept | question
- `status`: Where the claim stands now (see below)
- `description`: 1-3 sentences of plain prose
- `phase`: Phase id from `metadata.phases` (e.g. `phase-5`)
- `asserted`: ISO date the claim was first made - optional but strongly preferred
- `retired`: ISO date the claim stopped standing, or `null`
- `doc_ref`: Repo-relative path + anchor (e.g. `docs/FINDINGS.md#f9-divine-period-2`)
- `evidence`: Array of run ids bearing on the claim

### Runs (Contributors)
The experiments and models that generate evidence.

**Types:** `run` | `model` | `null-model`

**Fields:**
- `id`: Unique identifier (e.g. `run-05-gated-resweep`, `model-gpt2-small`)
- `label`: Display name
- `type`: run | model | null-model
- `description`: What the run did / what the model is
- `script`: Repo-relative path to the notebook or script (runs only)
- `output_dir`: Repo-relative path to the run's outputs (runs only)
- `n`: Sample description (e.g. `125 prompts, <=1000 iters`)
- `date`: ISO date the run happened

A `null-model` is a deliberate control - the thing that must *fail* for a claim to
mean anything. Keep it in the graph; a refutation by a null model is a result.

### Sources (Sources)
Docs, artefacts and prior work - where the evidence is written down.

**Types:** `doc` | `artefact` | `prior-work`

**Fields:**
- `id`: Unique identifier (e.g. `doc-findings`, `art-convergence-matrix-small`, `prior-radford-2019`)
- `title`: Display title
- `type`: doc | artefact | prior-work
- `path`: Repo-relative path or URL
- `description`: Optional one-liner

## Status vocabulary

Every claim carries exactly one status. These are the canonical values and colours -
use these exact hex values everywhere (they are also in `config.yaml` under
`visualization.status_colors`):

| Status          | Colour    | Means                                                                |
|-----------------|-----------|----------------------------------------------------------------------|
| `supported`     | `#2E7D5B` | Evidence stands behind it and nothing has knocked it down.            |
| `refuted`       | `#B3423F` | A run showed it to be false. The claim stays in the graph.            |
| `not-supported` | `#8F5A57` | Null result - evidence failed to back it, without contradicting it.   |
| `qualified`     | `#B9812F` | True, but only under conditions the original statement did not carry. |
| `retired`       | `#8A8F94` | No longer in play - question dissolved, or scope moved on.            |
| `corrected`     | `#5B7DB1` | The claim was wrong in detail and has been restated correctly.        |
| `open`          | `#6B4C8A` | Being actively worked; evidence exists but is not decisive.           |
| `untested`      | `#9AA3A8` | Stated, never yet put to a run.                                       |

### Status by claim type

The eight values are shared, but each type uses a slice of them, and `open` means
different things on either side of the `question` line:

| Type | Statuses it uses | Note |
|---|---|---|
| `hypothesis` | `untested`, `supported`, `refuted`, `not-supported`, `qualified`, `corrected`, `retired` | Moves as evidence lands. |
| `finding` | `supported`, `qualified`, `corrected`, `retired`, `refuted` | A finding starts life supported by its own run. |
| `concept` | `open` (default), `corrected`, `retired`, `untested` | `open` on a concept is *no epistemic status*, not open work. |
| `question` | `open`, `untested`, `retired` | `open` on a question is real open work. |

This is the point of the `question` type. Before it existed, `open` was the default a
concept fell into when nobody had an epistemic verdict to record, so filtering the
graph to `status = open` returned a pile of vocabulary and no work. `type = question
AND status = open` is the query that returns work; `open` finally means something for a
claim that is not a concept.

**A question that has been answered is not given an "answered" status.** It takes
`retired` plus a `retired` date, and the *answer* arrives as an edge: the finding (or
hypothesis) that settled it draws `retires` - or `supersedes`, if it replaces the
question with a sharper one - at the question. That way the answer is a first-class
node you can follow, and the question keeps its place on the timeline: scrub back to
before the answer and it is open again. A status value meaning "answered" would throw
away which result did the answering.

`untested` on a question is the narrow case where a protocol exists and nobody has run
it. If there is no protocol, the question is simply `open`.

`not-supported` is the null-result slot, and it is deliberately narrow: `refuted` means
the evidence points the other way, `qualified` means the claim survives in a narrowed or
mixed form, and `not-supported` means neither happened - the run simply failed to back
the claim. Use it when a disposition reads "not supported at pilot confidence"; do not
launder a null result into `qualified`, which would put it in the same bucket as genuine
partial support.

Falsified claims are never deleted. Deleting a refuted claim erases the evidence
that refuted it, and next year someone re-asserts it.

## Epistemic edge vocabulary

Edges are grouped by whether they carry epistemic force.

### Epistemic (signed - these change what you believe)
| Edge         | Style                    | Use for                                                     |
|--------------|--------------------------|-------------------------------------------------------------|
| `supports`   | solid `#2E7D5B`, arrow   | Run/finding raises confidence in the target claim.          |
| `refutes`    | dashed `#B3423F`, arrow  | Run/finding shows the target claim is false.                |
| `qualifies`  | dashed `#B9812F`, arrow  | Narrows the target's scope without killing it.              |
| `corrects`   | dotted `#5B7DB1`, arrow  | Fixes a wrong detail in the target.                         |
| `retires`    | dotted `#8A8F94`, arrow  | Takes the target out of play.                               |
| `supersedes` | dotted `#5B7DB1`, arrow  | A newer claim replaces an older one wholesale.              |
| `tests`      | solid `#6B4C8A`, arrow   | A run addresses a claim - direction of result not yet given.|

### Structural (neutral plumbing)
`produced-by`, `run-on`, `evidenced-by`, `documented-in` - thin solid `#C7CDD1`,
arrow. These connect claims to the runs, models, artefacts and docs behind them.
They say *where it came from*, not *whether it is true*.

### Associative (soft links)
- `analogous-to`, `breaks-down-at` - dashed `#5B7DB1`, no arrow (symmetric)
- `builds-on`, `cites`, `relates-to` - thin solid `#B0B7BC`, arrow
- `blocks`, `blocked-by` - dashed `#A8477A`, arrow (dependency between open work)

| Edge         | Direction                  | Use for                                                       |
|--------------|----------------------------|---------------------------------------------------------------|
| `blocks`     | blocker -> gated thing     | "no cross-model coherence claim until a matched null exists"  |
| `blocked-by` | gated thing -> blocker     | "the other 33 prompts remain blocked on the prompt library"   |

These two are the same relation read from opposite ends. Draw **one** edge per pair,
in whichever direction the source states it, and quote the source in the description -
drawing both directions doubles the graph's dependency count and makes a single stated
blocker look like two.

`blocks` / `blocked-by` are deliberately associative, not epistemic: a blocker changes
nothing about whether a claim is true, only about whether it can be settled yet. They
are what makes a shared blocker visible - two questions pointing `blocked-by` at the
same artefact are one unblocking away from both moving, which is invisible when the
same sentence is merely repeated in two prose descriptions.

Every relationship needs a real `description` saying **why** it holds. `weight`
(1-10, default 3) drives edge thickness where the viewer supports it, and `asserted`
(ISO date) drives the timeline scrubber.

## Timeline fields

The graph is replayable because three things carry dates:

- `claims[].asserted` - when the claim entered the graph
- `claims[].retired` - when it left (or `null` if it still stands)
- `relationships[].asserted` - when the edge was drawn, i.e. when the evidence landed

Plus `metadata.phases`, an ordered list of chapters used to label the scrubber:

```json
"phases": [
  {"id": "phase-0", "label": "Phase 0: Inspiration", "start": "2026-03-01"},
  {"id": "phase-5", "label": "Phase 5: Gated re-sweep", "start": "2026-06-14"}
]
```

Each claim's `phase` points at one of these ids. Setting the scrubber to a date
means: show only claims asserted on or before that date and not yet retired, and only
edges asserted on or before it. That reconstructs what you believed then, rather than
what you believe now.

## Node shapes

`hypothesis` diamond, `finding` dot, `concept` hexagon, `question` circle, `run`
square, `model` triangle, `null-model` triangleDown, `doc` box, `artefact` ellipse,
`prior-work` star. Also in `config.yaml` under `visualization.node_shapes`.

`question` is a `circle` (label drawn inside) rather than a `dot` (label drawn
alongside), so an open question does not read as another finding at a glance. Its
type colour is `#A8477A`.

## Workflow

### 1. Initialize
```powershell
python init.py
```
Creates `_data/entities.json`, `_data/visual_config.json`, `docs/` and `output/`.

### 2. State the hypothesis before you run anything
```python
from core.graph_manager import GraphManager

gm = GraphManager('config.yaml')

gm.add_entity('primary', {
    'id': 'h-fingerprint',
    'label': 'H: Each model has a stable convergence fingerprint',
    'type': 'hypothesis',
    'status': 'untested',
    'description': 'Iterated self-prompting converges to a signature attractor '
                   'that is stable across seeds for a given model.',
    'phase': 'phase-0',
    'asserted': '2026-03-01',
    'retired': None
})
gm.save()
```

### 3. Record the run, then the result
```python
gm.add_entity('contributors', {
    'id': 'run-05-gated-resweep',
    'label': 'Run 05: gated re-sweep',
    'type': 'run',
    'description': 'Re-runs the full prompt set with the convergence gate enabled.',
    'script': 'notebooks/05_gated_resweep.ipynb',
    'output_dir': 'output/run-05',
    'n': '125 prompts, <=1000 iters',
    'date': '2026-06-14'
})

gm.add_entity('sources', {
    'id': 'art-convergence-matrix-small',
    'title': 'Convergence matrix (small models)',
    'type': 'artefact',
    'path': 'output/run-05/convergence_matrix_small.png',
    'description': 'Per-model convergence rates from run 05.'
})

gm.add_entity('primary', {
    'id': 'f9-divine-period-2',
    'label': 'F9: Divine is a period-2 limit cycle',
    'type': 'finding',
    'status': 'supported',
    'description': 'The "divine" attractor is not a fixed point; it alternates '
                   'between two states with period 2.',
    'phase': 'phase-5',
    'asserted': '2026-06-14',
    'retired': None,
    'doc_ref': 'docs/FINDINGS.md#f9-divine-period-2',
    'evidence': ['run-05-gated-resweep']
})
```

### 4. Wire it up - every edge says why
```python
gm.add_relationship('run-05-gated-resweep', 'h-fingerprint', 'tests',
    'Run 05 sweeps all 5 models over the same prompt set to see whether '
    'each model lands on a consistent attractor.')

gm.add_relationship('f9-divine-period-2', 'h-fingerprint', 'qualifies',
    'The fingerprint is stable, but it is a 2-cycle rather than a fixed point, '
    'so "signature attractor" needs restating as "signature orbit".')

gm.add_relationship('f9-divine-period-2', 'run-05-gated-resweep', 'produced-by',
    'F9 was read off the gated re-sweep convergence traces.')

gm.add_relationship('f9-divine-period-2', 'art-convergence-matrix-small', 'evidenced-by',
    'The period-2 alternation is visible in the small-model convergence matrix.')

gm.update_entity('primary', 'h-fingerprint', {'status': 'qualified'})
gm.save()
```

### 4b. Record what the run left open

A run almost always closes one thing and leaves another. Do not let that second half
live only in a sentence inside a finding's `description`, where nothing can find it.

```python
gm.add_entity('primary', {
    'id': 'q-other-33-prompts',
    'label': 'Q: Do the other 33 Divine prompts share the flip axis?',
    'type': 'question',
    'status': 'open',
    'description': 'FINDINGS F10 leaves this open in as many words: "Open: whether '
                   'all 34 Divine prompts share this flip axis (blocked on the '
                   'prompt-library restoration, issue #9)."',
    'phase': 'phase-5',
    'asserted': '2026-07-19',
    'retired': None,
    'doc_ref': 'docs/FINDINGS.md#f10-anatomy-of-the-period-2-cycle'
})

gm.add_relationship('q-other-33-prompts', 'q-prompt-library', 'blocked-by',
    'F10 states the block in the source\'s own words: "blocked on the '
    'prompt-library restoration, issue #9".')

gm.add_relationship('q-other-33-prompts', 'f10-cycle-anatomy', 'relates-to',
    'The question is raised by F10 and is about the axis F10 measured.')
```

Three rules keep this honest:

1. The `description` carries the quote that leaves it open. If you cannot quote it,
   the record does not leave it open and there is no node to add.
2. `doc_ref` points at the passage the quote came from.
3. It is wired to something: `relates-to` the claim it came out of, and
   `blocks` / `blocked-by` whatever it gates or is gated by. A question with no
   edges is a note, not a graph node.

When the question is answered, do not edit the question's text. Add the finding, draw
`retires` from the finding to the question, and set the question's `status` to
`retired` with a date. The question keeps saying what was asked; the edge says what
answered it.

Note the pattern: the finding **qualifies** the hypothesis, and the hypothesis'
`status` moves `untested -> qualified`. The edge records the event; the status records
the current state. Both are needed - the edge alone cannot be read at a glance, and
the status alone loses the history.

### 5. Visualize
```powershell
python server.py
```
Opens the interactive viewer at http://localhost:8000/viewer.html

For the viewer plus the Gemini chat assistant:
```powershell
python start_server.py
```

#### Viewer controls

On a wide screen everything is on the surface: search, the *Colour by* selector,
*Show All* / *Reset View* / *Refresh Data* / *Chat with AI*, the status and type
chip rows, the breadcrumb, the legend over the canvas, and the timeline scrubber
pinned to the bottom.

Below 769px (phones) the same controls are still all there, just folded up so the
graph gets the screen:

| Control | Where it goes |
|---|---|
| Search | stays in the header |
| Status + type chips | behind the **Filters** button; the panel overlays the graph |
| Legend | behind the **Legend** button; overlays the graph, closed by default |
| Colour by, Show All, Reset View, Refresh Data, Chat with AI | behind the **⋮** overflow button |
| Breadcrumb | hidden until you have actually walked a path |
| Node details | a bottom sheet with its own scroll and a close (×) button |
| Timeline | still pinned to the bottom, compacted to the play button, scrubber and date |

The **Filters** button reads `Filters (12 of 17)` whenever any chip is off, so a
shut panel can never be the unexplained reason nodes are missing. One overlay is
open at a time; `Esc`, a tap on bare canvas, or opening a node closes them. All
three toggles are real buttons with `aria-expanded`, so they work from the
keyboard.

## Worked example: how a claim moves

```
2026-03-01  h-fingerprint            untested   (stated, no runs yet)
2026-04-02  run-02-baseline  --tests-->        h-fingerprint  ->  open
2026-05-10  f4-seed-variance --supports-->     h-fingerprint  ->  supported
2026-06-14  f9-divine-period-2 --qualifies-->  h-fingerprint  ->  qualified
2026-07-01  null-shuffled-prompts --refutes--> f4-seed-variance -> refuted
                                    ...which leaves h-fingerprint qualified,
                                    now resting on F9 alone.
```

Drag the scrubber to 2026-05-11 and the graph shows a green `supported` hypothesis
with one supporting finding. Drag it to today and the same hypothesis is amber, its
original support struck through by a null model. Nothing was deleted; the picture
changed because the dates changed.

## Gemini AI Integration (Optional)

To enable AI chat with graph context:

1. Copy `gemini_config.template.json` to `gemini_config.json` and add your API key
   from https://makersuite.google.com/app/apikey (the file is git-ignored).

2. Update `config.yaml`:
```yaml
gemini_context:
  enabled: true
```

3. Run `python start_server.py`. The assistant gets:
   - The whole evidence graph (claims, runs, sources, relationships)
   - Per-claim context: the claim record, its edges, its runs, and the file its
     `doc_ref` points at
   - Instructions to cite run ids and doc_refs, to respect edge direction, and to
     say "not recorded in the graph" rather than guess

## Tips

- Use consistent ID format: `lowercase-with-hyphens`. Prefixes help: `h-` hypothesis,
  `f9-` numbered finding, `concept-`, `q-` question, `run-`, `model-`, `null-`, `doc-`,
  `art-`, `prior-`.
- Filter `type = question AND status = open` to get the work queue. Filtering on
  `status = open` alone will hand you every concept that never got a verdict.
- Never invent a question to fill a gap you noticed. Extract questions the way you
  extract findings: from the text, with the sentence quoted. A graph of real answers
  and imagined questions is worse than one with no questions in it.
- Set `asserted` on every claim and every epistemic edge, or the timeline is dead.
- Never delete a refuted claim - set `status: refuted` and draw the `refutes` edge.
- Use `retires` + `retired` date for questions that dissolved; use `supersedes` when a
  newer claim replaces an older one wholesale.
- `tests` before you know the answer; `supports` / `refutes` once you do. Keeping both
  edges shows what was attempted, not just what worked.
- Point `doc_ref` at a real anchor in a real file. If it does not resolve, the claim
  is not traceable and should not be marked supported.
- Prefer many small claims over one big one - a claim that can only be half-refuted is
  two claims.
