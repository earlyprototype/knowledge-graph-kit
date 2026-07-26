"""Tests for the evidence template's config.yaml, plus a regression guard that the
four pre-existing templates still load unchanged through core/.

The evidence template is the only template that adds `status_colors` and
`edge_styles` to the visualization block, so these tests pin both the vocabulary
contract (documented in TEMPLATES.md) and the completeness of the styling maps.
"""

import json
import math
import re
import shutil
import subprocess
import sys
from pathlib import Path

# Make the repo root importable regardless of how pytest is invoked
REPO_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(REPO_ROOT))

import pytest

from core.config_loader import GraphConfig, load_config
from core.graph_manager import GraphManager

TEMPLATES_DIR = REPO_ROOT / "templates"
EVIDENCE_CONFIG = TEMPLATES_DIR / "evidence" / "config.yaml"
EVIDENCE_VIEWER = TEMPLATES_DIR / "evidence" / "viewer.html"
EVIDENCE_README = TEMPLATES_DIR / "evidence" / "README.md"

HEX_RE = re.compile(r"^#[0-9A-Fa-f]{6}$")

# --- The contract, restated here on purpose -------------------------------
# These lists are the test's own copy of TEMPLATES.md "Evidence Template".
# If config.yaml changes, this file must be changed deliberately with it.

EXPECTED_CLAIM_TYPES = ["hypothesis", "finding", "concept", "question"]

# `question` is additive and goes last: the three original types keep their
# positions so an index-based reader cannot be silently re-pointed.
ORIGINAL_CLAIM_TYPES = ["hypothesis", "finding", "concept"]

QUESTION_COLOR = "#A8477A"
QUESTION_SHAPE = "circle"

# The statuses a `question` may carry. `open` is the whole point: it is the only
# claim type for which `open` is a work signal rather than the default a claim
# with no epistemic verdict falls into. There is deliberately no "answered"
# status - an answered question is `retired` and the answer is the claim on the
# other end of its incoming retires/supersedes edge.
QUESTION_STATUSES = {"open", "untested", "retired"}

# Ordered as a severity gradient. `not-supported` sits immediately after
# `refuted`: it is the null result (evidence failed to back the claim) and must
# not be conflated with a refutation or with `qualified` partial support.
EXPECTED_STATUSES = [
    "supported",
    "refuted",
    "not-supported",
    "qualified",
    "retired",
    "corrected",
    "open",
    "untested",
]

NOT_SUPPORTED_COLOR = "#8F5A57"

# Minimum CIE76 deltaE between the new status colour and every other swatch.
# Below roughly this, two swatches are confusable at a glance in the legend.
MIN_PERCEPTUAL_DISTANCE = 20.0

EXPECTED_RUN_TYPES = ["run", "model", "null-model"]

EXPECTED_SOURCE_TYPES = ["doc", "artefact", "prior-work"]

EPISTEMIC_EDGES = [
    "supports",
    "refutes",
    "qualifies",
    "corrects",
    "retires",
    "supersedes",
    "tests",
]
STRUCTURAL_EDGES = ["produced-by", "run-on", "evidenced-by", "documented-in"]
ASSOCIATIVE_EDGES = [
    "analogous-to",
    "breaks-down-at",
    "builds-on",
    "cites",
    "relates-to",
    # dependency between open work and what it gates. Associative, not
    # epistemic: a blocker changes whether a claim can be settled yet, never
    # whether it is true.
    "blocks",
    "blocked-by",
]
DEPENDENCY_EDGES = ["blocks", "blocked-by"]
DEPENDENCY_COLOR = "#A8477A"

# The five associative edges that existed before the dependency pair was added.
ORIGINAL_ASSOCIATIVE_EDGES = [
    "analogous-to",
    "breaks-down-at",
    "builds-on",
    "cites",
    "relates-to",
]
EXPECTED_EDGE_TYPES = EPISTEMIC_EDGES + STRUCTURAL_EDGES + ASSOCIATIVE_EDGES

