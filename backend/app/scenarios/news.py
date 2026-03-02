"""课程知识点提取场景"""

import textwrap
from typing import Dict, List

import langextract as lx

from app.scenarios.base import BaseScenario


class NewsScenario(BaseScenario):
    """课程知识点提取场景（保留 news 场景 ID 以兼容现有接口）"""

    name = "课程知识点"
    description = "从教材、讲义中提取可用于智能导学的概念、定理、公式与适用条件等结构化信息"
    extract_classes = ["概念", "定理", "公式", "适用条件", "单位", "结论"]

    def get_prompt(self) -> str:
        return textwrap.dedent("""\
            从课程教材文本中提取以下信息:

            - 概念: 关键术语、定义对象
            - 定理: 明确命名或可识别的定理/规律
            - 公式: 数学表达式与符号关系
            - 适用条件: 定理或公式成立前提
            - 单位: 文本中出现的量纲与单位信息
            - 结论: 章节中给出的核心结论

            要求:
            1. extraction_text 必须是原文精确子串，不得改写
            2. 不推断原文未出现的信息
            3. 数值与单位必须保持原样
            4. 按原文出现顺序抽取，避免重复
            5. 为定理、公式补充章节或用途属性（如可识别）
            """)

    def get_examples(self) -> List[lx.data.ExampleData]:
        example_text = (
            "在稳态正弦电路中，欧姆定律可写为 U = I·R。"
            "该公式适用于线性时不变电阻元件，电压单位为 V，电流单位为 A。"
        )

        return [
            lx.data.ExampleData(
                text=example_text,
                extractions=[
                    lx.data.Extraction(
                        extraction_class="概念",
                        extraction_text="稳态正弦电路",
                        attributes={"章节": "电路基础"}
                    ),
                    lx.data.Extraction(
                        extraction_class="定理",
                        extraction_text="欧姆定律",
                        attributes={"用途": "电压电流关系"}
                    ),
                    lx.data.Extraction(
                        extraction_class="公式",
                        extraction_text="U = I·R",
                        attributes={"关联定理": "欧姆定律"}
                    ),
                    lx.data.Extraction(
                        extraction_class="适用条件",
                        extraction_text="线性时不变电阻元件",
                        attributes={"关联公式": "U = I·R"}
                    ),
                    lx.data.Extraction(
                        extraction_class="单位",
                        extraction_text="V",
                        attributes={"量纲": "电压"}
                    ),
                    lx.data.Extraction(
                        extraction_class="单位",
                        extraction_text="A",
                        attributes={"量纲": "电流"}
                    ),
                ]
            )
        ]

    def get_samples(self) -> List[Dict[str, str]]:
        return [
            {
                "id": "knowledge_sample_1",
                "title": "电路分析基础知识点",
                "text": textwrap.dedent("""\
                    叠加定理指出：在线性电路中，多个独立电源共同作用时的响应，
                    等于每个独立电源单独作用时响应的代数和。

                    该定理适用于线性网络，不适用于含非线性元件的电路。
                    在计算时，电压源置零可等效为短路，电流源置零可等效为开路。

                    节点电压法中常用公式为 G·V = I，其中电导单位为 S，电压单位为 V。
                    """).strip()
            },
            {
                "id": "knowledge_sample_2",
                "title": "控制系统稳定性知识点",
                "text": textwrap.dedent("""\
                    对于连续线性时不变系统，若闭环特征方程全部根实部小于 0，则系统渐近稳定。
                    劳斯判据可用于判别多项式根是否位于左半平面。

                    判据适用前提是特征方程系数为实数且首项系数大于 0。
                    在单位负反馈结构中，稳态误差常结合终值定理进行分析。
                    """).strip()
            }
        ]
