"""Tests for core.graph_manager.GraphManager against a minimal config."""

import sys
from pathlib import Path

# Make the repo root importable regardless of how pytest is invoked
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

import pytest

from core.graph_manager import GraphManager

MINIMAL_CONFIG = """\
domain: test
version: "1.0"

entity_types:
  primary:
    name: concepts
  contributors:
    name: people
  sources:
    name: papers

relationships:
  types: [relates-to]

paths:
  data_dir: "./_data"
  entities_file: "entities.json"
"""


@pytest.fixture
def gm(tmp_path):
    config_path = tmp_path / "config.yaml"
    config_path.write_text(MINIMAL_CONFIG, encoding="utf-8")
    return GraphManager(config_path=str(config_path))


def test_init_creates_empty_collections(gm):
    assert gm.graph_data["concepts"] == []
    assert gm.graph_data["relationships"] == []
    assert gm.graph_data["metadata"]["domain"] == "test"


def test_add_entity_and_duplicate_rejected(gm):
    entity = {"id": "a", "label": "A"}
    assert gm.add_entity("primary", entity) is True
    assert gm.add_entity("primary", entity) is False
    assert gm.get_entity("primary", "a") == entity


def test_add_relationship_and_duplicate_rejected(gm):
    assert gm.add_relationship("a", "b", "relates-to", description="test") is True
    assert gm.add_relationship("a", "b", "relates-to") is False
    rel = gm.graph_data["relationships"][0]
    assert (rel["from"], rel["to"], rel["type"]) == ("a", "b", "relates-to")


def test_update_entity(gm):
    gm.add_entity("primary", {"id": "a", "label": "A"})
    assert gm.update_entity("primary", "a", {"label": "A2"}) is True
    assert gm.get_entity("primary", "a")["label"] == "A2"
    assert gm.update_entity("primary", "missing", {"label": "X"}) is False


def test_save_and_reload_round_trip(gm, tmp_path):
    gm.add_entity("primary", {"id": "a", "label": "A"})
    gm.add_relationship("a", "a", "relates-to")
    gm.save()

    assert (tmp_path / "_data" / "entities.json").exists()

    reloaded = GraphManager(config_path=str(tmp_path / "config.yaml"))
    assert reloaded.get_entity("primary", "a") == {"id": "a", "label": "A"}
    assert len(reloaded.graph_data["relationships"]) == 1


def test_stats_and_validate(gm):
    gm.add_entity("primary", {"id": "a", "label": "A"})
    gm.add_relationship("a", "ghost", "relates-to")

    stats = gm.get_stats()
    assert stats["concepts"] == 1
    assert stats["relationships"] == 1

    issues = gm.validate()
    assert any("ghost" in issue for issue in issues)
