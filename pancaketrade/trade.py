import logging
import sys

import click
from loguru import logger

from pancaketrade.utils.config import read_config
from pancaketrade.utils.generic import InterceptHandler
from pancaketrade.persistence.models import db
from pancaketrade.bot import TradeBot

logger.remove()
logger.add(
    sys.stderr,
    format="<d>{time:YYYY-MM-DD HH:mm:ss}</> <lvl>{level: ^8}</>|<lvl><n>{message}</n></lvl>",
    level='DEBUG',
    backtrace=False,
    diagnose=False,
    colorize=True,
)
logging.getLogger("apscheduler.executors.default").setLevel("WARNING")
logging.basicConfig(handlers=[InterceptHandler()], level=0)


@click.command()
@click.argument('config_file', required=False, default='config.yml')
def main(config_file: str) -> None:
    try:
        config = read_config(config_file)
        bot = TradeBot(config=config)
        logger.info(bot)
        logger.info('Bot started')
    finally:
        db.close()


if __name__ == '__main__':
    main()
