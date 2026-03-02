import sys
import types


class _DummyExtraction:
    def __init__(self, *args, **kwargs):
        self.args = args
        self.kwargs = kwargs


class _DummyExampleData:
    def __init__(self, *args, **kwargs):
        self.args = args
        self.kwargs = kwargs


if "langextract" not in sys.modules:
    sys.modules["langextract"] = types.SimpleNamespace(
        data=types.SimpleNamespace(
            ExampleData=_DummyExampleData,
            Extraction=_DummyExtraction,
        )
    )

import app.scenarios  # noqa: F401
from app.scenarios.base import ScenarioRegistry


def test_core_teaching_scenarios_align_with_education_domain():
    scenarios = ScenarioRegistry.list_all()

    assert scenarios["news"]["name"] == "课程知识点"
    assert scenarios["finance"]["name"] == "工程习题"
    assert scenarios["medical"]["name"] == "学习日志"

    assert "概念" in scenarios["news"]["extract_classes"]
    assert "约束条件" in scenarios["finance"]["extract_classes"]
    assert "纠正策略" in scenarios["medical"]["extract_classes"]


def test_all_registered_scenarios_use_teaching_descriptions():
    scenarios = ScenarioRegistry.list_all()

    assert len(scenarios) == 7
    for scenario in scenarios.values():
        description = scenario["description"]
        assert any(keyword in description for keyword in ("课程", "教学", "导学", "学习"))