# The four templates that existed before the evidence template was added.
PRE_EXISTING_TEMPLATES = {
    "research": {
        "domain": "research",
        "entity_names": {
            "primary": "concepts",
            "contributors": "researchers",
            "sources": "papers",
        },
        "relationships": [
            "integrates-with",
            "relates-to",
            "requires",
            "enables",
            "challenges",
            "extends",
            "applies-to",
            "popularized",
            "theorized",
            "builds-on",
            "depends-on",
            "implements",
        ],
    },
    "systems": {
        "domain": "systems",
        "entity_names": {
            "primary": "components",
            "contributors": "teams",
            "sources": "specifications",
        },
        "relationships": [
            "depends-on",
            "integrates-with",
            "calls",
            "consumes-data-from",
            "produces-data-for",
            "deployed-on",
            "monitored-by",
            "owned-by",
            "extends",
            "implements",
            "replaces",
            "communicates-with",
            "authenticated-by",
        ],
    },
    "ecosystem": {
        "domain": "ecosystem",
        "entity_names": {
            "primary": "elements",
            "contributors": "stakeholders",
            "sources": "insights",
        },
        "relationships": [
            "provides-to",
            "receives-from",
            "influences",
            "depends-on",
            "competes-with",
            "partners-with",
            "funds",
            "regulates",
            "enables",
            "constrains",
            "collaborates-with",
            "supplies",
            "consumes",
        ],
    },
    "generic": {
        "domain": "generic",
        "entity_names": {
            "primary": "elements",
            "contributors": "actors",
            "sources": "documents",
        },
        "relationships": [
            "connects-to",
            "depends-on",
            "provides-to",
            "receives-from",
            "influences",
            "owns",
            "manages",
            "uses",
        ],
    },
}


# --- Fixtures --------------------------------------------------------------


@pytest.fixture(scope="module")
def evidence_config():
    """The real templates/evidence/config.yaml, loaded through core.config_loader."""
    assert EVIDENCE_CONFIG.exists(), f"missing template config: {EVIDENCE_CONFIG}"
    return load_config(str(EVIDENCE_CONFIG))


@pytest.fixture
def evidence_manager(tmp_path):
    """GraphManager over a copy of the evidence config, so nothing is written
    into the template directory."""
    dest = tmp_path / "config.yaml"
    shutil.copyfile(EVIDENCE_CONFIG, dest)
    return GraphManager(config_path=str(dest))


def _field(config: GraphConfig, category: str, field_name: str):
    fields = config.get_entity_type_config(category).get("fields", [])
    for field in fields:
        if field.get("name") == field_name:
            return field
    raise AssertionError(f"{category} has no field named {field_name!r}")


def _srgb_to_lab(hex_colour: str):
    """sRGB hex -> CIE L*a*b* (D65), so swatches can be compared perceptually."""
    raw = hex_colour.lstrip("#")
    channels = [int(raw[i : i + 2], 16) / 255 for i in (0, 2, 4)]

    def linearise(c):
        return c / 12.92 if c <= 0.04045 else ((c + 0.055) / 1.055) ** 2.4

    r, g, b = (linearise(c) for c in channels)
    x = r * 0.4124564 + g * 0.3575761 + b * 0.1804375
    y = r * 0.2126729 + g * 0.7151522 + b * 0.0721750
    z = r * 0.0193339 + g * 0.1191920 + b * 0.9503041

    def f(t):
        return t ** (1 / 3) if t > (6 / 29) ** 3 else t / (3 * (6 / 29) ** 2) + 4 / 29

    fx, fy, fz = f(x / 0.95047), f(y / 1.0), f(z / 1.08883)
    return 116 * fy - 16, 500 * (fx - fy), 200 * (fy - fz)


def _delta_e_76(a: str, b: str) -> float:
    return math.sqrt(sum((p - q) ** 2 for p, q in zip(_srgb_to_lab(a), _srgb_to_lab(b))))


def _viewer_source() -> str:
    assert EVIDENCE_VIEWER.exists(), f"missing template viewer: {EVIDENCE_VIEWER}"
    return EVIDENCE_VIEWER.read_text(encoding="utf-8")


def _viewer_script() -> str:
    """Every inline <script> block of the evidence viewer, concatenated."""
    blocks = re.findall(
        r"<script(?![^>]*src=)[^>]*>(.*?)</script>", _viewer_source(), re.S
    )
    assert blocks, "evidence viewer has no inline script blocks"
    return "\n".join(blocks)


def _js_array_literal(name: str) -> list:
    """Pull `const NAME = ['a', 'b', ...];` out of the viewer source."""
    match = re.search(rf"const\s+{name}\s*=\s*(\[.*?\]);", _viewer_script(), re.S)
    assert match, f"viewer has no {name} array"
    return json.loads(match.group(1).replace("'", '"'))


def _js_object_literal(name: str) -> dict:
    """Pull `const NAME = {...};` out of the viewer source (string values only)."""
    match = re.search(rf"const\s+{name}\s*=\s*(\{{.*?\n\s*\}});", _viewer_script(), re.S)
    assert match, f"viewer has no {name} object"
    body = re.sub(r"//[^\n]*", "", match.group(1))
    return json.loads(body.replace("'", '"'))


