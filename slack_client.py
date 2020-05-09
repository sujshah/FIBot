import time
from asyncio import Future
from typing import Union

from slack.errors import SlackApiError
from slack.web.client import WebClient
from slack.web.slack_response import SlackResponse

from twitter import SLACK_BOT_TOKEN

CHANNEL = '#football-transfer-alerts'


class SlackClient:
    def __init__(self):
        self.client = WebClient(token=SLACK_BOT_TOKEN)

    def _raw_send_slack_message(self, channel: str, message: str) -> Union[Future, SlackResponse]:
        return self.client.chat_postMessage(
            channel=channel,
            text=message,
        )

    def send_slack_message(self, channel: str, message: str) -> Union[Future, SlackResponse]:
        while True:
            try:
                return self._raw_send_slack_message(channel, message)
            except SlackApiError as e:
                if e.response["error"] == "ratelimited":
                    delay = int(e.response.headers['Retry-After'])
                    print(f"Rate limited. Retrying in {delay} seconds")
                    time.sleep(delay)
                    return self._raw_send_slack_message(channel, message)
                else:
                    # other errors
                    raise e
