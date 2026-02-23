# -*- coding: utf-8 -*-
"""
Server酱微信推送模块
"""

import requests
from config import SERVERCHAN_KEY, COLOR_MAPPING


class ServerChanPusher:
    """Server酱微信推送器"""

    API_URL = "https://sctapi.ftqq.com/{sckey}.send"

    def __init__(self, sckey=None):
        self.sckey = sckey or SERVERCHAN_KEY

    def push(self, title, content, short_content=None):
        """
        发送微信推送

        Args:
            title: 推送标题
            content: 推送内容（Markdown格式）
            short_content: 简短内容摘要

        Returns:
            dict: 推送结果
        """
        url = self.API_URL.format(sckey=self.sckey)

        data = {
            "title": title,
            "desp": content,
        }

        if short_content:
            data["short"] = short_content[:50]

        try:
            response = requests.post(url, data=data, timeout=10)
            result = response.json()

            if result.get("code") == 0:
                return {
                    "success": True,
                    "message": "推送成功",
                    "data": result
                }
            else:
                return {
                    "success": False,
                    "message": f"推送失败: {result.get('msg', '未知错误')}",
                    "data": result
                }
        except Exception as e:
            return {
                "success": False,
                "message": f"推送异常: {str(e)}",
                "data": None
            }

    def format_fortune_message(self, report):
        """
        格式化运势报告为Markdown消息
        """
        date = report["date"]
        weekday = report["weekday"]
        meta = report["metaphysics"]
        horo = report["horoscope"]
        final = report["final"]

        # 获取颜色信息
        color_name = final["lucky_color"]["color"]
        color_info = COLOR_MAPPING.get(color_name, {"color": "#FFFFFF", "rgb": "255,255,255"})

        # 运势等级
        level_emoji = {
            "excellent": "🌟🌟🌟🌟🌟",
            "good": "🌟🌟🌟🌟",
            "normal": "🌟🌟🌟",
            "challenging": "🌟🌟"
        }
        level_text = {
            "excellent": "大吉",
            "good": "吉",
            "normal": "平",
            "challenging": "欠佳"
        }

        emoji = level_emoji.get(horo["fortune_level"], "🌟🌟🌟")
        level = level_text.get(horo["fortune_level"], "平")

        # 构建消息
        message = f"""# 🔮 每日运势提醒

**📅 {date} {weekday}**

---

## 👤 您的基本信息

- **生肖**: {report['user_info']['zodiac']}
- **星座**: {report['user_info']['star_sign']}
- **五行**: {report['user_info']['element']}

---

## 📊 今日运势

**综合评分**: {final['score']}/100 {emoji}

### 干支信息
- **干支**: {meta['ganzhi']}
- **当日五行**: {meta['day_element']}
- **当日生肖**: {meta['day_zodiac']}

{f"### ⚠️ 冲煞提醒\n{meta['clash_warning']}\n" if meta.get("clash_warning") else ""}
{f"### ✨ 运势提示\n{meta['harmony_good']}\n" if meta.get("harmony_good") else ""}

---

## 👗 穿衣指南

### 🎨 幸运颜色: **{color_name}**

> {final['lucky_color']['reason']}

{final['wearing_advice']}

---

## ✅ 宜做事项

{chr(10).join(['- ' + item for item in final['do_list']])}

---

## ❌ 不宜做事项

{chr(10).join(['- ' + item for item in final['dont_list']])}

---

## 💡 运势总结

{final['summary']}

---

*🐰 火兔每日运势 | 每日21:00自动推送*
"""

        # 标题
        title = f"📅 {date} 运势提醒 | {level}"

        # 简短摘要
        short = f"幸运色{color_name} | 评分{final['score']}/100 | {level}"

        return title, message, short


# 测试
if __name__ == "__main__":
    from synthesizer import FortuneSynthesizer

    # 生成报告
    synthesizer = FortuneSynthesizer()
    report = synthesizer.synthesize()

    # 推送
    pusher = ServerChanPusher()
    title, content, short = pusher.format_fortune_message(report)

    print("标题:", title)
    print("\n内容预览:")
    print(content[:500])
    print("\n...")
