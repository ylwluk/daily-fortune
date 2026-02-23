# -*- coding: utf-8 -*-
"""
星座运势模块 - 金牛座
基于星座特征生成每日运势
"""

import datetime
import random
from config import USER_PROFILE


class HoroscopeGenerator:
    """金牛座运势生成器"""

    # 金牛座特征
    TAURUS_TRAITS = [
        "稳重踏实", "注重品质", "有耐心", "忠诚可靠",
        "爱好美食", "艺术气质", "固执", "占有欲强"
    ]

    # 金牛座幸运颜色库
    TAURUS_COLORS = [
        "绿色", "粉色", "橙色", "金色", "白色"
    ]

    # 金牛座幸运数字
    TAURUS_NUMBERS = [6, 20, 27, 4, 15]

    # 金牛座宜做事项库
    TAURUS_YI = [
        "整理家居", "品尝美食", "学习新技能", "理财规划",
        "艺术创作", "健身运动", "社交活动", "静心冥想",
        "购物消费", "听音乐", "园艺活动", "烹饪美食"
    ]

    # 金牛座不宜做事项库
    TAURUS_JI = [
        "冒险投资", "冲动消费", "激烈争论", "改变太大",
        "熬夜加班", "轻率做决定", "逃避问题", "过度敏感"
    ]

    # 每日运势模板
    FORTUNE_TEMPLATES = {
        "excellent": [
            "今日运势极佳！金牛的你思维清晰，财运亨通，适合把握机遇。",
            "木星眷顾！今日做任何决定都如有神助，财运和感情运都有提升。",
            "月亮在财帛宫，今天是收获的好日子！"
        ],
        "good": [
            "整体运势良好，保持稳定节奏会遇到更好的机会。",
            "今日适合脚踏实地做事，你的努力会被认可。",
            "社交运不错，可能遇到志同道合的朋友。"
        ],
        "normal": [
            "今日运势平稳，按部就班过好每一天即可。",
            "保持平常心，不要急于求成，好运会在不经意间到来。",
            "今日适合独处思考，给自己一些空间。"
        ],
        "challenging": [
            "今日运势有些低迷，建议保持低调，避免冲突。",
            "可能会遇到一些挑战，保持耐心会帮你度过难关。",
            "注意控制情绪，不要被小事影响心情。"
        ]
    }

    # 颜色对应的元素
    COLOR_ELEMENTS = {
        "绿": "木", "粉": "火", "橙": "火",
        "金": "金", "白": "金", "红": "火",
        "蓝": "水", "黑": "水", "黄": "土"
    }

    def __init__(self):
        self.star_sign = USER_PROFILE["star_sign"]
        self.favored_elements = USER_PROFILE["favored_elements"]

    def get_daily_fortune(self, target_date=None):
        """
        获取指定日期的星座运势
        """
        if target_date is None:
            target_date = datetime.date.today() + datetime.timedelta(days=1)

        # 根据日期生成一个稳定的运势等级
        # 使用日期作为随机种子，确保同一天结果一致
        seed = target_date.year * 10000 + target_date.month * 100 + target_date.day
        random.seed(seed)

        # 运势等级分布
        fortune_level = random.choices(
            ["excellent", "good", "normal", "challenging"],
            weights=[15, 35, 35, 15]
        )[0]

        # 获取运势描述
        fortune_text = random.choice(self.FORTUNE_TEMPLATES[fortune_level])

        # 获取幸运颜色（优先选择与喜用神匹配的颜色）
        lucky_colors = [c for c in self.TAURUS_COLORS
                       if self.COLOR_ELEMENTS.get(c, "") in self.favored_elements]

        if not lucky_colors:
            lucky_colors = self.TAURUS_COLORS

        lucky_color = random.choice(lucky_colors)
        lucky_number = random.choice(self.TAURUS_NUMBERS)

        # 根据运势等级选择宜忌
        if fortune_level == "excellent":
            yi_count = 4
            ji_count = 2
        elif fortune_level == "good":
            yi_count = 3
            ji_count = 2
        elif fortune_level == "normal":
            yi_count = 3
            ji_count = 3
        else:
            yi_count = 2
            ji_count = 4

        lucky_yi = random.sample(self.TAURUS_YI, min(yi_count, len(self.TAURUS_YI)))
        lucky_ji = random.sample(self.TAURUS_JI, min(ji_count, len(self.TAURUS_JI)))

        # 构建结果
        result = {
            "date": target_date.strftime("%Y-%m-%d"),
            "star_sign": self.star_sign,
            "fortune_level": fortune_level,
            "fortune_text": fortune_text,
            "lucky_color": lucky_color,
            "lucky_number": lucky_number,
            "lucky_yi": lucky_yi,
            "lucky_ji": lucky_ji,
            "traits": random.sample(self.TAURUS_TRAITS, 3)
        }

        # 重置随机种子
        random.seed()

        return result

    def get_fortune_score(self, fortune_level):
        """将运势等级转换为分数"""
        scores = {
            "excellent": 90,
            "good": 75,
            "normal": 60,
            "challenging": 45
        }
        return scores.get(fortune_level, 60)


# 测试
if __name__ == "__main__":
    generator = HoroscopeGenerator()
    result = generator.get_daily_fortune()

    print(f"日期: {result['date']}")
    print(f"星座: {result['star_sign']}")
    print(f"运势等级: {result['fortune_level']}")
    print(f"运势描述: {result['fortune_text']}")
    print(f"幸运颜色: {result['lucky_color']}")
    print(f"幸运数字: {result['lucky_number']}")
    print(f"宜: {result['lucky_yi']}")
    print(f"忌: {result['lucky_ji']}")
