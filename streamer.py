from dataclasses import dataclass
from typing import List, Iterable, Generator

from tweepy import StreamListener, OAuthHandler, Stream, API, Cursor, Status

from twitter import CONSUMER_KEY, CONSUMER_SECRET, ACCESS_TOKEN, ACCESS_TOKEN_SECRET


@dataclass
class Tweet(object):
    text: str
    name: str
    screen_name: str
    id: str
    likes: int
    retweets: int

    def __str__(self) -> str:
        return f'{self.name} @{self.screen_name} tweets:\n\n' \
               f'{self.text}\n\n' \
               f'Retweets {self.retweets} - ' \
               f'Likes {self.likes}'


class StdOutListener(StreamListener):

    def __init__(self):
        super().__init__()

    def on_data(self, data):
        raise NotImplementedError

    def on_error(self, status_code):
        if status_code == 420:
            return False


class TwitterStreamer:

    def stream_tweets(self, listener: StdOutListener, keywords: List[str] = None, users: List[str] = None) -> None:
        auth = authenticate_twitter_app()
        stream = Stream(auth, listener)
        stream.filter(track=keywords, follow=users, is_async=True)


def authenticate_twitter_app() -> OAuthHandler:
    auth = OAuthHandler(consumer_key=CONSUMER_KEY, consumer_secret=CONSUMER_SECRET)
    auth.set_access_token(key=ACCESS_TOKEN, secret=ACCESS_TOKEN_SECRET)
    return auth


class TwitterClient:
    def __init__(self):
        self.auth = authenticate_twitter_app()
        self.twitter_client = API(self.auth)

    def get_twitter_client_api(self) -> API:
        return self.twitter_client

    def get_user_timeline_tweets(self, twitter_user: str, num_tweets: int) -> Generator[Status, None, None]:
        cursor = Cursor(self.twitter_client.user_timeline, id=twitter_user).items(limit=num_tweets)
        return (tweet for tweet in cursor)

    def get_home_timeline_tweets(self, twitter_user: str, num_tweets) -> Generator[Status, None, None]:
        cursor = Cursor(self.twitter_client.home_timeline, id=twitter_user).items(limit=num_tweets)
        return (tweet for tweet in cursor)

    def get_ids_from_usernames(self, twitter_users: Iterable[str]) -> Generator[str, None, None]:
        for twitter_user in twitter_users:
            yield self.twitter_client.get_user(screen_name=twitter_user).id
