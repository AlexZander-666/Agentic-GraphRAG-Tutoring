"""工程习题提取场景"""

import textwrap
from typing import Dict, List

import langextract as lx

from app.scenarios.base import BaseScenario


class FinanceScenario(BaseScenario):
    """工程习题提取场景（保留 finance 场景 ID 以兼容现有接口）"""

    name = "工程习题"
    description = "从工程课程题目与解题过程文本中提取已知条件、目标、约束条件、公式和结论，支撑教学导学"
    extract_classes = ["已知条件", "目标", "约束条件", "公式", "中间推导", "结论"]

    def get_prompt(self) -> str:
        return textwrap.dedent("""\
            从工程习题文本中提取以下信息:

            - 已知条件: 题目给定的数值、参数、初始状态
            - 目标: 需要求解或证明的对象
            - 约束条件: 适用范围、边界条件、理想化假设
            - 公式: 解题中使用的计算式
            - 中间推导: 关键代换与推导结果
            - 结论: 最终答案及其单位/条件

            要求:
            1. extraction_text 必须是原文精确子串，不得改写
            2. 保留所有数字、符号与单位
            3. 为公式标注用途（如“求阻抗”“求稳态误差”）
            4. 为结论标注是否满足约束条件（若原文给出）
            5. 按原文顺序抽取，避免重复
            """)

    def get_examples(self) -> List[lx.data.ExampleData]:
        example_text = (
            "已知 R=10Ω，L=0.2H，角频率 ω=50rad/s，求串联 RL 电路的阻抗幅值。"
            "由公式 |Z|=√(R²+(ωL)²) 得 |Z|≈14.14Ω。"
        )

        return [
            lx.data.ExampleData(
                text=example_text,
                extractions=[
                    lx.data.Extraction(
                        extraction_class="已知条件",
                        extraction_text="R=10Ω",
                        attributes={"类型": "电阻"}
                    ),
                    lx.data.Extraction(
                        extraction_class="已知条件",
                        extraction_text="L=0.2H",
                        attributes={"类型": "电感"}
                    ),
                    lx.data.Extraction(
                        extraction_class="已知条件",
                        extraction_text="ω=50rad/s",
                        attributes={"类型": "角频率"}
                    ),
                    lx.data.Extraction(
                        extraction_class="目标",
                        extraction_text="求串联 RL 电路的阻抗幅值",
                        attributes={"章节": "交流电路"}
                    ),
                    lx.data.Extraction(
                        extraction_class="公式",
                        extraction_text="|Z|=√(R²+(ωL)²)",
                        attributes={"用途": "求阻抗幅值"}
                    ),
                    lx.data.Extraction(
                        extraction_class="结论",
                        extraction_text="|Z|≈14.14Ω",
                        attributes={"单位": "Ω"}
                    ),
                ]
            )
        ]

    def get_samples(self) -> List[Dict[str, str]]:
        return [
            {
                "id": "exercise_sample_1",
                "title": "电路分析计算题",
                "text": textwrap.dedent("""\
                    已知一阶 RC 电路中 R=2kΩ，C=50μF，输入电压为阶跃信号 10V。
                    设初始电容电压为 0V，求 t=0.1s 时电容电压 vc(t)。

                    约束条件：采用理想元件模型，忽略寄生参数与温度漂移。
                    已知公式 vc(t)=V(1-e^(-t/RC))，其中时间常数 τ=RC。

                    代入可得 τ=0.1s，故 vc(0.1)=10(1-e^-1)≈6.32V。
                    """).strip()
            },
            {
                "id": "exercise_sample_2",
                "title": "自动控制稳态误差题",
                "text": textwrap.dedent("""\
                    已知单位负反馈系统开环传递函数 G(s)=K/(s(s+2))，取 K=20。
                    求单位斜坡输入下系统稳态误差。

                    约束条件：系统闭环稳定且输入信号为 r(t)=t。
                    速度误差系数 Kv=lim(s->0) sG(s)=10。
                    因此稳态误差 ess=1/Kv=0.1。
                    """).strip()
            }
        ]
