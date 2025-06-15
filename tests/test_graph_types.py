import pytest
from pydantic import ValidationError

from research_evaluator_agent.agents.graph.types import SharedContext, MetricScoreResult, State, OutputState
from research_evaluator_agent.prompts.vars import MetricVars


def test_shared_context_defaults_and_valid():
    sc = SharedContext()
    # 默认值
    assert sc.language is None
    assert sc.format is None
    assert sc.focus == []
    assert sc.avoid == []
    # 赋值测试
    sc2 = SharedContext(language="en", format="table", focus=["a", "b"], avoid=["c"])
    assert sc2.language == "en"
    assert sc2.format == "table"
    assert sc2.focus == ["a", "b"]
    assert sc2.avoid == ["c"]


def test_shared_context_invalid_focus_type():
    with pytest.raises(ValidationError):
        SharedContext(focus="not-a-list")


def test_metric_score_result_defaults_and_valid():
    msr = MetricScoreResult()
    assert msr.metric_name == ""
    assert msr.score == 0
    assert msr.comment == ""
    # 赋值测试
    msr2 = MetricScoreResult(metric_name="depth", score=5, comment="OK")
    assert msr2.metric_name == "depth"
    assert msr2.score == 5
    assert msr2.comment == "OK"


def test_metric_score_result_invalid_score_type():
    with pytest.raises(ValidationError):
        MetricScoreResult(metric_name="breadth", score="high")


def test_state_minimal_required_fields_and_defaults():
    # 仅提供必需字段
    state = State(user_intent="test", input_content="content")
    assert state.locale == "zh-CN"
    assert state.metrics is None
    assert state.shared_context is None
    assert state.metric_scores is None
    # 提供 metrics 列表
    metrics = [MetricVars(metric_name="breadth"), MetricVars(metric_name="depth")]
    state2 = State(user_intent="u", input_content="c", metrics=metrics)
    assert state2.metrics == metrics

def test_state_shared_context():
    # 仅提供必需字段
    shared_context = SharedContext(language="en", format="table", focus=["a", "b"], avoid=["c"])
    # 提供 metrics 列表
    state2 = State(user_intent="u", input_content="c")
    setattr(state2, "shared_context", shared_context)
    assert state2.shared_context == shared_context


def test_state_invalid_missing_fields():
    with pytest.raises(ValidationError):
        State()


def test_state_invalid_metrics_type():
    with pytest.raises(ValidationError):
        State(user_intent="u", input_content="c", metrics=["breadth"])


def test_state_metric_scores_assignment():
    msr1 = MetricScoreResult(metric_name="breadth", score=3)
    msr2 = MetricScoreResult(metric_name="depth", score=4)
    state = State(user_intent="u", input_content="c", metric_scores=[msr1, msr2])
    assert state.metric_scores == [msr1, msr2]


def test_output_state_defaults_and_valid():
    os = OutputState()
    assert os.overall_score == 0.0
    assert os.overall_comment == ""
    assert os.metric_scores is None
    # 覆盖赋值
    msr1 = MetricScoreResult(metric_name="breadth", score=3, comment="good")
    msr2 = MetricScoreResult(metric_name="depth", score=4, comment="")
    os2 = OutputState(overall_score=4.2, overall_comment="summary", metric_scores=[msr1, msr2])
    assert os2.overall_score == 4.2
    assert os2.overall_comment == "summary"
    assert os2.metric_scores == [msr1, msr2]


def test_output_state_invalid_score_type():
    with pytest.raises(ValidationError):
        OutputState(overall_score="high") 