"""课堂讲义提取场景"""

import textwrap
from typing import Dict, List

import langextract as lx

from app.scenarios.base import BaseScenario


class RadiologyScenario(BaseScenario):
    """课堂讲义提取场景（保留 radiology 场景 ID 以兼容现有接口）"""

    name = "课堂讲义"
    description = "从课程讲义或板书整理中提取章节结构、定义、推导步骤与注意事项，用于教学导学"
    extract_classes = ["章节", "核心定义", "推导步骤", "例题", "注意事项", "前置知识"]

    def get_prompt(self) -> str:
        return textwrap.dedent("""\
            从课堂讲义文本中提取以下信息:

            - 章节: 主题标题与小节
            - 核心定义: 课程中给出的正式定义
            - 推导步骤: 推导过程中的关键步骤
            - 例题: 讲义中的典型例题描述
            - 注意事项: 常见误区或边界条件
            - 前置知识: 理解本节需要先掌握的知识点

            要求:
            1. extraction_text 必须是原文精确子串
            2. 不改写符号表达，不省略公式中的上下标
            3. 推导步骤按原文顺序抽取
            4. 注意事项要保留原文限定词（如“仅当”“必须”）
            """)

    def get_examples(self) -> List[lx.data.ExampleData]:
        example_text = (
            "第三章 节点电压法。定义：节点电压是该节点相对参考节点的电位差。"
            "推导步骤：先列 KCL 方程，再代入元件伏安关系。注意：参考方向必须先统一。"
        )

        return [
            lx.data.ExampleData(
                text=example_text,
                extractions=[
                    lx.data.Extraction(
                        extraction_class="章节",
                        extraction_text="第三章 节点电压法",
                        attributes={"层级": "章"}
                    ),
                    lx.data.Extraction(
                        extraction_class="核心定义",
                        extraction_text="节点电压是该节点相对参考节点的电位差",
                        attributes={"术语": "节点电压"}
                    ),
                    lx.data.Extraction(
                        extraction_class="推导步骤",
                        extraction_text="先列 KCL 方程，再代入元件伏安关系",
                        attributes={"顺序": "1-2"}
                    ),
                    lx.data.Extraction(
                        extraction_class="注意事项",
                        extraction_text="参考方向必须先统一",
                        attributes={"类型": "符号约定"}
                    ),
                ]
            )
        ]

    def get_samples(self) -> List[Dict[str, str]]:
        return [
            {
                "id": "lecture_sample_1",
                "title": "电路分析课堂讲义",
                "text": textwrap.dedent("""\
                    第四章 叠加定理与戴维宁等效
                    核心定义：线性双向网络对激励满足可加性与齐次性。
                    前置知识：欧姆定律、KCL、KVL。

                    推导步骤：
                    1. 识别独立电源并逐一置零；
                    2. 分别计算各独立电源单独作用下的响应；
                    3. 将各响应代数相加得到总响应。

                    注意事项：含受控源时不得将受控源置零。
                    """).strip()
            },
            {
                "id": "lecture_sample_2",
                "title": "信号与系统课堂讲义",
                "text": textwrap.dedent("""\
                    第二章 连续时间卷积
                    核心定义：y(t)=x(t)*h(t)=∫x(τ)h(t-τ)dτ。
                    例题：求单位阶跃输入通过一阶系统后的响应。
                    注意事项：卷积上下限取值需结合信号支撑区间。
                    """).strip()
            }
        ]
