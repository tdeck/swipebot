from providers.reddit import RedditProvider

class RedditPicsProvider(RedditProvider):

    def __init__(self):
        self.subreddit = 'pics'

    def is_suitable(self, post):

    def get_hash(self, post):
