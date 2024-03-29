#    This file is part of DemocraticBot.
#    https://github.com/Nekit10/DemoBot
#
#    DemocraticBot is free software: you can redistribute it and/or modify
#    it under the terms of the GNU General Public License as published by
#    the Free Software Foundation, either version 3 of the License, or
#    (at your option) any later version.
#
#    DemocraticBot is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU General Public License for more details.
#
#    You should have received a copy of the GNU General Public License
#    along with DemocraticBot.  If not, see <https://www.gnu.org/licenses/>.
#
#    Copyright (c) 2019 Nikita Serba

import platform
import sys

from src import demobot, logger
from src.botapi import TelegramBotAPI
from src.sysbugs.bugtrackerapi import report_exception
from src.syslang.langapi import load_chat_langs, msg_version_info

VERSION = '1.0.0-alpha.2'
DEBUG_MODE = True

logger.init()
load_chat_langs()


def log_server_info():
    logger.logger.info('\nPC Specs: ' +
                 '\nMachine: ' + platform.machine() +
                 '\nOS Version: ' + platform.version() +
                 '\nPlatform: ' + platform.platform() +
                 '\nUname: ' + ' '.join(platform.uname()) +
                 '\nSystem: ' + platform.system() +
                 '\nCPU: ' + platform.processor() +
                 '\nPython version: ' + platform.python_version())


if __name__ == '__main__':
    logger.logger.info('Starting bot')

    log_server_info()
    demobot.init_bot(DEBUG_MODE)

    if len(sys.argv) and sys.argv[1] == '--version-notify':
        api = TelegramBotAPI(demobot.config['token'], DEBUG_MODE)
        for chat in api.chats:
            api.send_message(chat, msg_version_info(chat))
        exit(0)

    while True:
        try:
            logger.logger.debug('Running main loop from beginning')
            demobot.main_loop()
        except Exception as e:
            if not DEBUG_MODE:
                logger.logger.warning('Exception (Ignored)! ' + str(e))
                report_exception(e)
                print(str(e))
            else:
                raise e