# A DOM/vis-network stub just rich enough that the viewer's inline script can be
# evaluated head-first under plain node, so viewer behaviour can be probed for
# real instead of pattern-matched in the source.
_VIEWER_STUB_PRELUDE = """
function stubEl() {
  return { addEventListener(){}, removeEventListener(){}, appendChild(){}, focus(){},
           classList:{add(){},remove(){},toggle(){},contains(){return false;}},
           style:{}, value:'', innerHTML:'', textContent:'', disabled:false,
           scrollTop:0, scrollHeight:0, checked:false, dataset:{} };
}
globalThis.document = { getElementById(){ return stubEl(); },
  createElement(){ return stubEl(); }, querySelector(){ return stubEl(); },
  querySelectorAll(){ return []; }, addEventListener(){} };
globalThis.addEventListener = function(){};
globalThis.location = { search:'', href:'', hash:'' };
globalThis.window = globalThis;
globalThis.vis = { Network: function(){ return { on(){}, fit(){}, once(){} }; },
                   DataSet: function(){ return { update(){}, get(){ return []; }, add(){} }; } };
globalThis.fetch = function(){ return Promise.reject(new Error('offline')); };
"""


def _probe_viewer(tmp_path: Path, harness: str) -> dict:
    """Run `harness` against the viewer's real script under node; return its JSON."""
    node = shutil.which("node")
    if node is None:
        pytest.skip("node is not available; cannot execute the viewer's script")
    script = tmp_path / "viewer_probe.js"
    script.write_text(_VIEWER_STUB_PRELUDE + _viewer_script() + harness, encoding="utf-8")
    result = subprocess.run(
        [node, str(script)], capture_output=True, text=True, timeout=60
    )
    assert result.returncode == 0, f"viewer script failed under node:\n{result.stderr}"
    return json.loads(result.stdout)


# --- Loading ---------------------------------------------------------------


def test_evidence_config_loads_via_config_loader(evidence_config):
    assert isinstance(evidence_config, GraphConfig)
    assert evidence_config.domain == "evidence"
    assert evidence_config.version == "1.0"


def test_evidence_config_has_required_top_level_fields(evidence_config):
    # _validate() enforces these, but pin them so a silent removal is caught here
    for field in ("domain", "entity_types", "paths"):
        assert field in evidence_config.config


def test_evidence_config_loads_via_graph_manager(evidence_manager):
    graph = evidence_manager.graph_data
    assert graph["metadata"]["domain"] == "evidence"
    assert graph["claims"] == []
    assert graph["runs"] == []
    assert graph["sources"] == []
    assert graph["relationships"] == []


def test_graph_manager_round_trip_with_evidence_vocabulary(evidence_manager, tmp_path):
    assert evidence_manager.add_entity(
        "primary",
        {
            "id": "h-example",
            "label": "H-example",
            "type": "hypothesis",
            "status": "open",
            "description": "A hypothesis.",
        },
    )
    assert evidence_manager.add_entity(
        "contributors",
        {"id": "run-1", "label": "Run 1", "type": "run", "description": "A run."},
    )
    assert evidence_manager.add_relationship(
        "run-1", "h-example", "tests", description="Run 1 was run to decide H-example."
    )
    evidence_manager.save()

    assert (tmp_path / "_data" / "entities.json").exists()
    assert (tmp_path / "_data" / "visual_config.json").exists()

    reloaded = GraphManager(config_path=str(tmp_path / "config.yaml"))
    assert reloaded.get_entity("primary", "h-example")["status"] == "open"
    assert reloaded.validate() == []


# --- Entity vocabulary -----------------------------------------------------


def test_entity_categories_and_names(evidence_config):
    names = {k: v["name"] for k, v in evidence_config.get_entity_types().items()}
    assert names == {
        "primary": "claims",
        "contributors": "runs",
        "sources": "sources",
    }


def test_claim_types_match_contract(evidence_config):
    assert evidence_config.get_entity_type_config("primary")["types"] == (
        EXPECTED_CLAIM_TYPES
    )
    assert _field(evidence_config, "primary", "type")["values"] == EXPECTED_CLAIM_TYPES


def test_claim_statuses_match_contract(evidence_config):
    assert _field(evidence_config, "primary", "status")["values"] == EXPECTED_STATUSES


# --- The `question` claim type --------------------------------------------


def test_question_is_in_the_claim_type_enum(evidence_config):
    """A question is what the record leaves open: distinct from a hypothesis,
    which asserts something testable, and from a concept, which is vocabulary."""
    for values in (
        evidence_config.get_entity_type_config("primary")["types"],
        _field(evidence_config, "primary", "type")["values"],
    ):
        assert "question" in values, "claims must offer a `question` type"


