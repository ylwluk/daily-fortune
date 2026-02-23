# -*- coding: utf-8 -*-
"""
运势综合分析模块
结合生肖五行和星座运势，生成最终推送内容
"""

import datetime
from config import USER_PROFILE, COLOR_MAPPING
from metaphysics import MetaphysicsAnalyzer
from horoscope import HoroscopeGenerator


class FortuneSynthesizer:
    """运势综合分析器"""

    def __init__(self):
        self.user = USER_PROFILE
        self.metaphysics = MetaphysicsAnalyzer()
        self.horoscope = HoroscopeGenerator()

    def synthesize(self, target_date=None):
        """
        综合分析生成每日运势报告
        """
        if target_date is None:
            target_date = datetime.date.today() + datetime.timedelta(days=1)

        # 获取各方运势数据
        meta_result = self.metaphysics.analyze_day(target_date)
        horo_result = self.horoscope.get_daily_fortune(target_date)

        # 综合分析
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
        """获取星期几"""
        weekdays = ["周一", "周二", "周三", "周四", "周五", "周六", "周日"]
        return weekdays[date.weekday()]

    def _get_user_summary(self):
        """获取用户基本信息摘要"""
        return {
            "birth_year": self.user["birth_year"],
            "zodiac": self.user["zodiac"],
            "element": self.user["element_detail"],
            "star_sign": self.user["star_sign"]
        }

    def _combine_analysis(self, meta, horo):
        """
        综合分析，生成最终结论
        """
        # 1. 确定幸运颜色
        final_color = self._decide_color(meta, horo)

        # 2. 确定宜做事项（综合黄历和星座）
        final_yi = self._combine_yi(meta["advice"]["宜"], horo["lucky_yi"])

        # 3. 确定不宜做事项
        final_ji = self._combine_ji(meta["advice"]["忌"], horo["lucky_ji"], meta)

        # 4. 确定运势总结
        summary = self._generate_summary(meta, horo)

        # 5. 计算综合运势评分
        score = self._calculate_score(meta, horo)

        # 6. 穿着建议
        wearing_advice = self._generate_wearing_advice(final_color, meta, horo)

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
        """
        确定最终幸运颜色
        原则：优先考虑喜用神，然后是星座运势
        """
        horo_color = horo["lucky_color"]
        day_element = meta["day_element"]
        favored = self.user["favored_elements"]

        # 颜色对应的元素
        color_elements = {
            "绿": "木", "粉": "火", "橙": "火", "红": "火",
            "金": "金", "白": "金", "黄": "土", "蓝": "水", "黑": "水"
        }

        # 获取星座颜色的元素
        horo_color_element = color_elements.get(horo_color, "")

        # 如果星座幸运色与喜用神匹配，直接使用
        if horo_color_element in favored:
            return {
                "color": horo_color,
                "reason": f"星座幸运色，与您的喜用神{horo_color_element}相生"
            }

        # 如果当日五行与喜用神匹配，选择匹配的颜色
        if day_element in favored:
            # 根据当日五行推荐颜色
            element_colors = {
                "木": ["绿", "青"],
                "火": ["红", "粉", "橙"],
                "土": ["黄", "棕"],
                "金": ["白", "金"],
                "水": ["蓝", "黑"]
            }
            suggested = element_colors.get(day_element, ["白"])
            # 选择一个与喜用神匹配的颜色
            for c in suggested:
                if color_elements.get(c, "") in favored:
                    return {
                        "color": c,
                        "reason": f"今日五行{day_element}，颜色助运"
                    }

        # 默认返回星座幸运色，但添加建议
        return {
            "color": horo_color,
            "reason": f"今日幸运色，建议搭配{favored[0]}色配饰增强运势" if favored else ""
        }

    def _combine_yi(self, meta_yi, horo_yi):
        """
        综合黄历宜和星座宜
        """
        # 合并去重，保留6条
        combined = list(set(meta_yi + horo_yi))
        # 优先保留黄历宜
        combined = meta_yi + [y for y in combined if y not in meta_yi]
        return combined[:6]

    def _combine_ji(self, meta_ji, horo_ji, meta):
        """
        综合黄历忌和星座忌
        """
        combined = list(set(meta_ji + horo_ji))

        # 如果有冲煞，添加提醒
        if meta.get("is_clash"):
            combined.append("避免重大决策")

        return combined[:6]

    def _generate_summary(self, meta, horo):
        """
        生成运势总结
        """
        parts = []

        # 生肖五行总结
        if meta.get("is_harmony"):
            parts.append("今日三合，运势亨通")
        elif meta.get("is_clash"):
            parts.append("今日相冲，宜守不宜攻")
        else:
            parts.append(meta["element_analysis"])

        # 星座总结
        parts.append(horo["fortune_text"])

        # 综合判断
        if meta.get("is_clash") or horo["fortune_level"] == "challenging":
            parts.append("建议保持低调，循序渐进")
        elif meta.get("is_harmony") or horo["fortune_level"] == "excellent":
            parts.append("把握机遇，乘势而上")
        else:
            parts.append("稳中求进，耐心等待")

        return "。".join(parts)

    def _calculate_score(self, meta, horo):
        """
        计算综合运势评分
        """
        # 基础分数
        base_score = 60

        # 星座运势分数
        horo_score = self.horoscope.get_fortune_score(horo["fortune_level"])

        # 生肖五行调整
        if meta.get("is_harmony"):
            meta_bonus = 15
        elif meta.get("is_clash"):
            meta_bonus = -15
        elif meta["day_element"] in self.user["favored_elements"]:
            meta_bonus = 10
        elif meta["day_element"] in self.user["忌用元素"]:
            meta_bonus = -10
        else:
            meta_bonus = 0

        # 计算最终分数
        final_score = int((horo_score * 0.6) + (60 + meta_bonus) * 0.4)
        final_score = max(0, min(100, final_score))  # 限制在0-100

        return final_score

    def _generate_wearing_advice(self, color, meta, horo):
        """
        生成穿着建议
        """
        color_name = color["color"]
        advice_parts = []

        advice_parts.append(f"主推颜色：{color_name}")

        # 根据五行提供建议
        if meta["day_element"] in self.user["favored_elements"]:
            advice_parts.append(f"今日五行{meta['day_element']}旺你，{color_name}让你更幸运")
        elif meta["day_element"] in self.user["忌用元素"]:
            advice_parts.append("注意调节，{color_name}为主，配件可平衡")

        # 添加配饰建议
        if color_name in ["绿", "青"]:
            advice_parts.append("配饰建议：木质手表或绿色包包")
        elif color_name in ["红", "粉", "橙"]:
            advice_parts.append("配饰建议：金属首饰或红色围巾")
        elif color_name in ["蓝", "黑"]:
            advice_parts.append("配饰建议：白色或金色配件提亮")

        return " | ".join(advice_parts)

    def _get_warnings(self, meta):
        """
        获取需要提醒的事项
        """
        warnings = []

        if meta.get("is_clash"):
            warnings.append(f"⚠️ 今日{meta['day_zodiac']}日与您相冲，请注意")
            warnings.append("❌ 避免在今天做重大决定")
            warnings.append("❌ 尽量不要与属鸡的人发生冲突")

        if meta["day_element"] == "水":
            warnings.append("⚠️ 今日水气较重，注意保暖防寒")

        if meta["day_element"] == "火":
            warnings.append("⚠️ 今日火气旺盛，注意降火")

        return warnings


# 测试
if __name__ == "__main__":
    synthesizer = FortuneSynthesizer()
    report = synthesizer.synthesize()

    print(f"日期: {report['date']} {report['weekday']}")
    print(f"用户: {report['user_info']['zodiac']} {report['user_info']['star_sign']}")
    print(f"干支: {report['metaphysics']['ganzhi']}")
    print(f"五行: {report['metaphysics']['day_element']}")
    print(f"幸运色: {report['final']['lucky_color']}")
    print(f"幸运数字: {report['final']['lucky_number']}")
    print(f"综合评分: {report['final']['score']}")
    print(f"宜: {report['final']['do_list']}")
    print(f"忌: {report['final']['dont_list']}")
    print(f"总结: {report['final']['summary']}")
    print(f"穿着: {report['final']['wearing_advice']}")
    if report['final']['warnings']:
        print(f"提醒: {report['final']['warnings']}")
