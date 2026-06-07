# -*- coding: utf-8 -*-
"""
运势综合分析模块
结合苏珊米勒风格星座运势 + 紫微斗数黄历，生成最终推送内容
"""

import datetime
from config import USER_PROFILE, COLOR_MAPPING, FORTUNE_LEVELS
from metaphysics import MetaphysicsAnalyzer
from horoscope import HoroscopeGenerator


class FortuneSynthesizer:
    def __init__(self):
        self.user = USER_PROFILE
        self.metaphysics = MetaphysicsAnalyzer()
        self.horoscope = HoroscopeGenerator()

    def synthesize(self, target_date=None):
        if target_date is None:
            target_date = datetime.date.today() + datetime.timedelta(days=1)

        meta_result = self.metaphysics.analyze_day(target_date)
        horo_result = self.horoscope.get_daily_fortune(target_date)

        report = {
            "date": target_date.strftime("%Y-%m-%d"),
            "weekday": self._get_weekday(target_date),
            "user_info": self._get_user_summary(),
            "metaphysics": meta_result,
            "horoscope": horo_result,
            "final": self._combine_analysis(meta_result, horo_result)
        }
        return report

    def _get_weekday(self, date):
        return ["周一", "周二", "周三", "周四", "周五", "周六", "周日"][date.weekday()]

    def _get_user_summary(self):
        return {
            "birth_year": self.user["birth_year"],
            "zodiac": self.user["zodiac"],
            "element": self.user["element_detail"],
            "star_sign": self.user["star_sign"],
            "na_yin": self.user.get("na_yin", ""),
            "animal": self.user.get("animal", ""),
            "gender": self.user.get("gender", "")
        }

    def _combine_analysis(self, meta, horo):
        final_color = self._decide_color(meta, horo)
        final_yi = self._combine_yi(meta["advice"]["宜"], horo["lucky_yi"], meta)
        final_ji = self._combine_ji(meta["advice"]["忌"], horo["lucky_ji"], meta)
        summary = self._generate_summary(meta, horo)
        score = self._calculate_score(meta, horo)
        wearing_advice = self._generate_wearing_advice(final_color, meta)

        return {
            "lucky_color": final_color,
            "lucky_number": horo["lucky_number"],
            "do_list": final_yi,
            "dont_list": final_ji,
            "summary": summary,
            "score": score,
            "wearing_advice": wearing_advice,
            "warnings": self._get_warnings(meta)
        }

    def _decide_color(self, meta, horo):
        horo_color = horo["lucky_color"]["color"]
        day_element = meta["day_element"]
        favored = self.user["favored_elements"]

        color_elements = {
            "绿": "木", "粉": "火", "橙": "火", "红": "火",
            "金": "土", "黄": "土", "蓝": "水", "黑": "水", "白": "金", "棕": "土", "青": "木"
        }

        horo_color_element = color_elements.get(horo_color, "")

        if horo_color_element in favored:
            return {
                "color": horo_color,
                "meaning": horo["lucky_color"].get("meaning", ""),
                "reason": f"星座幸运色，与您的喜用神{horo_color_element}相生"
            }

        if day_element in favored:
            element_colors = {"木": ["绿", "青"], "火": ["红", "粉", "橙"], "土": ["黄", "棕"], "金": ["白", "金"], "水": ["蓝", "黑"]}
            suggested = element_colors.get(day_element, ["白"])
            for c in suggested:
                if color_elements.get(c, "") in favored:
                    return {"color": c, "meaning": "", "reason": f"今日五行{day_element}，颜色助运"}

        return {"color": horo_color, "meaning": horo["lucky_color"].get("meaning", ""), "reason": horo["lucky_color"].get("advice", "")}

    def _combine_yi(self, meta_yi, horo_yi, meta):
        combined = list(set(meta_yi + horo_yi))
        if meta.get("is_harmony"): combined.append("今日三合，大胆行动")
        if meta.get("is_six_harmony"): combined.append("今日六合，贵人相助")
        return combined[:6]

    def _combine_ji(self, meta_ji, horo_ji, meta):
        combined = list(set(meta_ji + horo_ji))
        if meta.get("is_clash"):
            combined.append("今日相冲，忌重大决策")
            combined.append("避免冒险投资")
        return combined[:6]

    def _generate_summary(self, meta, horo):
        parts = []
        if meta.get("is_clash"): parts.append("今日相冲，宜守不宜攻")
        elif meta.get("is_harmony"): parts.append("今日三合，运势亨通")
        elif meta.get("is_six_harmony"): parts.append("今日六合，贵人运旺")
        parts.append(horo["overall_text"][:100] + "...")
        if meta.get("is_clash") or horo["fortune_level"] in ["challenging", "difficult"]:
            parts.append("建议保持低调，循序渐进")
        elif meta.get("is_harmony") or horo["fortune_level"] == "excellent":
            parts.append("把握机遇，乘势而上")
        else:
            parts.append("稳中求进，耐心等待")
        return "。".join(parts)

    def _calculate_score(self, meta, horo):
        base_score = 60
        horo_score = self.horoscope.get_fortune_score(horo["fortune_level"])

        if meta.get("is_six_harmony"): meta_bonus = 20
        elif meta.get("is_harmony"): meta_bonus = 15
        elif meta.get("is_clash"): meta_bonus = -15
        elif meta["day_element"] in self.user["favored_elements"]: meta_bonus = 10
        elif meta["day_element"] in self.user["avoid_elements"]: meta_bonus = -10
        else: meta_bonus = 0

        final_score = int((horo_score * 0.6) + (base_score + meta_bonus) * 0.4)
        return max(0, min(100, final_score))

    def _generate_wearing_advice(self, color, meta):
        color_name = color["color"]
        parts = [f"主推颜色：{color_name}"]
        if meta["day_element"] in self.user["favored_elements"]:
            parts.append(f"今日五行{meta['day_element']}旺你，{color_name}让你更幸运")
        elif meta["day_element"] in self.user["avoid_elements"]:
            parts.append(f"今日{color_name}为主，配饰可平衡")
        if color_name in ["绿", "青"]: parts.append("配饰建议：木质手表或绿色包包")
        elif color_name in ["红", "粉", "橙"]: parts.append("配饰建议：金属首饰或红色围巾")
        elif color_name in ["蓝", "黑"]: parts.append("配饰建议：白色或金色配件提亮")
        elif color_name in ["金", "白"]: parts.append("配饰建议：珍珠或银色首饰")
        return " | ".join(parts)

    def _get_warnings(self, meta):
        warnings = []
        if meta.get("is_clash"):
            warnings.append(f"今日{meta['day_zodiac']}日与您相冲，请注意")
            warnings.append("避免在今天做重大决定")
        if meta.get("is_harmony"):
            warnings.append(f"今日{meta['day_zodiac']}日三合，运势极佳")
        if meta["day_element"] == "水": warnings.append("今日水气较重，注意保暖防寒")
        if meta["day_element"] == "火": warnings.append("今日火气旺盛，注意降火")
        if meta["day_element"] == "土": warnings.append("今日土气较重，注意脾胃健康")
        return warnings


