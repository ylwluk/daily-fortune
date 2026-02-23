# 🐰 每日运势推送系统

基于1987年金牛座，结合生肖五行和星座的每日运势推送服务。

## 功能

- 🎨 每日幸运颜色推荐
- ✅ 宜做事项提示
- ❌ 不宜做事项提醒
- 📊 综合运势评分
- ⚠️ 冲煞提醒

## 技术栈

- Python 3.11
- APScheduler 定时任务
- Server酱 微信推送

## 本地运行

```bash
# 安装依赖
pip install requests APScheduler

# 测试推送
python3 main.py once

# 启动定时任务（保持程序运行）
python3 main.py
```

## GitHub Actions 自动部署

### 步骤1: 创建GitHub仓库

1. 登录 GitHub: https://github.com
2. 点击 "New repository"
3. 仓库名称: `daily-fortune`
4. 选择 "Public"
5. 点击 "Create repository"

### 步骤2: 上传代码

```bash
# 克隆仓库
git clone https://github.com/ylwluk/daily-fortune.git
cd daily-fortune

# 添加所有文件
git add .

# 提交
git commit -m "Initial commit"

# 推送到GitHub
git push origin main
```

### 步骤3: 配置Secrets

1. 进入仓库设置 → Secrets and variables → Actions
2. 点击 "New repository secret"
3. 名称: `SERVERCHAN_KEY`
4. 值: 您的Server酱SendeKey (SCT315905Th32M65fMe0lbAmLMcLrtJ5O6)
5. 点击 "Add secret"

### 步骤4: 验证

1. 进入 Actions 页面
2. 点击 "每日运势推送"
3. 点击 "Run workflow"
4. 确认推送成功

## 推送时间

每天 **21:00** 自动推送第二天的运势

## 用户信息

- 出生年份: 1987年
- 生肖: 兔（火兔/丁卯）
- 五行: 丁火（阴火）
- 星座: 金牛座
- 喜用神: 木、火

---
