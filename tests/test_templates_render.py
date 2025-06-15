import pytest
from pathlib import Path
from datetime import datetime

from research_evaluator_agent.prompts.template import apply_template
from research_evaluator_agent.prompts.vars import MetricVars, CustomMetricVars, InterpreterVars

PROMPT_DIR = Path("../src/research_evaluator_agent/prompts")

TEMPLATE_MAP = {
    "breadth": MetricVars,
    "depth": MetricVars,
    "novelty": MetricVars,
    "relevance": MetricVars,
    "factuality": MetricVars,
    "custom_metric": CustomMetricVars,
    "interpreter": InterpreterVars,
}


@pytest.mark.parametrize("tpl_name", list(TEMPLATE_MAP.keys()))
def test_template_render_smoke(tpl_name):
    tpl_path = PROMPT_DIR / f"{tpl_name}.md"
    assert tpl_path.exists(), f"Missing template {tpl_path}"

    # prepare vars
    if tpl_name == "custom_metric":
        vars_obj = CustomMetricVars( metric_name="coherence", metric_definition="logic", rubric=[{"score": 1, "description": "poor"}]
        )
    elif tpl_name == "interpreter":
        vars_obj = InterpreterVars( metrics=["breadth", "depth"])
    else:
        vars_obj = MetricVars(metric_name=tpl_name)

    rendered = apply_template(tpl_name, variables=vars_obj)

    # basic checks: no unreplaced variables, contains chunk/keywords
    assert "{{" not in rendered