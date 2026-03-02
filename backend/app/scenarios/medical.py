"""学习日志提取场景"""

import textwrap
from typing import Dict, List

import langextract as lx

from app.scenarios.base import BaseScenario


class MedicalScenario(BaseScenario):
    """学习日志提取场景（保留 medical 场景 ID 以兼容现有接口）"""

    name = "学习日志"
    description = "从学生反思、错题复盘和学习记录中提取错误归因与纠正策略，支撑教学导学追踪"
    extract_classes = ["学习目标", "错误类型", "错误归因", "纠正策略", "掌握度变化", "下一步计划", "证据片段"]

    def get_prompt(self) -> str:
        return textwrap.dedent("""\
            从学习日志文本中提取以下信息:

            - 学习目标: 本次学习或复盘目标
            - 错误类型: 计算错误、概念混淆、条件遗漏等
            - 错误归因: 导致错误的原因描述
            - 纠正策略: 学生采取或计划采取的改进方法
            - 掌握度变化: 对知识掌握情况的变化描述
            - 下一步计划: 后续学习安排
            - 证据片段: 支撑以上结论的原文语句

            要求:
            1. extraction_text 必须为原文精确子串，不得改写
            2. 不推断学生未明确表达的内容
            3. 保留原始量化描述（如“正确率从 60% 提升到 85%”）
            4. 按原文顺序抽取，避免重复
            5. 纠正策略尽量附带时间或执行频率属性（若原文包含）
            """)

    def get_examples(self) -> List[lx.data.ExampleData]:
        example_text = (
            "本周目标是掌握节点电压法。错题中我经常遗漏参考方向，导致符号错误。"
            "我计划每天完成 5 道节点方程练习，并在解题后逐步检查方向假设。"
            "目前正确率从 62% 提升到 81%。"
        )

        return [
            lx.data.ExampleData(
                text=example_text,
                extractions=[
                    lx.data.Extraction(
                        extraction_class="学习目标",
                        extraction_text="掌握节点电压法",
                        attributes={"周期": "本周"}
                    ),
                    lx.data.Extraction(
                        extraction_class="错误类型",
                        extraction_text="符号错误",
                        attributes={"场景": "节点方程"}
                    ),
                    lx.data.Extraction(
                        extraction_class="错误归因",
                        extraction_text="遗漏参考方向",
                        attributes={"影响": "导致符号错误"}
                    ),
                    lx.data.Extraction(
                        extraction_class="纠正策略",
                        extraction_text="每天完成 5 道节点方程练习",
                        attributes={"频率": "每天"}
                    ),
                    lx.data.Extraction(
                        extraction_class="掌握度变化",
                        extraction_text="正确率从 62% 提升到 81%",
                        attributes={"指标": "正确率"}
                    ),
                ]
            )
        ]

    def get_samples(self) -> List[Dict[str, str]]:
        return [
            {
                "id": "learning_log_sample_1",
                "title": "电路课程错题复盘",
                "text": textwrap.dedent("""\
                    本周学习目标：熟练使用戴维宁等效与叠加定理。
                    在三道综合题中，我有两次忽略了“线性网络”这个适用条件，导致结论虽然数值接近但逻辑错误。

                    错误归因：做题时急于代公式，没有先检查题目约束条件。
                    纠正策略：每次解题前先写“已知-求解-约束”三行清单；每天晚自习复盘 20 分钟。

                    掌握度变化：本周章节测验从 68 分提升到 84 分。
                    下一步计划：补做 6 道含受控源的等效变换题，并在周五前完成总结。
                    """).strip()
            },
            {
                "id": "learning_log_sample_2",
                "title": "控制系统学习反思",
                "text": textwrap.dedent("""\
                    我这周重点复习了劳斯判据和根轨迹法。
                    主要错误类型是“判据表首列符号变化数统计错误”和“根轨迹起止点判断混淆”。

                    错误归因是对步骤记忆化，缺少对定义的理解。
                    纠正策略：按步骤口述每一行推导原因，并和同学互查作业。

                    目前稳态误差相关题正确率由 55% 提升到 79%。
                    下周计划是完成一次 90 分钟限时训练，并把错因归档到错题本。
                    """).strip()
            }
        ]
