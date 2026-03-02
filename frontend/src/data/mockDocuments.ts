export const mockDocuments = {
  contract: {
    title: '电路分析教材节选',
    content: `电路分析课程讲义（节选）

章节：第四章 叠加定理与戴维宁等效
核心概念：在线性电路中，多个独立电源共同作用的响应，等于各独立电源单独作用响应的代数和。

定义与定理
1. 叠加定理只适用于线性网络。
2. 含受控源电路中，受控源不能直接置零。
3. 将独立电压源置零时可等效为短路，将独立电流源置零时可等效为开路。

关键公式
- 节点方程矩阵形式：G·V = I
- 戴维宁等效电压：Vth = Voc
- 戴维宁等效电阻：Rth = Voc / Isc（在满足测量条件时）

适用条件
- 网络由线性元件组成；
- 分析目标为电压或电流响应；
- 参数在分析区间内可视为常数。

常见错误提示
很多同学在受控源场景中直接将全部源置零，导致计算结果看似合理但逻辑不成立。`,
    extracted: {
      entities: [
        { type: '章节', value: '第四章 叠加定理与戴维宁等效', role: '课程章节', highlight: '第四章 叠加定理与戴维宁等效' },
        { type: '定理', value: '叠加定理', role: '核心定理', highlight: '叠加定理只适用于线性网络' },
        { type: '适用条件', value: '线性网络', role: '定理前提', highlight: '叠加定理只适用于线性网络' },
        { type: '概念', value: '受控源', role: '关键概念', highlight: '含受控源电路中，受控源不能直接置零' },
        { type: '公式', value: 'G·V = I', role: '节点方程', highlight: '节点方程矩阵形式：G·V = I' },
        { type: '公式', value: 'Vth = Voc', role: '等效电压公式', highlight: '戴维宁等效电压：Vth = Voc' },
        { type: '公式', value: 'Rth = Voc / Isc', role: '等效电阻公式', highlight: '戴维宁等效电阻：Rth = Voc / Isc' },
        { type: '结论', value: '受控源不能直接置零', role: '错误规避结论', highlight: '受控源不能直接置零' },
      ],
      relationships: [
        { from: '叠加定理', to: '线性网络', type: '适用于', strength: 0.96 },
        { from: '受控源', to: '受控源不能直接置零', type: '约束', strength: 0.94 },
        { from: '节点方程', to: 'G·V = I', type: '表达式', strength: 0.9 },
        { from: '戴维宁等效', to: 'Vth = Voc', type: '计算', strength: 0.88 },
        { from: '戴维宁等效', to: 'Rth = Voc / Isc', type: '计算', strength: 0.88 },
      ],
    },
  },
  research: {
    title: '工程习题讲解记录',
    content: `题目：已知串联 RL 电路中 R=10Ω，L=0.2H，角频率 ω=50rad/s，求阻抗幅值与相角。

解题过程
已知条件：
- R=10Ω
- L=0.2H
- ω=50rad/s

目标：
1. 计算阻抗幅值 |Z|
2. 计算相角 φ

约束条件：
- 采用稳态正弦响应模型；
- 元件视为理想线性元件。

公式：
|Z|=√(R²+(ωL)²)
φ=arctan(ωL/R)

中间推导：
ωL=10Ω
|Z|=√(10²+10²)=14.14Ω
φ=arctan(1)=45°

结论：
该电路阻抗幅值约为 14.14Ω，相角为 45°。`,
    extracted: {
      entities: [
        { type: '已知条件', value: 'R=10Ω', role: '电阻参数', highlight: 'R=10Ω' },
        { type: '已知条件', value: 'L=0.2H', role: '电感参数', highlight: 'L=0.2H' },
        { type: '已知条件', value: 'ω=50rad/s', role: '频率参数', highlight: 'ω=50rad/s' },
        { type: '目标', value: '计算阻抗幅值 |Z|', role: '求解目标', highlight: '计算阻抗幅值 |Z|' },
        { type: '目标', value: '计算相角 φ', role: '求解目标', highlight: '计算相角 φ' },
        { type: '约束条件', value: '稳态正弦响应模型', role: '模型约束', highlight: '采用稳态正弦响应模型' },
        { type: '公式', value: '|Z|=√(R²+(ωL)²)', role: '阻抗公式', highlight: '|Z|=√(R²+(ωL)²)' },
        { type: '公式', value: 'φ=arctan(ωL/R)', role: '相角公式', highlight: 'φ=arctan(ωL/R)' },
        { type: '中间推导', value: 'ωL=10Ω', role: '中间计算', highlight: 'ωL=10Ω' },
        { type: '结论', value: '|Z|=14.14Ω', role: '最终结果', highlight: '|Z|=√(10²+10²)=14.14Ω' },
        { type: '结论', value: 'φ=45°', role: '最终结果', highlight: 'φ=arctan(1)=45°' },
      ],
      relationships: [
        { from: 'R=10Ω', to: '|Z|=√(R²+(ωL)²)', type: '代入', strength: 0.9 },
        { from: 'L=0.2H', to: '|Z|=√(R²+(ωL)²)', type: '代入', strength: 0.9 },
        { from: 'ω=50rad/s', to: 'φ=arctan(ωL/R)', type: '代入', strength: 0.9 },
        { from: '稳态正弦响应模型', to: '公式', type: '适用前提', strength: 0.86 },
        { from: '中间推导', to: '结论', type: '得到', strength: 0.92 },
      ],
    },
  },
  medical: {
    title: '学生学习日志',
    content: `学习日志（电路分析）

本周学习目标：掌握节点电压法与戴维宁等效的使用边界。

错题复盘：
1. 在第4章练习题中，我遗漏了“线性网络”这个适用条件，导致结论逻辑错误。
2. 在含受控源题目里，我把受控源错误置零，造成结果偏差。

错误归因：
- 做题时只关注数值计算，忽略了前提条件检查；
- 没有先写“已知-目标-约束”清单。

纠正策略：
- 每天完成 5 道条件判断题；
- 每次解题前先写出适用条件；
- 每晚 20 分钟复盘错题并标注错因。

掌握度变化：
章节小测正确率从 62% 提升到 83%。

下一步计划：
周末完成 2 套综合题，重点训练受控源与等效变换。`,
    extracted: {
      entities: [
        { type: '学习目标', value: '掌握节点电压法与戴维宁等效的使用边界', role: '阶段目标', highlight: '本周学习目标：掌握节点电压法与戴维宁等效的使用边界' },
        { type: '错误类型', value: '遗漏适用条件', role: '错题类型', highlight: '遗漏了“线性网络”这个适用条件' },
        { type: '错误类型', value: '受控源错误置零', role: '错题类型', highlight: '把受控源错误置零' },
        { type: '错误归因', value: '忽略前提条件检查', role: '认知归因', highlight: '忽略了前提条件检查' },
        { type: '纠正策略', value: '每天完成 5 道条件判断题', role: '训练策略', highlight: '每天完成 5 道条件判断题' },
        { type: '纠正策略', value: '每晚 20 分钟复盘错题', role: '复盘策略', highlight: '每晚 20 分钟复盘错题并标注错因' },
        { type: '掌握度变化', value: '正确率从 62% 提升到 83%', role: '成效指标', highlight: '章节小测正确率从 62% 提升到 83%' },
        { type: '下一步计划', value: '完成 2 套综合题', role: '后续行动', highlight: '周末完成 2 套综合题' },
      ],
      relationships: [
        { from: '遗漏适用条件', to: '逻辑错误', type: '导致', strength: 0.9 },
        { from: '受控源错误置零', to: '结果偏差', type: '导致', strength: 0.9 },
        { from: '纠正策略', to: '正确率从 62% 提升到 83%', type: '提升', strength: 0.86 },
        { from: '学习目标', to: '下一步计划', type: '指导', strength: 0.84 },
      ],
    },
  },
};
