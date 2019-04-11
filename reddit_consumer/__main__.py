from time import sleep

from reddit_consumer.reddit import get_subreddit, extract_comment
from tqdm import tqdm
from praw.exceptions import APIException, ClientException
import fire

class StreamConsumer:

    def __init__(self):
        self.sub = get_subreddit()
        self.retries = 10
        self.delay_before_retry = 360 # seconds

    def stdout(self):
        try:
            for c in tqdm(self.sub.stream.comments()):
                print(extract_comment(c))
        except KeyboardInterrupt:
            print('\nShutting down..')
    
    def redis(self):
        try:
            for c in tqdm(self.sub.stream.comments()):
                print(extract_comment(c))
        except APIException as e:
            print(e, )
            self._retry()
        except ClientException as e:
            self._retry()
    
    def _retry(self):
        if self.retries == 0:
            exit(0)
        self.retries -= 1
        sleep(self.delay_before_retry)
        self.redis()
        


def main():
    fire.Fire(StreamConsumer)

if __name__ == "__main__":
    main()
