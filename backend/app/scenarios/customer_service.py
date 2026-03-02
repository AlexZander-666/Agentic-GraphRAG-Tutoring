"""答疑对话提取场景"""

import textwrap
from typing import Dict, List

import langextract as lx

from app.scenarios.base import BaseScenario


class CustomerServiceScenario(BaseScenario):
    """答疑对话提取场景（保留 customer_service 场景 ID 以兼容现有接口）"""

    name = "答疑对话"
    description = "从师生问答记录中提取问题焦点、证据引用和后续学习行动，支持教学导学闭环"
    extract_classes = ["学生问题", "澄清信息", "知识点定位", "解题思路", "引用证据", "未解决问题", "后续行动"]

    def get_prompt(self) -> str:
        return textwrap.dedent("""\
            从答疑对话中提取以下信息:

            - 学生问题: 学生提出的核心问题
            - 澄清信息: 教师追问或学生补充条件
            - 知识点定位: 对应章节、定理或公式
            - 解题思路: 教师给出的解题路径
            - 引用证据: 教材/讲义中的支持片段
            - 未解决问题: 当前对话未闭环的问题
            - 后续行动: 建议的练习或复习任务

            要求:
            1. extraction_text 必须是原文精确子串
            2. 区分“学生表述”与“教师建议”
            3. 引用证据应保留章节或定位信息（若原文包含）
            4. 按对话时间顺序抽取
            """)

    def get_examples(self) -> List[lx.data.ExampleData]:
        example_text = (
            "学生：为什么我的节点方程总是少一个未知量？教师：先确认参考节点是否唯一。"
            "请回看教材3.2节，并完成第12题。"
        )

        return [
            lx.data.ExampleData(
                text=example_text,
                extractions=[
                    lx.data.Extraction(
                        extraction_class="学生问题",
                        extraction_text="为什么我的节点方程总是少一个未知量",
                        attributes={"角色": "学生"}
                    ),
                    lx.data.Extraction(
                        extraction_class="解题思路",
                        extraction_text="先确认参考节点是否唯一",
                        attributes={"角色": "教师"}
                    ),
                    lx.data.Extraction(
                        extraction_class="引用证据",
                        extraction_text="教材3.2节",
                        attributes={"类型": "教材定位"}
                    ),
                    lx.data.Extraction(
                        extraction_class="后续行动",
                        extraction_text="完成第12题",
                        attributes={"时限": "课后"}
                    ),
                ]
            )
        ]

    def get_samples(self) -> List[Dict[str, str]]:
        return [
            {
                "id": "qa_dialog_sample_1",
                "title": "电路答疑记录",
                "text": textwrap.dedent("""\
                    学生：我在叠加定理这题里算出的电流比标准答案大一倍，不知道错在哪里。
                    教师：请先说明你是否把受控源也置零了？
                    学生：是的，我把所有源都置零了。
                    教师：这里需要澄清，只有独立源置零，受控源必须保留。
                    引用证据：教材第4章第2节“受控源处理规则”。
                    后续行动：重做习题 4-8 与 4-9，并在明天晚自习前提交更正过程。
                    """).strip()
            },
            {
                "id": "qa_dialog_sample_2",
                "title": "控制理论答疑记录",
                "text": textwrap.dedent("""\
                    学生：终值定理什么时候不能用？
                    教师：闭环不稳定时不能直接使用，需要先做稳定性判断。
                    知识点定位：第5章“稳态误差与终值定理”。
                    未解决问题：你对“闭环极点位置与稳定性关系”还不熟悉。
                    后续行动：先复习劳斯判据，再完成课后第5、6题。
                    """).strip()
            }
        ]
