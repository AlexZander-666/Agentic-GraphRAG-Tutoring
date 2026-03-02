"""实验报告提取场景"""

import textwrap
from typing import Dict, List

import langextract as lx

from app.scenarios.base import BaseScenario


class MedicationScenario(BaseScenario):
    """实验报告提取场景（保留 medication 场景 ID 以兼容现有接口）"""

    name = "实验报告"
    description = "从实验指导书和实验报告中提取实验目的、条件、步骤与结论，服务教学导学和可追溯验证"
    extract_classes = ["实验目的", "实验条件", "仪器参数", "实验步骤", "观测结果", "误差分析", "结论"]

    def get_prompt(self) -> str:
        return textwrap.dedent("""\
            从实验文本中提取以下信息:

            - 实验目的: 本实验要验证或测量的对象
            - 实验条件: 环境、先验假设、操作约束
            - 仪器参数: 仪器型号、量程、精度等
            - 实验步骤: 操作流程
            - 观测结果: 原始数据或现象描述
            - 误差分析: 偏差来源与影响
            - 结论: 实验结论及是否达到目标

            要求:
            1. extraction_text 必须为原文精确子串，不得改写
            2. 参数与单位原样保留
            3. 按步骤先后顺序抽取
            4. 误差分析不得推断原文未出现内容
            """)

    def get_examples(self) -> List[lx.data.ExampleData]:
        example_text = (
            "实验目的：测量 RC 电路时间常数。仪器为示波器，采样率 1MS/s。"
            "步骤：输入阶跃信号并记录电容电压上升曲线。结论：测得 τ≈0.098s。"
        )

        return [
            lx.data.ExampleData(
                text=example_text,
                extractions=[
                    lx.data.Extraction(
                        extraction_class="实验目的",
                        extraction_text="测量 RC 电路时间常数",
                        attributes={"课程": "电路实验"}
                    ),
                    lx.data.Extraction(
                        extraction_class="仪器参数",
                        extraction_text="采样率 1MS/s",
                        attributes={"仪器": "示波器"}
                    ),
                    lx.data.Extraction(
                        extraction_class="实验步骤",
                        extraction_text="输入阶跃信号并记录电容电压上升曲线",
                        attributes={"序号": "1"}
                    ),
                    lx.data.Extraction(
                        extraction_class="结论",
                        extraction_text="测得 τ≈0.098s",
                        attributes={"单位": "s"}
                    ),
                ]
            )
        ]

    def get_samples(self) -> List[Dict[str, str]]:
        return [
            {
                "id": "lab_sample_1",
                "title": "RC 暂态响应实验",
                "text": textwrap.dedent("""\
                    实验目的：验证一阶 RC 电路充电过程，并估计时间常数。
                    实验条件：室温 25°C，电源电压 5V，初始电容电压为 0V。
                    仪器参数：示波器量程 10V/div，采样率 2MS/s。

                    实验步骤：
                    1. 按电路图连接 R=2kΩ、C=47μF；
                    2. 输入方波激励并捕获上升沿；
                    3. 记录 63.2% 电压对应时刻。

                    观测结果：63.2% 电压点出现在 0.095s 左右。
                    误差分析：导线接触电阻与示波器读数分辨率引入约 3% 偏差。
                    结论：测得时间常数与理论值基本一致。
                    """).strip()
            },
            {
                "id": "lab_sample_2",
                "title": "控制系统阶跃响应实验",
                "text": textwrap.dedent("""\
                    实验目的：观察二阶系统在不同阻尼比下的超调与调节时间。
                    实验条件：采样周期 1ms，输入为单位阶跃。
                    实验步骤：分别设置阻尼比 0.3、0.6、0.9，记录输出曲线指标。
                    观测结果：阻尼比 0.3 时超调约 38%，阻尼比 0.9 时几乎无超调。
                    结论：阻尼比增大可降低超调，但响应速度会下降。
                    """).strip()
            }
        ]
