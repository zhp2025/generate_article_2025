import json
import re
import demjson3

def extract_and_parse_json(response: str) -> dict:
    """
    从响应文本中提取JSON代码块并进行解析。
    
    参数:
    - response: 模型的响应文本

    返回:
    - 合并后的JSON对象（如果提取成功），否则抛出解析错误。
    """
    json_objects = []
    
    # 1. 如果文本中根本没有 ```json，则直接尝试解析整个文本
    if "```json" not in response:
        try:
            return json.loads(response)
        except json.JSONDecodeError:
            # 如果内置json解析失败，则尝试demjson3
            try:
                return demjson3.decode(response)
            except demjson3.JSONError:
                raise ValueError("无法解析JSON响应(既不符合标准JSON，也无法宽松解析)。")
    
    # 2. 如果文本中有 ```json，则正则提取所有代码块
    try:
        json_blocks = re.findall(r"```json(.*?)```", response, re.DOTALL)
    except Exception as e:
        print(f"提取JSON时出错: {e}")
        print(f"当前响应文本:\n{response}")
        # 再次尝试原始的整体JSON解析
        try:
            return json.loads(response)
        except json.JSONDecodeError:
            # 如果内置json解析失败，则尝试demjson3
            try:
                return demjson3.decode(response)
            except demjson3.JSONError:
                raise ValueError("无法解析JSON响应(既不符合标准JSON，也无法宽松解析)。")

    # 3. 逐块解析
    for block in json_blocks:
        block = block.strip()
        if not block:
            continue
        try:
            # 优先使用标准json
            json_object = json.loads(block)
            json_objects.append(json_object)
        except json.JSONDecodeError:
            # 如果失败，用demjson3做第二次解析
            try:
                json_object = demjson3.decode(block)
                json_objects.append(json_object)
            except demjson3.JSONError:
                print("无法解析以下JSON片段:\n", block)

    if not json_objects:
        print(f"当前响应文本:\n{response}")
        raise ValueError("响应中未找到有效的JSON片段，或所有片段均解析失败。")

    # 4. 如果只找到一个JSON对象，直接返回；如果有多个，则合并它们
    if len(json_objects) == 1:
        return json_objects[0]
    else:
        # 合并多个JSON对象
        merged_json = {}
        for obj in json_objects:
            # 如果obj本身不是dict，需要根据实际需求决定如何处理。
            # 这里假设所有都是dict，可以直接 .update() 合并
            if isinstance(obj, dict):
                merged_json.update(obj)
            else:
                # 如果不是dict，则根据需求自己处理，这里仅做示例
                merged_json["non_dict_items"] = merged_json.get("non_dict_items", [])
                merged_json["non_dict_items"].append(obj)
        return merged_json


if __name__ == "__main__":
    test_str = """
    {
  "target_audience": {
    "25-35岁职场新人": "缺乏商务场合礼仪知识影响职业发展",
    "40-50岁企业家": "需要建立符合东方文化特色的商务礼仪体系",
    "18-22岁大学生": "求职面试及社交场合缺乏得体礼仪指导",
    "家庭教育从业者": "需系统化传统文化素材开展礼仪教育",
    "外企中国区管理者": "需平衡中西礼仪差异提升团队管理",
    "新婚家庭主妇": "处理复杂家族关系时欠缺传统礼节认知",
    "传统文化爱好者": "渴望系统学习中华礼仪文化精髓",
    "海外华人家庭": "需要传承中华礼仪但缺乏实用指南",
    "服务行业从业者": "提升客户接待礼仪规范与细节把控",
    "退休老干部": "希望系统梳理传统礼仪知识传承后代"
  },
  "key_selling_points": {
    "文化溯源体系": "从《论语》到孟母三迁的典故考据，建立礼仪文化认知坐标系",
    "场景化操作指南": "185个细分场景涵盖居家/会客/宴饮/职场等全场景",
    "视觉化教学系统": "39幅手绘插画构建沉浸式学习场景，还原传统礼仪场景",
    "代际传承方法论": "独创家风养成七步法，解决现代家庭礼仪教育痛点",
    "东西方礼仪对照": "特别标注国际交往中的文化差异处理要点",
    "职场进阶秘籍": "包含12种商务接待核心礼仪与8大谈判座次原则",
    "新媒体时代礼仪": "新增微信礼仪/视频会议礼仪等数字化场景指南",
    "古礼今用转化": "将"安位"传统转化为现代会议座次安排SOP",
    "形象管理法则": "从服饰搭配到仪态管理的18个关键细节标准",
    "应急处理预案": "包含21种社交尴尬场景的化解技巧与话术",
    "家风建设工具包": "提供家庭礼仪教育的30天实践计划表",
    "文化自信构建": "通过礼仪认知重塑当代中国人的文化身份认同"
  },
  "article_structure": {
    "痛点解决型": "场景痛点描述+传统文化智慧+现代解决方案+效果承诺",
    "文化自信型": "文明传承意义+文化断代危机+本书修复价值+案例实证",
    "对比解析型": "中西礼仪差异对比+典型冲突案例+本书调和方案",
    "场景矩阵型": "家庭/职场/商务/涉外四大场景痛点+对应章节指引",
    "代际传承型": "祖辈智慧失传现状+家风建设方案+亲子共读建议",
    "权威背书型": "孔子/孟子等先贤语录+现代专家解读+实操案例验证",
    "视觉化导览": "重点插图解析+场景还原+行为指导要点提炼",
    "成长见证体": "素人学习日记+行为改变轨迹+关键章节指引"
  },
  "language_style": {
    "文化浸润型": "「当孟母三迁的智慧穿越千年，在本书第78页与您的育儿困惑相遇」",
    "权威专业型": "「北大礼仪研究中心数据显示：83%的商务合作失败源于座次失误，本书第三章提供完整解决方案」",
    "场景共鸣型": "「年终酒会上，那个因为坐错位置被冷落的年轻人，后来在本书102页找到了答案」",
    "数据实证型": "「185个场景覆盖率达98%的日常礼仪需求，39幅插画使学习效率提升60%」",
    "代际对话型": "「爷爷抽屉里的老礼单看不懂？本书用37页图解带您解密传统婚嫁礼仪」",
    "痛点刺激型": "「您可能不知道：一次错误的茶杯摆放正在影响客户的合作意愿」",
    "文化自信型": "「这不是繁文缛节，而是流淌在血脉里的文明密码」",
    "亲切实用型": "「明天要见未来公婆？立即翻到第156页获取传统拜见礼仪三步法」",
    "视觉化引导": "「跟随第24页的插画指引，三步掌握得体拱手礼的正确姿势」",
    "悬念制造型": "「乾隆皇帝用哪三个礼仪细节判断臣子忠诚度？答案藏在第二章插画中」"
  }
}
"""

    print(extract_and_parse_json(test_str))
    