if __name__ == "__main__":
    synthesizer = FortuneSynthesizer()
    report = synthesizer.synthesize()
    print(f"日期: {report['date']} {report['weekday']}")
    print(f"用户: {report['user_info']['zodiac']} {report['user_info']['star_sign']} {report['user_info']['na_yin']}")
    print(f"干支: {report['metaphysics']['ganzhi']} ({report['metaphysics']['nayin']})")
    print(f"建除: {report['metaphysics']['jianchu']}（{report['metaphysics']['jianchu_nature']}）")
    print(f"六曜: {report['metaphysics']['liuyao']} - {report['metaphysics']['liuyao_meaning']}")
    print(f"冲煞: {report['metaphysics']['clash_warning'] if report['metaphysics']['is_clash'] else '无'}")
    print(f"幸运色: {report['final']['lucky_color']}")
    print(f"幸运数字: {report['final']['lucky_number']}")
    print(f"综合评分: {report['final']['score']}")
    print(f"宜: {report['final']['do_list']}")
    print(f"忌: {report['final']['dont_list']}")
    print(f"总结: {report['final']['summary']}")
    print(f"穿着: {report['final']['wearing_advice']}")
    if report['final']['warnings']: print(f"提醒: {report['final']['warnings']}")
    print(f"\n星座运势等级: {report['horoscope']['fortune_level']} - {report['horoscope']['fortune_label']}")
    print(f"综合运势: {report['horoscope']['overall_text'][:80]}...")