def test_adding_question_did_not_disturb_the_original_claim_types(evidence_config):
    """Additive means additive: the three original types keep their order and
    their positions, and `question` is appended after them."""
    values = _field(evidence_config, "primary", "type")["values"]
    assert values[: len(ORIGINAL_CLAIM_TYPES)] == ORIGINAL_CLAIM_TYPES
    assert values[-1] == "question"


def test_question_adds_no_new_status_values(evidence_config):
    """The `question` type reuses the status vocabulary rather than extending it.

    An open question is `open` - which is exactly the point, since `open` was
    previously only ever the default a concept fell into when nobody had an
    epistemic verdict to record. An *answered* question does not get an
    "answered" status: it is `retired`, and the answer is carried by the
    incoming retires/supersedes edge from whatever answered it.
    """
    values = _field(evidence_config, "primary", "status")["values"]
    assert values == EXPECTED_STATUSES, (
        "the question type must not add status values; it reuses open/untested/retired"
    )
    assert QUESTION_STATUSES <= set(values)
    assert "answered" not in values, (
        "an answered question is `retired` with a retires edge naming the answer; "
        "a status value meaning 'answered' throws away which result did the answering"
    )


def test_question_status_semantics_are_documented(evidence_config):
    """The status enum's comment has to say how a question uses the vocabulary,
    or the distinction is folklore rather than schema."""
    comment = str(_field(evidence_config, "primary", "status").get("comment", "")).lower()
    assert "question" in comment, "the status field must document the question type"
    for token in ("open", "retire"):
        assert token in comment, f"status comment does not mention {token!r}"


def test_question_has_a_colour_and_a_shape(evidence_config):
    visual = evidence_config.get_visual_config()
    assert visual["colors"].get("question") == QUESTION_COLOR
    assert visual["node_shapes"].get("question") == QUESTION_SHAPE


def test_question_colour_is_distinct_from_every_other_node_type(evidence_config):
    """An open question must not read as a finding or a hypothesis on the canvas."""
    colors = evidence_config.get_visual_config()["colors"]
    confusable = {
        name: round(_delta_e_76(colors["question"], colour), 2)
        for name, colour in colors.items()
        if name not in ("question", "default")
        and _delta_e_76(colors["question"], colour) < MIN_PERCEPTUAL_DISTANCE
    }
    assert not confusable, f"question ({colors['question']}) is confusable with: {confusable}"


def test_question_shape_is_not_reused_by_another_node_type(evidence_config):
    shapes = evidence_config.get_visual_config()["node_shapes"]
    clashes = [
        name
        for name, shape in shapes.items()
        if name not in ("question", "default") and shape == QUESTION_SHAPE
    ]
    assert not clashes, f"{QUESTION_SHAPE!r} is also used by: {clashes}"


def test_graph_manager_accepts_a_question_claim(evidence_manager, tmp_path):
    """End to end: a question node with a blocked-by edge survives a round trip."""
    assert evidence_manager.add_entity(
        "primary",
        {
            "id": "q-gate-cadence",
            "label": "Q: what is the true settling iteration?",
            "type": "question",
            "status": "open",
            "description": "The record leaves it open: settling times are unresolved.",
        },
    )
    assert evidence_manager.add_entity(
        "primary",
        {
            "id": "q-prompt-library",
            "label": "Q: is the prompt library restored?",
            "type": "question",
            "status": "open",
            "description": "Named as the blocker by the record.",
        },
    )
    assert evidence_manager.add_relationship(
        "q-gate-cadence",
        "q-prompt-library",
        "blocked-by",
        description="The cadence re-run needs the prompt library back first.",
    )
    evidence_manager.save()

    reloaded = GraphManager(config_path=str(tmp_path / "config.yaml"))
    restored = reloaded.get_entity("primary", "q-gate-cadence")
    assert restored["type"] == "question"
    assert restored["status"] == "open"
    assert reloaded.validate() == []


def test_run_types_match_contract(evidence_config):
    assert evidence_config.get_entity_type_config("contributors")["types"] == (
        EXPECTED_RUN_TYPES
    )
    assert (
        _field(evidence_config, "contributors", "type")["values"] == EXPECTED_RUN_TYPES
    )


def test_source_types_match_contract(evidence_config):
    assert evidence_config.get_entity_type_config("sources")["types"] == (
        EXPECTED_SOURCE_TYPES
    )
    assert _field(evidence_config, "sources", "type")["values"] == EXPECTED_SOURCE_TYPES


