from accounts import TransferListener, IDS
from streamer import TwitterStreamer


def send_tweets_to_slack() -> None:
    stream = TwitterStreamer()
    stream.stream_tweets(listener=TransferListener(), users=list(IDS))


if __name__ == '__main__':
    send_tweets_to_slack()
