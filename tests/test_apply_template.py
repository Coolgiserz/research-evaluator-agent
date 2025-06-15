import pytest
from datetime import datetime

from research_evaluator_agent.prompts.template import apply_template
from research_evaluator_agent.prompts.vars import MetricVars, CustomMetricVars, InterpreterVars


def test_apply_template_with_dataclass():
    vars_obj = MetricVars( language="en")
    result = apply_template("breadth", variables=vars_obj.to_dict())
    print(result)
    assert "breadth" in result
    # LANGUAGE should be substituted (not appear as Jinja variable)
    assert "{{ LANGUAGE }}" not in result



def test_custom_metric_template():
    vars_obj = CustomMetricVars(
        metric_name="coherence",
        metric_definition="Logic coherence",
        rubric=[{"score": 1, "description": "Poor"}, {"score": 5, "description": "Great"}],
    )
    result = apply_template("custom_metric", variables=vars_obj)
    assert "coherence" in result
    assert "Logic coherence" in result