@pytest.mark.parametrize(
    "category,required",
    [
        ("primary", ["id", "label", "type", "status", "description"]),
        ("contributors", ["id", "label", "type", "description"]),
        ("sources", ["id", "title", "type", "path"]),
    ],
)
def test_required_fields_are_marked_required(evidence_config, category, required):
    actual = {
        f["name"]
        for f in evidence_config.get_entity_type_config(category)["fields"]
        if f.get("required")
    }
    assert actual == set(required)


# --- Relationship vocabulary ----------------------------------------------


def test_relationship_types_match_contract(evidence_config):
    assert evidence_config.get_relationship_types() == EXPECTED_EDGE_TYPES


def test_relationship_types_have_no_duplicates(evidence_config):
    types = evidence_config.get_relationship_types()
    assert len(types) == len(set(types))


@pytest.mark.parametrize("family", [EPISTEMIC_EDGES, STRUCTURAL_EDGES, ASSOCIATIVE_EDGES])
def test_every_edge_family_is_present(evidence_config, family):
    types = set(evidence_config.get_relationship_types())
    assert set(family) <= types


# --- The `blocks` / `blocked-by` dependency pair --------------------------


def test_dependency_edges_are_present(evidence_config):
    """The vocabulary must be able to say 'this blocks that', not just describe
    it in prose where nothing can pair two claims stuck behind one artefact."""
    types = evidence_config.get_relationship_types()
    for edge in DEPENDENCY_EDGES:
        assert edge in types, f"relationship vocabulary is missing {edge!r}"


def test_dependency_edges_are_associative_not_epistemic(evidence_config):
    """A blocker changes whether a claim can be settled yet, never whether it is
    true - so `blocks` must not join the signed family."""
    for edge in DEPENDENCY_EDGES:
        assert edge not in EPISTEMIC_EDGES
        assert edge not in STRUCTURAL_EDGES
        assert edge in ASSOCIATIVE_EDGES


def test_dependency_pair_was_appended_without_reordering(evidence_config):
    """Additive: every pre-existing edge type keeps its position in the list."""
    types = evidence_config.get_relationship_types()
    original = EPISTEMIC_EDGES + STRUCTURAL_EDGES + ORIGINAL_ASSOCIATIVE_EDGES
    assert types[: len(original)] == original
    assert types[len(original):] == DEPENDENCY_EDGES


def test_dependency_edges_are_directed_and_share_a_style(evidence_config):
    """`blocks` and `blocked-by` are one relation read from opposite ends, so
    they must be drawn identically - and with an arrow, since which end is
    blocked is the whole content of the edge."""
    styles = evidence_config.get_visual_config()["edge_styles"]
    for edge in DEPENDENCY_EDGES:
        assert styles[edge]["arrows"] is True, f"{edge} must be drawn with an arrow"
        assert styles[edge]["color"] == DEPENDENCY_COLOR
    assert styles["blocks"] == styles["blocked-by"]


def test_dependency_edges_do_not_look_like_the_soft_associative_links(evidence_config):
    """An unblocking is actionable; `relates-to` is not. They must not be drawn
    the same, or the work signal disappears into the plumbing."""
    styles = evidence_config.get_visual_config()["edge_styles"]
    for soft in ("builds-on", "cites", "relates-to"):
        assert styles["blocks"]["color"] != styles[soft]["color"], (
            f"blocks is drawn in the same colour as {soft}"
        )
    assert styles["blocks"]["color"] == evidence_config.get_visual_config()["colors"][
        "question"
    ], "dependency edges should read as part of the question family"


# --- Visualization: status_colors -----------------------------------------


def test_status_colors_present(evidence_config):
    visual = evidence_config.get_visual_config()
    assert "status_colors" in visual, "evidence template must define status_colors"
    assert isinstance(visual["status_colors"], dict)


def test_status_colors_cover_every_status_plus_default(evidence_config):
    status_colors = evidence_config.get_visual_config()["status_colors"]
    missing = [s for s in EXPECTED_STATUSES if s not in status_colors]
    assert not missing, f"status_colors missing entries for: {missing}"
    assert "default" in status_colors, "status_colors needs a 'default' fallback"


def test_status_colors_have_no_extra_keys(evidence_config):
    status_colors = evidence_config.get_visual_config()["status_colors"]
    extra = set(status_colors) - set(EXPECTED_STATUSES) - {"default"}
    assert not extra, f"status_colors has entries for unknown statuses: {sorted(extra)}"


def test_status_colors_are_valid_hex(evidence_config):
    status_colors = evidence_config.get_visual_config()["status_colors"]
    bad = {k: v for k, v in status_colors.items() if not HEX_RE.match(str(v))}
    assert not bad, f"invalid hex colours in status_colors: {bad}"


def test_status_colors_are_distinct_per_status(evidence_config):
    status_colors = evidence_config.get_visual_config()["status_colors"]
    values = [status_colors[s].lower() for s in EXPECTED_STATUSES]
    assert len(values) == len(set(values)), "two statuses share a colour"


