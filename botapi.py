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

import json

import requests


class TelegramBotException(Exception):
    pass


class TelegramBotAPI:
    """A set if function that communicate with official Telegram bot api"""
    token: str
    url: str
    offset: int = 934596997

    polls: dict
    _POLLS_FILENAME: str = "polls.json"

    def __init__(self, token: str):
        """
        Create instance of TelegramBotAPI

        Params:
        token: str - your's bot token. You can get it from @BotFather in Telegram
        """

        self.token = token
        self.url = 'https://api.telegram.org/bot' + token
        self.polls = self.load_polls()

    def start_poll(self, chat_id: int, question: str, answers: list) -> dict:
        response = json.loads(requests.get('{}/sendPoll?chat_id={}&question={}%options={}'.format(
            self.url,
            str(chat_id),
            question,
            '[' + ','.join(answers) + ']')).json())

        if not response['ok']:
            raise TelegramBotException(response['description'])

        poll_id = int(response['result']['poll']['id'])
        self.polls[poll_id] = []

        return response

    def send_message(self, chat_id: int, msg: str) -> dict:
        response = json.loads(requests.get('{}/sendMessage?chat_id={}&text={}'.format(
            self.url,
            str(chat_id),
            msg)))

        if not response['ok']:
            raise TelegramBotException(response['description'])

        return response

    def get_new_updates(self) -> dict:
        response = json.loads(requests.get('{}/getUpdates?offset={}'.format(self.url, str(self.offset))))

        self.offset = response['result'][-1]['update_id'] + 1

        if not response['ok']:
            raise TelegramBotException(response['description'])

        self._update_polls(response['result'])

        return response

    def _get_new_updates_without_offset(self) -> dict:
        response = json.loads(requests.get('{}/getUpdates'.format(self.url)))

        if not response['ok']:
            raise TelegramBotException(response['description'])

        return response

    def send_error_message(self, chat_id: int, e: Exception) -> dict:
        return self.send_message(chat_id, 'Error: ' + str(e))

    @staticmethod
    def load_polls() -> dict:
        """Load information about all polls from file"""

        with open(TelegramBotAPI._POLLS_FILENAME) as f:
            return json.loads(f.read())

    def save_polls(self) -> None:
        """Saves information about polls to file"""

        with open(TelegramBotAPI._POLLS_FILENAME) as f:
            f.write(json.dumps(self.polls))

    def get_poll_result(self, poll_id: int) -> dict:
        pass

    def _update_polls(self, updates: list) -> None:
        """Update options of every poll that was updated"""

        pass
