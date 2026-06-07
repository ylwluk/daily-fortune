# -*- coding: utf-8 -*-
"""
生肖五行分析模块 - 紫微斗数+黄历融合版
包含：彭祖百忌、建除十二神、六曜、冲煞、纳音五行
"""

import datetime
from config import (
    USER_PROFILE, ZODIAC_CLASH, ZODIAC_HARMONY, ZODIAC_SIX_HARMONY,
    PENGZU_TIANGAN_BAIJI, PENGZU_DIZHI_BAIJI,
    JIANCHU_SHIER, JIANCHU_LUCK, LIUYAO, LIUYAO_MEANING,
    ZIWEI_BASE
)


class MetaphysicsAnalyzer:
    ZODIAC_ELEMENTS = {
        "子": "水", "丑": "土", "寅": "木", "卯": "木",
        "辰": "土", "巳": "火", "午": "火", "未": "土",
        "申": "金", "酉": "金", "戌": "土", "亥": "水"
    }
    HEAVENLY_STEM_ELEMENTS = {
        "甲": "木", "乙": "木", "丙": "火", "丁": "火",
        "戊": "土", "己": "土", "庚": "金", "辛": "金",
        "壬": "水", "癸": "水"
    }
    STEM_YINYANG = {
        "甲": "阳", "乙": "阴", "丙": "阳", "丁": "阴",
        "戊": "阳", "己": "阴", "庚": "阳", "辛": "阴",
        "壬": "阳", "癸": "阴"
    }
    NAYIN_TABLE = {
        "甲子": "海中金", "乙丑": "海中金", "丙寅": "炉中火", "丁卯": "炉中火",
        "戊辰": "大林木", "己巳": "大林木", "庚午": "路旁土", "辛未": "路旁土",
        "壬申": "剑锋金", "癸酉": "剑锋金", "甲戌": "山头火", "乙亥": "山头火",
        "丙子": "涧下水", "丁丑": "涧下水", "戊寅": "城头土", "己卯": "城头土",
        "庚辰": "白蜡金", "辛巳": "白蜡金", "壬午": "杨柳木", "癸未": "杨柳木",
        "甲申": "泉中水", "乙酉": "泉中水", "丙戌": "屋上土", "丁亥": "屋上土",
        "戊子": "霹雳火", "己丑": "霹雳火", "庚寅": "松柏木", "辛卯": "松柏木",
        "壬辰": "长流水", "癸巳": "长流水", "甲午": "沙石金", "乙未": "沙石金",
        "丙申": "山下火", "丁酉": "山下火", "戊戌": "平地木", "己亥": "平地木",
        "庚子": "壁上土", "辛丑": "壁上土", "壬寅": "金泊金", "癸卯": "金泊金",
        "甲辰": "佛灯火", "乙巳": "佛灯火", "丙午": "天河水", "丁未": "天河水",
        "戊申": "大驿土", "己酉": "大驿土", "庚戌": "钗钏金", "辛亥": "钗钏金",
        "壬子": "桑柘木", "癸丑": "桑柘木", "甲寅": "大溪水", "乙卯": "大溪水",
        "丙辰": "沙中土", "丁巳": "沙中土", "戊午": "天上火", "己未": "天上火",
        "庚申": "石榴木", "辛酉": "石榴木", "壬戌": "大海水", "癸亥": "大海水"
    }

    def __init__(self):
        self.user_zodiac = USER_PROFILE["zodiac"]
        self.user_element = USER_PROFILE["element"]
        self.favored_elements = USER_PROFILE["favored_elements"]
        self.avoid_elements = USER_PROFILE["avoid_elements"]
        self.na_yin = USER_PROFILE.get("na_yin", "炉中火")

    def get_daily_ganzhi(self, target_date=None):
        if target_date is None:
            target_date = datetime.date.today() + datetime.timedelta(days=1)
        base_date = datetime.date(1900, 1, 1)
        days_diff = (target_date - base_date).days
        stems = ["甲", "乙", "丙", "丁", "戊", "己", "庚", "辛", "壬", "癸"]
        branches = ["子", "丑", "寅", "卯", "辰", "巳", "午", "未", "申", "酉", "戌", "亥"]
        return stems[days_diff % 10] + branches[days_diff % 12]

    def get_zodiac_from_branch(self, branch):
        return {"子":"鼠","丑":"牛","寅":"虎","卯":"兔","辰":"龙","巳":"蛇","午":"马","未":"羊","申":"猴","酉":"鸡","戌":"狗","亥":"猪"}.get(branch, "")

    def get_jianchu(self, target_date=None):
        if target_date is None:
            target_date = datetime.date.today() + datetime.timedelta(days=1)
        base_date = datetime.date(2024, 2, 4)
        days_diff = (target_date - base_date).days
        return ["建","除","满","平","定","执","破","危","成","收","开","闭"][days_diff % 12]

    def get_liuyao(self, target_date=None):
        if target_date is None:
            target_date = datetime.date.today() + datetime.timedelta(days=1)
        base_date = datetime.date(2024, 1, 1)
        days_diff = (target_date - base_date).days
        return LIUYAO[days_diff % 6]

    def get_nayin(self, ganzhi):
        return self.NAYIN_TABLE.get(ganzhi, "未知")

    def analyze_day(self, target_date=None):
        if target_date is None:
            target_date = datetime.date.today() + datetime.timedelta(days=1)

        ganzhi = self.get_daily_ganzhi(target_date)
        stem, branch = ganzhi[0], ganzhi[1]
        stem_element = self.HEAVENLY_STEM_ELEMENTS.get(stem, "土")
        branch_element = self.ZODIAC_ELEMENTS.get(branch, "土")
        day_element = stem_element
        day_zodiac = self.get_zodiac_from_branch(branch)
        jianchu = self.get_jianchu(target_date)
        liuyao = self.get_liuyao(target_date)
        nayin = self.get_nayin(ganzhi)

        clash_list = ZODIAC_CLASH.get(self.user_zodiac, [])
        harmony_list = ZODIAC_HARMONY.get(self.user_zodiac, [])
        six_harmony = ZODIAC_SIX_HARMONY.get(self.user_zodiac, "")

        is_clash = day_zodiac in clash_list
        is_harmony = day_zodiac in harmony_list
        is_six_harmony = day_zodiac == six_harmony

        jianchu_info = JIANCHU_SHIER.get(jianchu, {"nature": "平常", "yi": [], "ji": []})
        jianchu_luck = JIANCHU_LUCK.get(jianchu, "平")
        liuyao_meaning = LIUYAO_MEANING.get(liuyao, "")
        advice = self._combine_advice(jianchu_info, stem, branch, is_clash, is_harmony)
        lucky_color_suggestion = self._get_lucky_color_suggestion(day_element, is_clash)
        overall_mood = self._get_overall_mood(jianchu_luck, is_clash, is_harmony, is_six_harmony, day_element)

        return {
            "date": target_date.strftime("%Y-%m-%d"),
            "ganzhi": ganzhi, "stem": stem, "branch": branch,
            "stem_element": stem_element, "branch_element": branch_element,
            "day_element": day_element, "day_zodiac": day_zodiac, "nayin": nayin,
            "jianchu": jianchu, "jianchu_nature": jianchu_info["nature"],
            "jianchu_luck": jianchu_luck, "liuyao": liuyao, "liuyao_meaning": liuyao_meaning,
            "is_clash": is_clash, "is_harmony": is_harmony, "is_six_harmony": is_six_harmony,
            "clash_zodiac": day_zodiac if is_clash else None,
            "clash_warning": self._generate_clash_warning(day_zodiac) if is_clash else "",
            "harmony_good": self._generate_harmony_good(day_zodiac) if is_harmony else "",
            "six_harmony_good": self._generate_six_harmony_good(day_zodiac) if is_six_harmony else "",
            "element_analysis": self._analyze_element(day_element, stem),
            "pengzu_tiangan": f"天干{stem}日：{PENGZU_TIANGAN_BAIJI.get(stem, '')}" if PENGZU_TIANGAN_BAIJI.get(stem) else "",
            "pengzu_dizhi": f"地支{branch}日：{PENGZU_DIZHI_BAIJI.get(branch, '')}" if PENGZU_DIZHI_BAIJI.get(branch) else "",
            "advice": advice, "lucky_color_suggestion": lucky_color_suggestion,
            "overall_mood": overall_mood,
            "huotu_tips": self._get_huotu_tips(day_element, is_clash, is_harmony),
            "warnings": self._get_warnings(is_clash, day_element)
        }

    def _analyze_element(self, day_element, stem):
        notes = []
        if day_element in self.favored_elements:
            notes.append(f"今日五行{day_element}与您的喜用神相生，非常有利！")
        elif day_element in self.avoid_elements:
            if day_element == "水": notes.append("今日五行水克火，需注意保持平和心态，避免急躁")
            elif day_element == "土": notes.append("今日五行土泄火，注意休息调养，不宜过度劳累")
        else:
            notes.append(f"今日五行{day_element}，平稳过渡，无特别生克")
        yinyang = self.STEM_YINYANG.get(stem, "")
        if yinyang == "阴": notes.append(f"天干{stem}为阴，利于内敛思考和沉淀，适合学习与规划")
        else: notes.append(f"天干{stem}为阳，利于外在行动和社交，适合拓展与谈判")
        return "".join(notes)

    def _combine_advice(self, jianchu_info, stem, branch, is_clash, is_harmony):
        yi_list = list(jianchu_info.get("yi", []))
        ji_list = list(jianchu_info.get("ji", []))
        tiangan_ji = PENGZU_TIANGAN_BAIJI.get(stem, "").split("，")[-1] if PENGZU_TIANGAN_BAIJI.get(stem) else ""
        dizhi_ji = PENGZU_DIZHI_BAIJI.get(branch, "").split("，")[-1] if PENGZU_DIZHI_BAIJI.get(branch) else ""
        if tiangan_ji: ji_list.append(f"天干忌：{tiangan_ji}")
        if dizhi_ji: ji_list.append(f"地支忌：{dizhi_ji}")
        if is_clash: ji_list.append("今日与您相冲，忌重大决策")
        if is_harmony: yi_list.append("今日三合吉日，运势顺畅")
        return {"宜": list(set(yi_list))[:6], "忌": list(set(ji_list))[:6]}

    def _get_lucky_color_suggestion(self, day_element, is_clash):
        if is_clash: return {"recommended": "绿色系", "reason": "今日相冲，木气助运，稳定心神", "colors": ["绿", "青", "白"]}
        if day_element == "木": return {"recommended": "绿色系（增强木气）", "reason": "今日木气旺盛，绿色增强你的喜用神能量", "colors": ["绿", "青"]}
        elif day_element == "火": return {"recommended": "红色系（增强火气）", "reason": "今日火气旺人，红色助你运势上升", "colors": ["红", "粉", "橙"]}
        elif day_element == "土": return {"recommended": "黄色系（需注意休息）", "reason": "今日土气较重，宜静养，不宜过度操劳", "colors": ["黄", "棕"]}
        elif day_element == "金": return {"recommended": "白色系（金生水）", "reason": "今日金气当令，白色助你财运", "colors": ["白", "金"]}
        elif day_element == "水": return {"recommended": "蓝色系（但需防火）", "reason": "今日水气旺人，蓝色助你平衡，但需注意火邪", "colors": ["蓝", "黑"]}
        return {"recommended": "绿色系（稳定能量）", "reason": "今日五行平稳，绿色带来稳定好运", "colors": ["绿", "青", "白"]}

    def _get_overall_mood(self, jianchu_luck, is_clash, is_harmony, is_six_harmony, day_element):
        if is_clash: base = "今日运势欠佳"
        elif is_six_harmony: base = "今日六合大吉"
        elif is_harmony: base = "今日三合吉庆"
        elif jianchu_luck == "吉": base = "今日黄道吉日"
        elif jianchu_luck == "凶": base = "今日黑道诸事不宜"
        else: base = "今日运势平稳"
        if day_element in self.favored_elements: base += "，喜用神得令，运势加成！"
        elif day_element in self.avoid_elements: base += "，忌神当令，宜静不宜动"
        return base

    def _generate_clash_warning(self, day_zodiac):
        return f"今日{day_zodiac}日，与您的{self.user_zodiac}相冲！建议保持低调，避免重大决策。"
    def _generate_harmony_good(self, day_zodiac):
        return f"今日{day_zodiac}日，与您{self.user_zodiac}三合！三合为三大吉星汇聚，运势亨通，诸事顺遂。"
    def _generate_six_harmony_good(self, day_zodiac):
        return f"今日{day_zodiac}日，与您{self.user_zodiac}六合！六合为阴阳相合，贵人运旺盛。"

    def _get_huotu_tips(self, day_element, is_clash, is_harmony):
        tips = [f"命格：{self.na_yin}，木火为喜，水土为忌", "性格：外柔内刚，富有创造力与直觉力"]
        if is_harmony: tips.append("今日三合，运势极佳，火命人今日特别顺利")
        elif is_clash: tips.append("今日相冲，火命人需特别注意情绪管理，保持平和")
        else: tips.append("今日运势平稳，按部就班即可")
        if day_element == "水": tips.append("今日水气旺人，火命人需注意调节，可多穿红橙色衣物平衡")
        elif day_element == "土": tips.append("今日土气泄火，注意休息，避免过度操劳")
        elif day_element == "木": tips.append("今日木气助火，火命人今日能量充沛，适合开展新项目")
        return tips

    def _get_warnings(self, is_clash, day_element):
        warnings = []
        if is_clash: warnings.extend(["今日与您相冲，请保持低调", "避免在今天做重大决定"])
        if day_element == "水": warnings.append("今日水气较重，注意保暖防寒，心脑血管")
        if day_element == "火": warnings.append("今日火气旺盛，注意降火，多喝水")
        if day_element == "土": warnings.append("今日土气较重，注意脾胃健康")
        return warnings


if __name__ == "__main__":
    analyzer = MetaphysicsAnalyzer()
    result = analyzer.analyze_day()
    print(f"日期: {result['date']}")
    print(f"干支: {result['ganzhi']}（{result['nayin']}）")
    print(f"五行: {result['day_element']}")
    print(f"生肖: {result['day_zodiac']}")
    print(f"建除: {result['jianchu']}（{result['jianchu_nature']}）-{result['jianchu_luck']}")
    print(f"六曜: {result['liuyao']} - {result['liuyao_meaning']}")
    print(f"冲煞: {result['clash_warning'] if result['is_clash'] else '无'}")
    print(f"三合: {result['harmony_good'] if result['is_harmony'] else '无'}")
    print(f"五行分析: {result['element_analysis']}")
    print(f"宜: {result['advice']['宜']}")
    print(f"忌: {result['advice']['忌']}")
    print(f"幸运色: {result['lucky_color_suggestion']}")
    print(f"运势: {result['overall_mood']}")
    print(f"火兔专属: {result['huotu_tips']}")
