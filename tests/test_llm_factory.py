import os
from pathlib import Path

import pytest

from research_evaluator_agent.llms import get_llm


@pytest.fixture(scope="module")
def conf_file(tmp_path_factory):
    cfg = {
        "llm": {
            "basic": {
                "model": "gpt-test",
                "api_key": "sk-test",
                "base_url": "http://localhost:1234",
            }
        }
    }
    p = tmp_path_factory.mktemp("cfg") / "conf.yaml"
    import json

    import yaml
    with p.open("w", encoding="utf-8") as f:
        yaml.safe_dump(cfg, f)
    return p


def test_get_llm(conf_file):
    llm = get_llm("basic", conf_path=str(conf_file))
    # Should return ChatOpenAI instance
    from langchain_openai import ChatOpenAI

    assert isinstance(llm, ChatOpenAI)
    # Subsequent call returns cached instance
    llm2 = get_llm("basic", conf_path=str(conf_file))
    assert llm is llm2

def test_get_llm_basic_conf(conf_file):
    llm = get_llm("basic")
    # Should return ChatOpenAI instance
    from langchain_openai import ChatOpenAI

    assert isinstance(llm, ChatOpenAI)
    # Subsequent call returns cached instance
    response = llm.invoke("hi")
    print(response)
    assert isinstance(response.content, str)

def test_get_llm_reason_conf(conf_file):
    llm = get_llm("reason")
    # Should return ChatOpenAI instance
    from langchain_openai import ChatOpenAI

    assert isinstance(llm, ChatOpenAI)
    # Subsequent call returns cached instance
    response = llm.invoke("hi")
    print(response)
    assert isinstance(response.content, str)