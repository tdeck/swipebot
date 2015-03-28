from provider import DataProvider
from hashlib import md5
import json
import urllib2

class RedditProvider(DataProvider):

    def __init__(self, subreddit):
        super(RedditProvider, self).__init__()
        self.subreddit = subreddit
        self.name = 'reddit_' + subreddit

    def is_suitable(self, post):
        """
        Returns a boolean to check whether a given post is suitable for inclusion in the data set
        Default: always true
        """
        return True

    def get_hash(self, post):
        """
        Must return a hash for a given post to uniquely identify the content and match duplicates.
        Default: url based
        """
        return md5(post['data']['url']).hexdigest()

    def get_listing(self):
        try:
            opener = urllib2.build_opener()
            opener.addheaders = [('User-agent', self.user_agent)]
            response = opener.open('http://reddit.com/r/' + self.subreddit + '/new.json?limit=100')
            posts = json.load(response, encoding='UTF-8')['data']['children']

            return [
                (
                    post['data']['id'], 
                    post['data']['title'], 
                    self.get_hash(post), 
                    int(post['data']['created_utc'])
                )
                for post in posts if post['kind'] == 't3' and self.is_suitable(post)
            ]
        except:
            return None

    def get_rating(self, slug):
        try:
            opener = urllib2.build_opener()
            opener.addheaders = [('User-agent', self.user_agent)]
            response = opener.open('http://reddit.com/r/' + self.subreddit + '/by_id/t3_' + slug + '.json')
            info = json.load(response, encoding='UTF-8')['data']['children'][0]['data']
            return (info['ups'], info['downs'])
        except:
            return None
