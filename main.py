# -*- coding: utf-8 -*-
"""
每日运势推送主程序
每天21:00自动推送第二天运势
"""

import datetime
import time
import logging
from apscheduler.schedulers.blocking import BlockingScheduler
from apscheduler.triggers.cron import CronTrigger

from synthesizer import FortuneSynthesizer
from pusher import ServerChanPusher
from config import PUSH_HOUR, PUSH_MINUTE

# 配置日志
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


def run_daily_fortune():
    """
    执行每日运势推送
    """
    logger.info("=" * 50)
    logger.info("开始生成每日运势...")

    try:
        # 1. 生成运势报告
        synthesizer = FortuneSynthesizer()
        report = synthesizer.synthesize()

        logger.info(f"日期: {report['date']} {report['weekday']}")
        logger.info(f"幸运颜色: {report['final']['lucky_color']['color']}")
        logger.info(f"综合评分: {report['final']['score']}/100")

        # 2. 格式化消息
        pusher = ServerChanPusher()
        title, content, short = pusher.format_fortune_message(report)

        logger.info("消息格式化完成")

        # 3. 发送推送
        result = pusher.push(title, content, short)

        if result["success"]:
            logger.info(f"✅ 推送成功！")
            logger.info(f"   标题: {title}")
        else:
            logger.error(f"❌ 推送失败: {result['message']}")

        logger.info("=" * 50)
        return result

    except Exception as e:
        logger.error(f"❌ 生成运势时出错: {str(e)}")
        return {"success": False, "message": str(e)}


def test_push():
    """
    测试推送功能
    """
    logger.info("开始测试推送...")
    return run_daily_fortune()


def main():
    """
    主函数 - 启动定时调度器
    """
    logger.info("🚀 每日运势推送系统启动")
    logger.info(f"⏰ 推送时间: 每天 {PUSH_HOUR:02d}:{PUSH_MINUTE:02d}")

    # 创建调度器
    scheduler = BlockingScheduler()

    # 添加定时任务 (每天21:00执行)
    scheduler.add_job(
        run_daily_fortune,
        CronTrigger(hour=PUSH_HOUR, minute=PUSH_MINUTE),
        id='daily_fortune',
        name='每日运势推送',
        replace_existing=True
    )

    logger.info("✅ 定时任务已添加")

    try:
        # 启动调度器
        scheduler.start()
    except (KeyboardInterrupt, SystemExit):
        logger.info("系统已停止")
        scheduler.shutdown()


if __name__ == "__main__":
    # 如果直接运行，则执行测试推送
    import sys

    if len(sys.argv) > 1 and sys.argv[1] == "test":
        # 测试模式
        test_push()
    elif len(sys.argv) > 1 and sys.argv[1] == "once":
        # 单次执行模式
        run_daily_fortune()
    else:
        # 调度器模式
        main()