# --- Visualization: the `not-supported` status ----------------------------


def test_not_supported_is_in_the_status_enum_after_refuted(evidence_config):
    values = _field(evidence_config, "primary", "status")["values"]
    assert "not-supported" in values, "claims status enum must offer a null-result value"
    assert values.index("not-supported") == values.index("refuted") + 1, (
        "'not-supported' must sit immediately after 'refuted' in the severity gradient"
    )


def test_not_supported_colour_is_present_and_valid_hex(evidence_config):
    status_colors = evidence_config.get_visual_config()["status_colors"]
    assert "not-supported" in status_colors, "status_colors is missing 'not-supported'"
    colour = status_colors["not-supported"]
    assert HEX_RE.match(str(colour)), f"invalid hex colour for not-supported: {colour!r}"
    assert colour == NOT_SUPPORTED_COLOR


def test_not_supported_colour_is_perceptually_distinct(evidence_config):
    """It is a muted sibling of `refuted`, but it must not read as `refuted`."""
    status_colors = evidence_config.get_visual_config()["status_colors"]
    subject = status_colors["not-supported"]
    distances = {
        name: _delta_e_76(subject, colour)
        for name, colour in status_colors.items()
        if name != "not-supported"
    }
    confusable = {
        name: round(d, 2) for name, d in distances.items() if d < MIN_PERCEPTUAL_DISTANCE
    }
    assert not confusable, (
        f"not-supported ({subject}) is confusable with: {confusable} "
        f"(CIE76 deltaE below {MIN_PERCEPTUAL_DISTANCE})"
    )


# --- Visualization: the viewer's copy of the vocabulary -------------------


def test_viewer_status_order_matches_the_config_vocabulary():
    assert _js_array_literal("STATUS_ORDER") == EXPECTED_STATUSES


def test_viewer_status_colors_match_the_config(evidence_config):
    config_colors = evidence_config.get_visual_config()["status_colors"]
    viewer_colors = _js_object_literal("STATUS_COLORS")
    for status in EXPECTED_STATUSES + ["default"]:
        assert status in viewer_colors, f"viewer STATUS_COLORS is missing {status!r}"
        assert viewer_colors[status] == config_colors[status], (
            f"viewer and config disagree on the {status!r} colour"
        )


def test_viewer_has_a_readable_label_for_every_status():
    labels = _js_object_literal("STATUS_LABELS")
    for status in EXPECTED_STATUSES:
        assert status in labels, f"viewer STATUS_LABELS is missing {status!r}"
        assert labels[status].strip(), f"{status!r} has an empty label"
    assert labels["not-supported"] == "Not supported"


def test_viewer_renders_not_supported_in_chips_and_legend(tmp_path):
    probe = _probe_viewer(
        tmp_path,
        """
allNodes = [
  { id:'a', status:'supported',     entityType:'finding' },
  { id:'b', status:'not-supported', entityType:'finding' }
];
colourMode = 'status';
const present = collectPresentValues();
buildChips();
console.log(JSON.stringify({
  present: present.statuses,
  chipActive: activeStatuses['not-supported'],
  colour: statusColour('not-supported'),
  label: statusLabel('not-supported'),
  nodeColour: nodeLiveColour({ status:'not-supported', entityType:'finding' }),
  visible: nodeMatchesChips({ id:'b', status:'not-supported', entityType:'finding' })
}));
""",
    )
    assert probe["present"] == ["supported", "not-supported"]
    assert probe["chipActive"] is True
    assert probe["colour"] == NOT_SUPPORTED_COLOR
    assert probe["label"] == "Not supported"
    assert probe["nodeColour"] == NOT_SUPPORTED_COLOR
    assert probe["visible"] is True


