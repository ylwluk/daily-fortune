# -*- coding: utf-8 -*-
"""
Server酱微信推送模块
"""

import requests
from config import SERVERCHAN_KEY, COLOR_MAPPING


class ServerChanPusher:
    API_URL = "https://sctapi.ftqq.com/{sckey}.send"

    def __init__(self, sckey=None):
        self.sckey = sckey or SERVERCHAN_KEY

    def push(self, title, content, short_content=None):
        url = self.API_URL.format(sckey=self.sckey)
        data = {"title": title, "desp": content}
        if short_content:
            data["short"] = short_content[:50]

        try:
            response = requests.post(url, data=data, timeout=10)
            result = response.json()
            if result.get("code") == 0:
                return {"success": True, "message": "推送成功", "data": result}
            else:
                return {"success": False, "message": f"推送失败: {result.get('msg', '未知错误')}", "data": result}
        except Exception as e:
            return {"success": False, "message": f"推送异常: {str(e)}", "data": None}

    def format_fortune_message(self, report):
        date = report["date"]
        weekday = report["weekday"]
        meta = report["metaphysics"]
        horo = report["horoscope"]
        final = report["final"]

        level_emoji = horo["fortune_emoji"]
        level_label = horo["fortune_label"]

        color_name = final["lucky_color"]["color"]
        color_info = COLOR_MAPPING.get(color_name, {"color": "#10B981", "rgb": "16, 185, 129"})

        newline = "\n"

        message = f"""# 🐰 每日运势提醒

**📅 {date} {weekday}**

---

## 👤 命格信息

- **生肖**: {report['user_info']['zodiac']}（{report['user_info'].get('animal', '')}）
- **星座**: {report['user_info']['star_sign']}
- **纳音**: {report['user_info'].get('na_yin', '')}
- **五行**: {report['user_info']['element']}

---

## ⭐ 综合运势

**综合评分**: {final['score']}/100 {level_emoji} **{level_label}**

### 苏珊米勒今日提示

{horo['overall_text']}

---

## 📊 四大维度运势

### 💕 爱情
{horo['love']['text']}

### 💼 事业
{horo['career']['text']}

### 💰 财运
{horo['money']['text']}

### ❤️ 健康
{horo['health']['text']}

---

## 📅 干支黄历信息

- **干支**: {meta['ganzhi']}（{meta['nayin']}）
- **天干五行**: {meta['stem_element']} | **地支五行**: {meta['branch_element']}
- **建除**: {meta['jianchu']}（{meta['jianchu_nature']}）- {meta['jianchu_luck']}
- **六曜**: {meta['liuyao']} - {meta['liuyao_meaning']}

{f"### ⚠️ 冲煞提醒\n{meta['clash_warning']}\n" if meta.get("clash_warning") else ""}
{f"### ✨ 三合吉兆\n{meta['harmony_good']}\n" if meta.get("harmony_good") else ""}
{f"### 💫 六合吉兆\n{meta['six_harmony_good']}\n" if meta.get("six_harmony_good") else ""}

{f"### 🔮 五行分析\n{meta['element_analysis']}\n" if meta.get("element_analysis") else ""}

{f"### 📜 彭祖百忌\n{meta['pengzu_tiangan']}\n{meta['pengzu_dizhi']}\n" if meta.get("pengzu_tiangan") or meta.get("pengzu_dizhi") else ""}

---

## 👗 穿衣指南

### 🎨 幸运颜色: **{color_name}**

> {final['lucky_color'].get('reason', '')}

{final['wearing_advice']}

---

## ✅ 宜做事项

{newline.join(['- ' + item for item in final['do_list']])}

---

## ❌ 不宜做事项

{newline.join(['- ' + item for item in final['dont_list']])}

---

## 💡 运势总结

{final['summary']}

---

{f"## ⚠️ 特别提醒\n{newline.join(['- ' + w for w in final['warnings']])}\n" if final['warnings'] else ""}

*🐰 火兔每日运势 | 金牛座守护 | 每日20:00自动推送*
"""

        title = f"📅 {date} 运势提醒 | {level_label} | 幸运色{color_name}"

        short = f"幸运色{color_name} | 评分{final['score']}/100 | {level_label}"

        return title, message, short


if __name__ == "__main__":
    from synthesizer import FortuneSynthesizer
    synthesizer = FortuneSynthesizer()
    report = synthesizer.synthesize()
    pusher = ServerChanPusher()
    title, content, short = pusher.format_fortune_message(report)
    print("标题:", title)
    print("\n内容预览:")
    print(content[:800])
    print("\n...")
