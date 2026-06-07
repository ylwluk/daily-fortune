# -*- coding: utf-8 -*-
"""
星座运势模块 - 金牛座（苏珊米勒风格）
事件导向写法：结合行星相位，给出具体日期建议
覆盖爱情、事业、财运、健康四大维度
"""

import datetime
import random
from config import USER_PROFILE, TAURUS_TRAITS, TAURUS_PLANETS, FORTUNE_LEVELS


class HoroscopeGenerator:
    """金牛座运势生成器 - 苏珊米勒风格"""

    # ============ 金牛座行星知识库 ============
    PLANET_INFLUENCE = {
        "金星": {
            "affects": ["爱情", "金钱", "美", "艺术", "和谐"],
            "good_aspect": "感情升温，财运亨通，适合美容购物",
            "bad_aspect": "易冲动消费，人际摩擦，审美疲劳"
        },
        "火星": {
            "affects": ["行动", "竞争", "冲动", "能量"],
            "good_aspect": "行动力强，果断出击，竞争中胜出",
            "bad_aspect": "易冲动，争吵，意外受伤"
        },
        "木星": {
            "affects": ["幸运", "扩张", "旅行", "高等教育"],
            "good_aspect": "好运降临，机会增多，出行顺利",
            "bad_aspect": "过度乐观，浪费，判断失误"
        },
        "土星": {
            "affects": ["责任", "考验", "延迟", "坚持"],
            "good_aspect": "脚踏实地说服力，稳固人际关系",
            "bad_aspect": "压力增大，阻碍，延迟感"
        },
        "水星": {
            "affects": ["沟通", "学习", "交易", "短途旅行"],
            "good_aspect": "思维清晰，谈判顺利，学习新技能",
            "bad_aspect": "沟通误解，计划延误，电子设备故障"
        }
    }

    # ============ 金牛座幸运数字详解 ============
    TAURUS_NUMBERS = {
        6: "代表和谐与爱，金星数字，带来人际关系的好运",
        20: "金牛座守护数字，强烈吸引正面能量",
        27: "双重金星能量，适合财务决策和艺术创作",
        4: "土星数字，代表稳定与实际，适合长期规划",
        15: "代表智慧与美感，适合学习与创作活动",
        33: "双重金星，高灵性数字，适合心灵成长"
    }

    # ============ 金牛座四大维度宜忌 ============
    TAURUS_LOVE_YI = [
        "共进晚餐", "安排浪漫约会", "送礼物给伴侣", "表达感谢",
        "一起逛家居店", "讨论未来计划", "给伴侣做早餐",
        "改善居家环境", "观看艺术展览", "参加品酒活动"
    ]
    TAURUS_LOVE_JI = [
        "冲动分手", "过度占有", "冷战", "忽视伴侣感受",
        "攀比其他情侣", "过度猜疑", "在经济问题上撒谎"
    ]

    TAURUS_CAREER_YI = [
        "脚踏实地理财", "展示专业能力", "稳扎稳打推进项目",
        "与上司沟通加薪", "学习实用技能", "整理工作环境",
        "谈判合同", "处理积压任务", "建立长期合作关系"
    ]
    TAURUS_CAREER_JI = [
        "冒险投资", "冲动跳槽", "过度攀比职位", "忽视工作细节",
        "轻率做决定", "与同事争执", "超出预算消费"
    ]

    TAURUS_MONEY_YI = [
        "检查财务状况", "制定储蓄计划", "评估投资组合",
        "购买实用物品", "学习理财知识", "清理不必要的支出",
        "稳健投资", "与财务顾问沟通", "规划大额消费"
    ]
    TAURUS_MONEY_JI = [
        "冲动购物", "高风险投资", "借大钱给他人", "忽视账单",
        "攀比消费", "参与赌博", "财务隐瞒"
    ]

    TAURUS_HEALTH_YI = [
        "晨间瑜伽", "健康烹饪", "园林劳动", "散步冥想",
        "规律作息", "体检", "足部按摩", "听舒缓音乐"
    ]
    TAURUS_HEALTH_JI = [
        "熬夜", "暴饮暴食", "久坐不动", "情绪压抑",
        "过度劳累", "忽视身体信号", "激烈运动"
    ]

    # ============ 金牛座苏珊米勒风格文案库 ============
    TAURUS_HOROSCOPE_TEMPLATES = {
        "excellent": {
            "love": [
                "金星与木星形成和谐相位，今天是表白或加深感情的绝佳时机。如果你单身，外出社交会遇到有趣的人。金星在金牛座，你的魅力和审美都处于高峰。",
                "今日感情运极佳，有伴者与伴侣关系更加亲密，单身者可能有意外邂逅。注意把握机遇，但也不要操之过急，顺其自然会有最好的结果。"
            ],
            "career": [
                "火星与金星形成吉相，你的努力正在被看见。今天适合向老板展示你的能力，可能会有意外的好消息。继续保持脚踏实地的风格，成功会自然到来。",
                "事业上有突破性进展，你的创造力和稳定性得到了充分认可。今天是签署重要合同或推进长期项目的好日子。金星照耀，你的专业形象更加突出。"
            ],
            "money": [
                "财务状况看好，木星带来额外的收入机会。可能会有分红、奖金或意外的小财。今天适合做财务规划，但也要注意不要过度消费。",
                "正财运势佳，金星在财帛宫，今天适合评估投资组合或处理财务文件。可能有贵人提供理财建议，带来收益。稳扎稳打是关键。"
            ],
            "health": [
                "身心状态极佳，星星能量让你充满活力。今天适合运动健身或户外活动，身体的灵活性提高。记得多喝水，保持良好的作息习惯。",
                "健康运良好，土星能量让你更加有耐心和毅力，适合开始新的健康计划。今天的感觉特别平和，情绪稳定，是调整身体状态的好时机。"
            ]
        },
        "good": {
            "love": [
                "感情生活平稳，与伴侣相处融洽。今天适合一起做些简单的事，如一起做饭或散步，这比奢华的约会更能加深感情。单身者可以多参加社交活动。",
                "人际关系和谐，金星能量让你更具亲和力。今天在社交场合中会给人留下好印象，可能结识新朋友或有旧友联系。",
                "感情运不错，今天适合和伴侣讨论未来计划，如旅行或搬家等重大决定。单身的金牛座，魅力值上升，可以多外出走走。"
            ],
            "career": [
                "工作进展顺利，你在团队中的价值被认可。今天适合与同事合作或处理文书工作，细节处理得当会让你赢得信任。",
                "事业运良好，保持你一贯的稳定风格就能有所收获。今天不适合冒险，但稳扎稳打的推进会让你的地位更加稳固。",
                "火星带来行动力，今天适合处理之前拖延的工作。你的耐心和专业度会帮助你克服困难。如果有重要的会议，提前准备会让你更有信心。"
            ],
            "money": [
                "财务状况稳定，没有大的支出或收入。今天适合检查账单、规划预算等日常财务管理工作。金星让你在购物时更加明智。",
                "财运中等，需要多加注意支出。今天可能会遇到促销或诱惑，记住只买真正需要的东西。可以考虑学习一些理财知识。",
                "正财稳定，可能有小笔收入。今天适合处理财务文件或与银行打交道。保持记录的好习惯会帮你更好地管理钱财。"
            ],
            "health": [
                "健康状况良好，保持常规的作息和饮食即可。今天适合做一些舒缓的运动，如散步或瑜伽，帮助你放松身心。",
                "身体状态不错，但要注意不要过度劳累。今天的工作量可能较大，记得适时休息。金星能量让你更注重生活质量。",
                "健康运平稳，今天适合检查一下身体状况或预约体检。预防胜于治疗，及早发现问题能更好地处理。"
            ]
        },
        "normal": {
            "love": [
                "感情生活平淡，没有特别的事件。今天适合独处思考，给自己一些空间。如果有伴侣，可以尝试主动做些小事表达关心。",
                "感情运一般，保持平常心即可。今天可能会遇到一些沟通上的小摩擦，及时解释和沟通能避免误会。",
                "今日感情运平稳，单身者可以专注于自我提升。金牛座的你，耐心和稳定是最大的魅力，不必急于求成。"
            ],
            "career": [
                "工作进展按部就班，没有特别的变化。今天适合处理日常事务，保持稳定的节奏即可。避免做出重大决定。",
                "事业运平平，今天可能有些琐碎的工作需要处理。耐心处理这些小事，积累起来会有大的收获。",
                "工作状态一般，需要更多的时间和精力来完成常规任务。今天不适合开展新项目，专注于手头的工作就好。"
            ],
            "money": [
                "财务状况平稳，没有特别的变化。今天适合保守理财，避免冒险或大额支出。保持收支平衡是今天的重点。",
                "财运一般，可能有小的支出或收入。今天不适合做任何重要的财务决策，保持现有的投资组合就好。",
                "财务运平平，今天需要更加注意开支。可能会有些意外的支出，提前做好预算能帮你更好地应对。"
            ],
            "health": [
                "健康状况一般，注意休息和调节。今天可能会有一些小的身体不适，及时调整可以避免更大的问题。",
                "身体状态平稳，不需要特别的关注。今天适合做一些轻松的活动，帮助放松身心。",
                "健康运平平，今天要注意不要给自己太大压力。工作和生活的平衡很重要，适时放松才能保持最佳状态。"
            ]
        },
        "challenging": {
            "love": [
                "感情生活有些紧张，可能与伴侣有摩擦。今天需要更加耐心倾听对方的想法，避免固执己见。金星逆行期间，沟通需要更加谨慎。",
                "今日感情运欠佳，可能会有误会或争执。如果有重要的事需要讨论，建议改天再说。今天更适合独处和反思。",
                "人际关系需要更加小心，今天可能会遇到挑剔或难以相处的人。保持冷静，不要被情绪左右，这是度过今天的最佳方式。"
            ],
            "career": [
                "工作上可能遇到阻碍或延迟，需要更多的耐心。今天不适合做重要的决定或签署文件，可能会遇到意外的变化。",
                "事业运低迷，可能会有压力或批评的声音。今天保持低调，专注于手头的工作，避免与人争执是最好的策略。",
                "工作中可能有小人或阻碍，需要谨慎处理。今天最适合的是做好自己的本职工作，不要参与办公室政治。"
            ],
            "money": [
                "财务状况需要小心，今天可能会有意外支出或财务纠纷。避免做任何投资或购买大件，今天保守为上。",
                "财运欠佳，可能会有财务上的损失或麻烦。今天要特别注意账单和合同，避免被人占便宜。",
                "财务运低迷，今天不适合做任何财务决策。可能会有意外的支出，提前做好心理准备会更从容。"
            ],
            "health": [
                "健康状况需要多加注意，今天可能会感到疲惫或压力较大。注意休息，不要勉强自己。",
                "身体状态欠佳，可能会有小的健康问题。今天要注意饮食和作息，避免过度劳累。",
                "健康运低迷，今天要特别注意情绪管理。可能会有些烦躁或沮丧，及时调整心态很重要。必要时寻求朋友或专业人士的帮助。"
            ]
        },
        "difficult": {
            "love": [
                "感情生活面临重大挑战，可能有分手或重大争执。今天需要格外冷静，任何冲动的决定都可能带来后悔。建议远离重要的人际决策。",
                "今日感情运极差，可能会有严重的误会或冲突。如果可能的话，尽量避免与重要的人长时间相处。今天更适合独处和休息。"
            ],
            "career": [
                "工作上可能遇到重大挫折或阻碍，可能有项目失败或人际冲突。今天保持低调，做好最基本的工作，不要尝试任何冒险。",
                "事业运极差，可能会有裁员或重大调整的消息。今天最重要的是保持冷静，做好自己的本职工作，等待时机好转。"
            ],
            "money": [
                "财务状况危险，今天可能有重大财务损失或纠纷。今天一定要避免任何投资或大额消费，守住自己的钱袋子最重要。",
                "财运极差，可能会有大的支出或财务纠纷。今天不适合做任何财务相关的决定，保持现有的财务状况是最明智的选择。"
            ],
            "health": [
                "健康状况需要特别关注，今天可能会有突发状况或旧病复发。今天不适合做任何冒险的活动，注意安全第一。",
                "健康运极差，今天要特别小心意外或伤害。建议不要进行任何危险的活动，多休息，保持平和的心态。"
            ]
        }
    }

    # ============ 金牛座幸运颜色详解 ============
    TAURUS_COLOR_MEANINGS = {
        "绿": {
            "meaning": "木星色彩，代表成长与繁荣",
            "advice": "特别适合今天的选择，与你的喜用神木相生",
            "best_for": ["事业突破", "学习新技能", "人际拓展"],
            "pair_with": ["青", "白"]
        },
        "粉": {
            "meaning": "金星本色，代表爱情与美",
            "advice": "今天感情运佳，粉色能增强你的魅力",
            "best_for": ["约会", "社交", "艺术创作"],
            "pair_with": ["白", "金"]
        },
        "金": {
            "meaning": "金星与财富的象征",
            "advice": "增强财运的颜色选择",
            "best_for": ["财务决策", "商业谈判", "购物"],
            "pair_with": ["白", "棕"]
        },
        "棕": {
            "meaning": "土象稳重，大地之色彩",
            "advice": "让你更加踏实稳定的选择",
            "best_for": ["重要会议", "谈判", "居家布置"],
            "pair_with": ["绿", "白"]
        },
        "青": {
            "meaning": "木气青色，生机勃勃",
            "advice": "与你的喜用神完全匹配，带来好运",
            "best_for": ["开始新项目", "学习", "健康养生"],
            "pair_with": ["绿", "白"]
        },
        "白": {
            "meaning": "金白之色，纯净高雅",
            "advice": "百搭颜色，让你更加清新脱俗",
            "best_for": ["正式场合", "日常穿搭", "配饰选择"],
            "pair_with": ["金", "粉"]
        }
    }

    def __init__(self):
        self.star_sign = USER_PROFILE["star_sign"]
        self.favored_elements = USER_PROFILE["favored_elements"]
        self.na_yin = USER_PROFILE.get("na_yin", "炉中火")
        self.element = USER_PROFILE["element"]

    def get_daily_fortune(self, target_date=None):
        """
        获取指定日期的苏珊米勒风格星座运势
        """
        if target_date is None:
            target_date = datetime.date.today() + datetime.timedelta(days=1)

        # 使用日期作为随机种子，确保同一天结果一致
        seed = target_date.year * 10000 + target_date.month * 100 + target_date.day
        random.seed(seed)

        # 确定运势等级
        fortune_level = self._determine_fortune_level(target_date)

        # 生成四大维度运势
        love_fortune = self._generate_dimension_fortune("love", fortune_level)
        career_fortune = self._generate_dimension_fortune("career", fortune_level)
        money_fortune = self._generate_dimension_fortune("money", fortune_level)
        health_fortune = self._generate_dimension_fortune("health", fortune_level)

        # 综合运势描述
        overall_text = self._generate_overall_text(fortune_level)

        # 确定幸运颜色
        lucky_color = self._determine_lucky_color(fortune_level)

        # 幸运数字
        lucky_number = self._get_lucky_number(target_date)

        # 金牛座宜忌事项（综合四大维度）
        yi_items = self._get_yi_items(fortune_level)
        ji_items = self._get_ji_items(fortune_level)

        # 金牛座特质
        traits = random.sample(TAURUS_TRAITS, 3)

        # 行星相位提示
        planet_tips = self._get_planet_tips(target_date)

        # 重置随机种子
        random.seed()

        return {
            "date": target_date.strftime("%Y-%m-%d"),
            "star_sign": self.star_sign,
            "fortune_level": fortune_level,
            "fortune_label": FORTUNE_LEVELS[fortune_level]["label"],
            "fortune_emoji": FORTUNE_LEVELS[fortune_level]["emoji"],
            "overall_text": overall_text,
            "love": love_fortune,
            "career": career_fortune,
            "money": money_fortune,
            "health": health_fortune,
            "lucky_color": lucky_color,
            "lucky_number": lucky_number,
            "lucky_yi": yi_items,
            "lucky_ji": ji_items,
            "traits": traits,
            "planet_tips": planet_tips,
            "taurus_advice": self._get_taurus_advice(fortune_level)
        }

    def _determine_fortune_level(self, target_date):
        """根据日期确定运势等级，模拟行星相位影响"""
        seed = target_date.year * 10000 + target_date.month * 100 + target_date.day

        # 运势等级分布（参照苏珊米勒的写作风格）
        weights = [10, 30, 35, 20, 5]  # excellent, good, normal, challenging, difficult
        levels = ["excellent", "good", "normal", "challenging", "difficult"]

        # 根据日期调整权重（月相影响）
        day_of_month = target_date.day
        if day_of_month in [1, 15, 16]:  # 新月和满月附近
            weights = [15, 35, 30, 15, 5]  # 更容易有好运
        elif day_of_month in [8, 22, 23]:  # 弦月附近
            weights = [5, 20, 35, 30, 10]  # 更容易有挑战

        return random.choices(levels, weights=weights)[0]

    def _generate_dimension_fortune(self, dimension, fortune_level):
        """生成单个维度的运势描述"""
        templates = self.TAURUS_HOROSCOPE_TEMPLATES[fortune_level][dimension]
        text = random.choice(templates)

        # 根据运势等级确定建议强度
        if fortune_level in ["excellent", "good"]:
            action = "推荐"
        elif fortune_level == "normal":
            action = "建议"
        else:
            action = "提醒"

        return {
            "text": text,
            "action": action,
            "level": fortune_level
        }

    def _generate_overall_text(self, fortune_level):
        """生成综合运势总结（苏珊米勒风格的温暖收尾）"""
        summaries = {
            "excellent": [
                "亲爱的金牛座，今天是你近期最闪耀的日子！行星能量完美配合，金星、木星都在为你加油。无论你在哪个领域，都有可能收获惊喜。记住，你的耐心和稳定是你最大的武器，继续保持这个风格，成功会自然到来。享受今天，相信自己！",
                "今天是非常好的一天，金牛座的你正站在好运的风口上。木星为你打开了新的可能，金星让你的魅力和财运同时提升。这是一年中为数不多的黄金日，好好把握！但也要记住，幸运也会眷顾有准备的人。"
            ],
            "good": [
                "金牛座，今天的整体运势不错，保持你一贯的稳健风格就能有所收获。行星相位对你友好，尤其是在人际关系和财务方面。不要急于求成，稳扎稳打是今天的关键词。相信你的直觉，你比想象中更有智慧。",
                "今天对你来说是充实的一天，金星和火星的相位为你带来行动力和人缘。可能会有些小惊喜等着你，但最重要的是保持心态的平和。你已经做得很好了，继续前进！"
            ],
            "normal": [
                "金牛座，今天是平稳的一天，没有特别大的起伏，也没有特别的挑战。这正好是整理自己、蓄势待发的好时机。不要急于做任何决定，用这段时间好好思考一下接下来的计划。稳定是你最大的优势。",
                "今天对你来说是普通的一天，但这普通本身就是一种幸福。没有大起大落，正好可以专注于日常的小事。做好手头的工作，享受和家人朋友的相处，这就是今天的最佳策略。"
            ],
            "challenging": [
                "金牛座，今天可能会有一些不如意的事情发生，但不要担心，这只是暂时的。行星相位可能让你感到有些压力或阻碍，但记住，困难是成长的阶梯。你的耐心和坚韧会帮助你度过难关。今天最重要的是保持冷静，不要被情绪左右。",
                "今天对你来说有些挑战，可能会有意外的变化或人际摩擦。但这也是检验你应变能力的机会。不要试图对抗，而是顺其自然地调整。你的韧性是你最大的财富，这段困难时期很快就会过去。"
            ],
            "difficult": [
                "亲爱的金牛座，今天是充满挑战的一天，行星相位对你不太友好。可能会有一些意外或挫折发生，但请记住，这只是黎明前的黑暗。保持低调，做好自己的本职工作，不要做任何冒险的决定。今天最重要的是照顾好自己，寻求朋友和家人的支持。你的坚强会帮你度过这一切。",
                "今天对你来说是困难的一天，可能会有财务损失、人际冲突或健康问题。不要试图强行推进任何事情，守成为上。今天最适合的是休息、反思和寻求支持。你已经经历过很多挑战，你的韧性会帮你度过。今天之后，好运会回来。"
            ]
        }
        return random.choice(summaries[fortune_level])

    def _determine_lucky_color(self, fortune_level):
        """确定幸运颜色，考虑金牛座特质和运势等级"""
        # 金牛座偏好的颜色排序
        taurus_colors = ["绿", "粉", "金", "棕", "青", "白"]

        if fortune_level in ["excellent", "good"]:
            # 运势好时，选择最能增强能量的颜色
            color = random.choice(["绿", "金", "粉"])
        elif fortune_level == "normal":
            color = random.choice(["绿", "青", "白"])
        else:
            # 运势低迷时，选择能带来稳定的颜色
            color = random.choice(["绿", "棕", "白"])

        color_info = self.TAURUS_COLOR_MEANINGS.get(color, {
            "meaning": "稳定能量",
            "advice": "帮助你度过今天的选择",
            "best_for": ["稳定", "平衡"]
        })

        return {
            "color": color,
            "meaning": color_info["meaning"],
            "advice": color_info["advice"],
            "best_for": color_info["best_for"]
        }

    def _get_lucky_number(self, target_date):
        """根据日期确定幸运数字"""
        seed = target_date.year * 10000 + target_date.month * 100 + target_date.day
        random.seed(seed)

        # 选择主幸运数和辅助幸运数
        main_number = random.choice([6, 20, 27])
        secondary_numbers = random.sample([n for n in [4, 15, 33] if n != main_number], 2)

        random.seed()
        return {
            "main": main_number,
            "secondary": secondary_numbers,
            "meaning": self.TAURUS_NUMBERS.get(main_number, "金牛座幸运数字")
        }

    def _get_yi_items(self, fortune_level):
        """获取金牛座今日宜做事项"""
        if fortune_level == "excellent":
            return random.sample(self.TAURUS_LOVE_YI + self.TAURUS_CAREER_YI, 4)
        elif fortune_level == "good":
            return random.sample(self.TAURUS_CAREER_YI + self.TAURUS_MONEY_YI, 3)
        elif fortune_level == "normal":
            return random.sample(self.TAURUS_HEALTH_YI + self.TAURUS_CAREER_YI, 3)
        else:
            return random.sample(self.TAURUS_HEALTH_YI, 2)

    def _get_ji_items(self, fortune_level):
        """获取金牛座今日不宜事项"""
        if fortune_level == "excellent":
            return random.sample(self.TAURUS_CAREER_JI, 2)
        elif fortune_level == "good":
            return random.sample(self.TAURUS_MONEY_JI + self.TAURUS_CAREER_JI, 2)
        elif fortune_level == "normal":
            return random.sample(self.TAURUS_MONEY_JI + self.TAURUS_LOVE_JI, 2)
        else:
            return random.sample(self.TAURUS_LOVE_JI + self.TAURUS_CAREER_JI + self.TAURUS_MONEY_JI, 3)

    def _get_planet_tips(self, target_date):
        """根据日期生成行星相位提示"""
        seed = target_date.year * 10000 + target_date.month * 100 + target_date.day
        random.seed(seed)

        planets = list(self.PLANET_INFLUENCE.keys())
        tips = []

        # 根据日期选择1-2颗行星给出提示
        selected_planets = random.sample(planets, min(2, len(planets)))
        for planet in selected_planets:
            aspect = random.choice(["good", "bad"])
            info = self.PLANET_INFLUENCE[planet]
            tips.append({
                "planet": planet,
                "aspect": aspect,
                "affects": info["affects"],
                "description": info[f"{aspect}_aspect"]
            })

        random.seed()
        return tips

    def _get_taurus_advice(self, fortune_level):
        """获取金牛座专属建议"""
        advice = {
            "excellent": "今天是行动的好日子，金牛座的你已经准备充分了。勇敢踏出第一步，你会发现世界比你想象的更支持你。记住，你值得这份好运！",
            "good": "保持你一贯的稳健风格，今天的你会收获不小。不要害怕展示你的能力，你比竞争对手更有耐心和实力。",
            "normal": "今天适合韬光养晦，不必急于表现。利用这段时间整理思路，为接下来的机遇做好准备。",
            "challenging": "今天需要更多的耐心和智慧。金牛座的你天生韧性十足，相信自己能够度过难关。今天不适合冒险，但适合反思和学习。",
            "difficult": "今天是守成为上的日子。不要试图改变什么，专注于最基本的责任。今天最重要的事是照顾好自己的情绪和身体。"
        }
        return advice.get(fortune_level, "")

    def get_fortune_score(self, fortune_level):
        """将运势等级转换为分数"""
        return FORTUNE_LEVELS[fortune_level]["score_range"][0]


# 测试
if __name__ == "__main__":
    generator = HoroscopeGenerator()
    result = generator.get_daily_fortune()

    print(f"日期: {result['date']}")
    print(f"星座: {result['star_sign']}")
    print(f"运势等级: {result['fortune_level']} - {result['fortune_label']} {result['fortune_emoji']}")
    print(f"\n综合运势:")
    print(result['overall_text'])
    print(f"\n💕 爱情: {result['love']['text']}")
    print(f"💼 事业: {result['career']['text']}")
    print(f"💰 财运: {result['money']['text']}")
    print(f"❤️ 健康: {result['health']['text']}")
    print(f"\n🎨 幸运颜色: {result['lucky_color']['color']} - {result['lucky_color']['meaning']}")
    print(f"📅 幸运数字: {result['lucky_number']['main']}")
    print(f"✅ 宜: {result['lucky_yi']}")
    print(f"❌ 忌: {result['lucky_ji']}")
    if result['planet_tips']:
        print(f"\n🌙 行星提示:")
        for tip in result['planet_tips']:
            print(f"  {tip['planet']}: {tip['description']}")