def test_viewer_falls_back_gracefully_on_an_unknown_status(tmp_path):
    """A status the viewer has never heard of must take the default colour and
    stay reachable - chip, legend and canvas. A hardcoded vocabulary that
    silently swallows unknown values is exactly the bug that forced the
    `not-supported` migration; this guards the next extension too."""
    probe = _probe_viewer(
        tmp_path,
        """
allNodes = [
  { id:'a', status:'supported',        entityType:'finding' },
  { id:'b', status:'flibbertigibbet',  entityType:'finding' },
  { id:'c', status:'toString',         entityType:'finding' }
];
colourMode = 'status';
const present = collectPresentValues();
buildChips();
console.log(JSON.stringify({
  present: present.statuses,
  chipActive: activeStatuses['flibbertigibbet'],
  colour: statusColour('flibbertigibbet'),
  prototypeKeyColour: statusColour('toString'),
  defaultColour: STATUS_COLORS.default,
  label: statusLabel('flibbertigibbet'),
  nodeColour: nodeLiveColour({ status:'flibbertigibbet', entityType:'finding' }),
  visible: nodeMatchesChips({ id:'b', status:'flibbertigibbet', entityType:'finding' })
}));
""",
    )
    # It is offered as a filter chip rather than dropped ...
    assert "flibbertigibbet" in probe["present"]
    assert probe["chipActive"] is True
    # ... it renders in the neutral default colour rather than `undefined` ...
    assert probe["colour"] == probe["defaultColour"]
    assert probe["nodeColour"] == probe["defaultColour"]
    # ... an Object.prototype key is not mistaken for a palette entry ...
    assert probe["prototypeKeyColour"] == probe["defaultColour"]
    # ... it gets a readable label ...
    assert probe["label"] == "Flibbertigibbet"
    # ... and the node stays visible on the canvas.
    assert probe["visible"] is True


def test_viewer_status_order_never_gates_visibility():
    """STATUS_ORDER must only sort; collectPresentValues and buildChips must both
    append statuses it does not list."""
    script = _viewer_script()
    for func in ("collectPresentValues", "buildChips"):
        body = re.search(rf"function {func}\(\) \{{(.*?)\n        \}}", script, re.S)
        assert body, f"viewer has no {func}()"
        assert "indexOf(s) === -1" in body.group(1), (
            f"{func}() no longer appends statuses missing from STATUS_ORDER"
        )


# --- Visualization: edge_styles -------------------------------------------


def test_edge_styles_present(evidence_config):
    visual = evidence_config.get_visual_config()
    assert "edge_styles" in visual, "evidence template must define edge_styles"
    assert isinstance(visual["edge_styles"], dict)


def test_edge_styles_cover_every_edge_type_plus_default(evidence_config):
    edge_styles = evidence_config.get_visual_config()["edge_styles"]
    missing = [t for t in EXPECTED_EDGE_TYPES if t not in edge_styles]
    assert not missing, f"edge_styles missing entries for: {missing}"
    assert "default" in edge_styles, "edge_styles needs a 'default' fallback"


def test_edge_styles_have_no_extra_keys(evidence_config):
    edge_styles = evidence_config.get_visual_config()["edge_styles"]
    extra = set(edge_styles) - set(EXPECTED_EDGE_TYPES) - {"default"}
    assert not extra, f"edge_styles has entries for unknown types: {sorted(extra)}"


def test_every_edge_style_is_complete_and_well_formed(evidence_config):
    edge_styles = evidence_config.get_visual_config()["edge_styles"]
    for name, style in edge_styles.items():
        assert isinstance(style, dict), f"{name}: style must be a mapping"
        for key in ("color", "dashes", "width", "arrows"):
            assert key in style, f"{name}: edge style missing {key!r}"
        assert HEX_RE.match(str(style["color"])), (
            f"{name}: invalid hex colour {style['color']!r}"
        )
        assert isinstance(style["arrows"], bool), f"{name}: arrows must be a bool"
        assert isinstance(style["width"], (int, float)) and style["width"] > 0, (
            f"{name}: width must be a positive number"
        )
        dashes = style["dashes"]
        if isinstance(dashes, list):
            assert dashes and all(isinstance(d, (int, float)) for d in dashes), (
                f"{name}: dashes list must hold numbers"
            )
        else:
            assert isinstance(dashes, bool), (
                f"{name}: dashes must be a bool or a list of numbers"
            )


def test_epistemic_edges_are_directed(evidence_config):
    """Signed edges must carry an arrow - direction is what makes them signed."""
    edge_styles = evidence_config.get_visual_config()["edge_styles"]
    for name in EPISTEMIC_EDGES:
        assert edge_styles[name]["arrows"] is True, f"{name} must be drawn with an arrow"


def test_supports_and_refutes_use_the_status_palette(evidence_config):
    """The signed pair must read as the same green/red as the status colours."""
    visual = evidence_config.get_visual_config()
    assert visual["edge_styles"]["supports"]["color"] == (
        visual["status_colors"]["supported"]
    )
    assert visual["edge_styles"]["refutes"]["color"] == visual["status_colors"]["refuted"]


# --- Visualization: node colours / shapes ---------------------------------


def test_node_colors_cover_every_node_type(evidence_config):
    colors = evidence_config.get_visual_config()["colors"]
    for node_type in EXPECTED_CLAIM_TYPES + EXPECTED_RUN_TYPES + EXPECTED_SOURCE_TYPES:
        assert node_type in colors, f"colors missing entry for {node_type}"
    assert "default" in colors
    bad = {k: v for k, v in colors.items() if not HEX_RE.match(str(v))}
    assert not bad, f"invalid hex colours in colors: {bad}"


