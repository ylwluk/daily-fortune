# -*- coding: utf-8 -*-
"""
生肖五行分析模块
分析每日与用户生肖五行的关系
"""

import datetime
from config import USER_PROFILE, ZODIAC_CLASH, ZODIAC_HARMONY


class MetaphysicsAnalyzer:
    """生肖五行分析器"""

    # 地支对应的五行
    ZODIAC_ELEMENTS = {
        "子": "水", "丑": "土", "寅": "木", "卯": "木",
        "辰": "土", "巳": "火", "午": "火", "未": "土",
        "申": "金", "酉": "金", "戌": "土", "亥": "水"
    }

    # 天干对应的五行
    HEAVENLY_STEM_ELEMENTS = {
        "甲": "木", "乙": "木", "丙": "火", "丁": "火",
        "戊": "土", "己": "土", "庚": "金", "辛": "金",
        "壬": "水", "癸": "水"
    }

    # 每日吉凶宜忌 (简化版黄历)
    DAILY_Advice = {
        "子日": {"宜": ["祭祀", "沐浴", "扫舍", "整手足甲"], "忌": ["动土", "破土", "安葬"]},
        "丑日": {"宜": ["祭祀", "祈福", "求嗣", "开光"], "忌": ["开市", "交易", "立券"]},
        "寅日": {"宜": ["纳财", "开仓", "出货财", "入学"], "忌": ["栽种", "牧养"]},
        "卯日": {"宜": ["嫁娶", "纳采", "订盟", "会亲友"], "忌": ["祈福", "求嗣"]},
        "辰日": {"宜": ["订盟", "纳采", "冠笄", "竖柱"], "忌": ["开市", "交易"]},
        "巳日": {"宜": ["塑绘", "会友", "习艺", "入学"], "忌": ["造屋", "起基"]},
        "午日": {"宜": ["祭祀", "祈福", "求嗣", "斋醮"], "忌": ["开市", "立券", "交易"]},
        "未日": {"宜": ["嫁娶", "纳采", "订盟", "会亲友"], "忌": ["动土", "破土"]},
        "申日": {"宜": ["纳财", "开仓", "出货财", "赴任"], "忌": ["词讼", "安门"]},
        "酉日": {"宜": ["祭祀", "祈福", "求嗣", "开光"], "忌": ["出行", "移徙"]},
        "戌日": {"宜": ["会亲友", "订盟", "纳采", "竖柱"], "忌": ["开市", "交易"]},
        "亥日": {"宜": ["沐浴", "剃头", "整手足甲", "扫舍"], "忌": ["开市", "交易", "立券"]}
    }

    def __init__(self):
        self.user_zodiac = USER_PROFILE["zodiac"]
        self.user_element = USER_PROFILE["element"]
        self.favored_elements = USER_PROFILE["favored_elements"]
        self.忌用元素 = USER_PROFILE["忌用元素"]

    def get_daily_ganzhi(self, target_date=None):
        """
        获取指定日期的干支纪年
        使用简化算法（基于1900年为庚子年）
        """
        if target_date is None:
            target_date = datetime.date.today() + datetime.timedelta(days=1)

        # 基准日期: 1900-01-01 为庚子年
        base_date = datetime.date(1900, 1, 1)
        days_diff = (target_date - base_date).days

        # 天干循环 (0-9)
        stems = ["庚", "辛", "壬", "癸", "甲", "乙", "丙", "丁", "戊", "己"]
        stem = stems[days_diff % 10]

        # 地支循环 (0-11)
        branches = ["子", "丑", "寅", "卯", "辰", "巳", "午", "未", "申", "酉", "戌", "亥"]
        branch = branches[days_diff % 12]

        return stem + branch

    def get_zodiac_from_branch(self, branch):
        """根据地支获取对应生肖"""
        zodiac_map = {
            "子": "鼠", "丑": "牛", "寅": "虎", "卯": "兔",
            "辰": "龙", "巳": "蛇", "午": "马", "未": "羊",
            "申": "猴", "酉": "鸡", "戌": "狗", "亥": "猪"
        }
        return zodiac_map.get(branch, "")

    def analyze_day(self, target_date=None):
        """
        分析指定日期的运势
        返回分析结果字典
        """
        if target_date is None:
            target_date = datetime.date.today() + datetime.timedelta(days=1)

        ganzhi = self.get_daily_ganzhi(target_date)
        stem = ganzhi[0]
        branch = ganzhi[1]

        # 获取当日五行
        stem_element = self.HEAVENLY_STEM_ELEMENTS.get(stem, "土")
        branch_element = self.ZODIAC_ELEMENTS.get(branch, "土")
        day_element = stem_element  # 以天干五行作为当日主导五行

        # 获取当日生肖
        day_zodiac = self.get_zodiac_from_branch(branch)

        # 分析结果
        result = {
            "date": target_date.strftime("%Y-%m-%d"),
            "ganzhi": ganzhi,
            "day_element": day_element,
            "day_zodiac": day_zodiac,
            "is_clash": False,
            "is_harmony": False,
            "clash_warning": "",
            "harmony_good": "",
            "element_analysis": "",
            "advice": {"宜": [], "忌": []},
            "lucky_color_suggestion": "",
            "overall_mood": ""
        }

        # 1. 检查冲煞
        if day_zodiac in ZODIAC_CLASH.get(self.user_zodiac, []):
            result["is_clash"] = True
            result["clash_warning"] = f"⚠️ 今日{day_zodiac}日，与您的{self.user_zodiac}相冲！建议保持低调，避免重大决策"

        # 2. 检查三合
        if day_zodiac in ZODIAC_HARMONY.get(self.user_zodiac, []):
            result["is_harmony"] = True
            result["harmony_good"] = f"✨ 今日{day_zodiac}日，与您{self.user_zodiac}三合，运势顺畅！"

        # 3. 五行分析
        element_notes = []
        if day_element in self.favored_elements:
            element_notes.append(f"今日五行{day_element}，与您的喜用神相生，非常有利！")
        elif day_element in self.忌用元素:
            if day_element == "水":
                element_notes.append("⚠️ 今日五行水克火，需注意保持平和心态")
            elif day_element == "土":
                element_notes.append("⚠️ 今日五行土泄火，注意休息调养")
        else:
            element_notes.append(f"今日五行{day_element}，平稳过渡")

        result["element_analysis"] = "".join(element_notes)

        # 4. 获取基础宜忌
        base_advice = self.DAILY_Advice.get(branch, {"宜": ["祭祀", "祈福"], "忌": ["动土", "破土"]})
        result["advice"] = base_advice

        # 5. 幸运颜色建议
        if day_element == "木":
            result["lucky_color_suggestion"] = "绿色系（增强木气）"
        elif day_element == "火":
            result["lucky_color_suggestion"] = "红色系（增强火气）"
        elif day_element == "土":
            result["lucky_color_suggestion"] = "黄色系（需注意休息）"
        elif day_element == "金":
            result["lucky_color_suggestion"] = "白色系（金生水）"
        elif day_element == "水":
            result["lucky_color_suggestion"] = "蓝色系（但需防火）"

        # 6. 整体运势判断
        if result["is_harmony"]:
            result["overall_mood"] = "⭐⭐⭐⭐⭐ 运势大吉"
        elif result["is_clash"]:
            result["overall_mood"] = "⭐⭐ 运势欠佳"
        elif day_element in self.favored_elements:
            result["overall_mood"] = "⭐⭐⭐⭐ 运势良好"
        else:
            result["overall_mood"] = "⭐⭐⭐ 运势平稳"

        return result


# 测试
if __name__ == "__main__":
    analyzer = MetaphysicsAnalyzer()
    result = analyzer.analyze_day()
    print(f"日期: {result['date']}")
    print(f"干支: {result['ganzhi']}")
    print(f"五行: {result['day_element']}")
    print(f"生肖: {result['day_zodiac']}")
    print(f"冲煞: {result['clash_warning']}")
    print(f"三合: {result['harmony_good']}")
    print(f"五行分析: {result['element_analysis']}")
    print(f"宜: {result['advice']['宜']}")
    print(f"忌: {result['advice']['忌']}")
    print(f"幸运色: {result['lucky_color_suggestion']}")
    print(f"运势: {result['overall_mood']}")
