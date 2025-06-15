import textwrap
from pathlib import Path

import pytest

from research_evaluator_agent.config.metrics import MetricConfiguration, MetricInfo


SAMPLE_CONF = Path("conf.yaml.sample")


@pytest.mark.skipif(not SAMPLE_CONF.exists(), reason="sample config missing")
def test_metric_configuration_load_sample():
    cfg = MetricConfiguration(SAMPLE_CONF)

    # expected metric names order
    expected = [
        "breadth",
        "depth",
        "relevance",
        "novelty",
        "factuality",
    ]
    assert cfg.names == expected
    assert len(cfg) == 5

    # weights mapping keys set equals names
    weights = cfg.weights()
    assert set(weights.keys()) == set(expected)

    # templates mapping keys equal names and file text non-empty
    templates = cfg.templates()
    assert set(templates.keys()) == set(expected)
    for content in templates.values():
        assert content.strip(), "template content should not be empty"


def test_metric_configuration_missing_file(tmp_path: Path):
    fake_path = tmp_path / "missing.yaml"
    with pytest.raises(FileNotFoundError):
        MetricConfiguration(fake_path)


def test_metric_configuration_invalid_weight(tmp_path: Path):
    # create minimal config with invalid weight
    conf_path = tmp_path / "conf.yaml"
    conf_path.write_text(
        textwrap.dedent(
            """
            metrics:
              toy:
                template: prompts/breadth.md
                weight: 0
            """
        ).strip()
    )

    with pytest.raises(ValueError):
        MetricConfiguration(conf_path)

SAMPLE_CONF = Path("../conf.yaml")

@pytest.mark.skip("not done")
def test_metric_configuration():
    cfg = MetricConfiguration(SAMPLE_CONF)

    # expected metric names order
    expected = [
        "breadth",
        "depth",
        "relevance",
        "novelty",
        "factuality",
    ]
    assert cfg.names == expected
    assert len(cfg) == 5

    # weights mapping keys set equals names
    weights = cfg.weights()
    assert set(weights.keys()) == set(expected)

    # templates mapping keys equal names and file text non-empty
    templates = cfg.templates()
    assert set(templates.keys()) == set(expected)
    for content in templates.values():
        assert content.strip(), "template content should not be empty"