def test_node_shapes_cover_every_node_type(evidence_config):
    shapes = evidence_config.get_visual_config()["node_shapes"]
    for node_type in EXPECTED_CLAIM_TYPES + EXPECTED_RUN_TYPES + EXPECTED_SOURCE_TYPES:
        assert node_type in shapes, f"node_shapes missing entry for {node_type}"
    assert "default" in shapes


def test_get_color_for_type_falls_back(evidence_config):
    assert evidence_config.get_color_for_type("hypothesis") == "#6B4C8A"
    assert evidence_config.get_color_for_type("no-such-type") == "#7f8c8d"


# --- The template README documents what the schema offers -----------------


@pytest.fixture(scope="module")
def evidence_readme():
    assert EVIDENCE_README.exists(), f"missing template README: {EVIDENCE_README}"
    return EVIDENCE_README.read_text(encoding="utf-8")


def test_readme_documents_every_claim_type(evidence_readme):
    for claim_type in EXPECTED_CLAIM_TYPES:
        assert f"`{claim_type}`" in evidence_readme, (
            f"the template README never mentions the {claim_type!r} claim type"
        )


def test_readme_documents_every_status(evidence_readme):
    for status in EXPECTED_STATUSES:
        assert f"`{status}`" in evidence_readme, f"README is missing status {status!r}"


def test_readme_documents_every_edge_type(evidence_readme):
    for edge in EXPECTED_EDGE_TYPES:
        assert f"`{edge}`" in evidence_readme, f"README is missing edge type {edge!r}"


def test_readme_explains_how_a_question_is_answered(evidence_readme):
    """The one rule that is easy to get wrong: the answer rides on an edge, not
    on a status value."""
    assert "retires" in evidence_readme
    lowered = evidence_readme.lower()
    assert "answered" in lowered
    assert "`question`" in evidence_readme


def test_readme_status_table_covers_the_question_type(evidence_readme):
    """The per-type status table must exist, or the reader has no way to know
    that `open` means something different on a concept and on a question."""
    assert "Status by claim type" in evidence_readme
    assert "| `question` |" in evidence_readme


# --- Regression guard: the four pre-existing templates --------------------


@pytest.mark.parametrize("template", sorted(PRE_EXISTING_TEMPLATES))
def test_pre_existing_template_still_loads(template):
    config = load_config(str(TEMPLATES_DIR / template / "config.yaml"))
    expected = PRE_EXISTING_TEMPLATES[template]

    assert config.domain == expected["domain"]
    names = {k: v["name"] for k, v in config.get_entity_types().items()}
    assert names == expected["entity_names"]
    assert config.get_relationship_types() == expected["relationships"]


@pytest.mark.parametrize("template", sorted(PRE_EXISTING_TEMPLATES))
def test_pre_existing_template_still_builds_a_graph(template, tmp_path):
    dest = tmp_path / "config.yaml"
    shutil.copyfile(TEMPLATES_DIR / template / "config.yaml", dest)
    manager = GraphManager(config_path=str(dest))

    expected_names = PRE_EXISTING_TEMPLATES[template]["entity_names"]
    for name in expected_names.values():
        assert manager.graph_data[name] == []
    assert manager.graph_data["relationships"] == []
    assert manager.graph_data["metadata"]["domain"] == template

    manager.add_entity("primary", {"id": "x", "label": "X"})
    manager.add_relationship(
        "x", "x", PRE_EXISTING_TEMPLATES[template]["relationships"][0]
    )
    manager.save()
    assert (tmp_path / "_data" / "entities.json").exists()
    assert manager.validate() == []


@pytest.mark.parametrize("template", sorted(PRE_EXISTING_TEMPLATES))
def test_pre_existing_templates_do_not_gain_evidence_only_keys(template):
    """status_colors / edge_styles belong to the evidence template only; if they
    leak into the others, the evidence work was applied too broadly."""
    visual = load_config(str(TEMPLATES_DIR / template / "config.yaml")).get_visual_config()
    assert "status_colors" not in visual
    assert "edge_styles" not in visual
    assert set(visual) == {"colors", "node_sizes", "physics"}


def test_all_five_templates_are_present_and_loadable():
    templates = sorted(p.name for p in TEMPLATES_DIR.iterdir() if (p / "config.yaml").exists())
    assert templates == ["ecosystem", "evidence", "generic", "research", "systems"]
    for name in templates:
        load_config(str(TEMPLATES_DIR / name / "config.yaml"))
