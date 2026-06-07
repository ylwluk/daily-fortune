# -*- coding: utf-8 -*-
"""
每日运势推送主程序
每天20:00自动推送第二天运势（苏珊米勒风格 + 紫微斗数黄历）
"""

import datetime
import logging
from apscheduler.schedulers.blocking import BlockingScheduler
from apscheduler.triggers.cron import CronTrigger

from synthesizer import FortuneSynthesizer
from pusher import ServerChanPusher
from config import PUSH_HOUR, PUSH_MINUTE

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


def run_daily_fortune():
    logger.info("=" * 50)
    logger.info("开始生成每日运势...")

    try:
        synthesizer = FortuneSynthesizer()
        report = synthesizer.synthesize()

        logger.info(f"日期: {report['date']} {report['weekday']}")
        logger.info(f"综合评分: {report['final']['score']}/100 {report['horoscope']['fortune_emoji']}")
        logger.info(f"幸运颜色: {report['final']['lucky_color']['color']}")

        pusher = ServerChanPusher()
        title, content, short = pusher.format_fortune_message(report)
        logger.info("消息格式化完成")

        result = pusher.push(title, content, short)

        if result["success"]:
            logger.info(f"推送成功！标题: {title}")
        else:
            logger.error(f"推送失败: {result['message']}")

        logger.info("=" * 50)
        return result

    except Exception as e:
        logger.error(f"生成运势时出错: {str(e)}")
        return {"success": False, "message": str(e)}


def main():
    logger.info("每日运势推送系统启动")
    logger.info(f"推送时间: 每天 {PUSH_HOUR:02d}:{PUSH_MINUTE:02d}")

    scheduler = BlockingScheduler()

    scheduler.add_job(
        run_daily_fortune,
        CronTrigger(hour=PUSH_HOUR, minute=PUSH_MINUTE),
        id='daily_fortune',
        name='每日运势推送',
        replace_existing=True
    )

    logger.info("定时任务已添加")

    try:
        scheduler.start()
    except (KeyboardInterrupt, SystemExit):
        logger.info("系统已停止")
        scheduler.shutdown()


if __name__ == "__main__":
    import sys
    if len(sys.argv) > 1 and sys.argv[1] == "once":
        run_daily_fortune()
    elif len(sys.argv) > 1 and sys.argv[1] == "test":
        run_daily_fortune()
    else:
        main()
