"""作业批改提取场景"""

import textwrap
from typing import Dict, List

import langextract as lx

from app.scenarios.base import BaseScenario


class SalesScenario(BaseScenario):
    """作业批改提取场景（保留 sales 场景 ID 以兼容现有接口）"""

    name = "作业批改"
    description = "从作业题目、学生答案和教师批注中提取评分证据与反馈建议，用于教学导学"
    extract_classes = ["题号", "学生答案", "标准答案", "得分点", "失分点", "反馈建议", "引用证据"]

    def get_prompt(self) -> str:
        return textwrap.dedent("""\
            从作业批改文本中提取以下信息:

            - 题号: 题目编号
            - 学生答案: 学生原始作答内容
            - 标准答案: 标准解法或参考结论
            - 得分点: 学生答对的关键点
            - 失分点: 学生存在的问题
            - 反馈建议: 可执行改进建议
            - 引用证据: 用于支持判分的原文片段

            要求:
            1. extraction_text 必须是原文精确子串
            2. 得分点和失分点要与题号关联
            3. 不补充原文没有的评分结论
            4. 按原文顺序抽取
            """)

    def get_examples(self) -> List[lx.data.ExampleData]:
        example_text = (
            "第3题：学生答案写出 KCL 方程但符号方向错误。批注：列式思路正确，电流方向统一后可得满分。"
        )

        return [
            lx.data.ExampleData(
                text=example_text,
                extractions=[
                    lx.data.Extraction(
                        extraction_class="题号",
                        extraction_text="第3题",
                        attributes={"类型": "电路分析"}
                    ),
                    lx.data.Extraction(
                        extraction_class="学生答案",
                        extraction_text="写出 KCL 方程但符号方向错误",
                        attributes={"题号": "第3题"}
                    ),
                    lx.data.Extraction(
                        extraction_class="得分点",
                        extraction_text="列式思路正确",
                        attributes={"题号": "第3题"}
                    ),
                    lx.data.Extraction(
                        extraction_class="失分点",
                        extraction_text="符号方向错误",
                        attributes={"题号": "第3题"}
                    ),
                    lx.data.Extraction(
                        extraction_class="反馈建议",
                        extraction_text="电流方向统一后可得满分",
                        attributes={"题号": "第3题"}
                    ),
                ]
            )
        ]

    def get_samples(self) -> List[Dict[str, str]]:
        return [
            {
                "id": "grading_sample_1",
                "title": "电路作业批改记录",
                "text": textwrap.dedent("""\
                    第1题（10分）：学生正确写出戴维宁等效电阻计算步骤，得分点完整，得 10 分。
                    第2题（12分）：学生答案中将电流源置零处理错误，失分点为“未区分独立源与受控源”，得 7 分。

                    教师反馈建议：
                    1. 先检查题目是否含受控源，再决定等效处理方式；
                    2. 每步推导后标注单位，避免后续计算混乱。

                    引用证据：教材第4章“含受控源电路的等效变换”明确指出受控源不能直接置零。
                    """).strip()
            },
            {
                "id": "grading_sample_2",
                "title": "控制课程作业批注",
                "text": textwrap.dedent("""\
                    第5题：学生使用终值定理求稳态误差，方法正确。
                    失分点：未验证闭环系统稳定性就直接套用终值定理。
                    标准答案要求先判稳，再计算误差系数。
                    反馈建议：今后按“判稳-建模-代入”三步作答。
                    """).strip()
            }
        ]
