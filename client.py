from provider import DataProvider
from threading import Thread
from time import time, sleep

class SwipeClient(Thread):
    def __init__(self, provider):
        self.provider = provider

    def run(self):
        while True:
            # Grab an insert the listing
            sleep(self.provider.min_interval)
            posts = self.provider.get_listing()
            if posts:
                self.insert_listing(posts)

            # Update as many outdated posts as we can
            next_poll = time() + self.provider.poll_rate - self.provider.min_interval
            outdated = self.get_outdated()
            for post in outdated:
                if time() >= next_poll: break
                sleep(self.provider.min_interval)
                (id, slug) = post
                rating = self.provider.get_rating(slug)
                if rating:
                    self.insert_rating(id, rating)
        
            # Wait the rest of the poll period if there's still time
            margin = next_poll - time()
            if margin > 0:
                print "Finished poll with", margin, "seconds to spare"
                sleep(margin)
            else:
                print "Ran over time by", -margin, "seconds"

    def insert_listing(self, listing):
        """
        Takes a list of new post tuples from provider.get_listing() and inserts them into the database if they're
        not already being tracked.
        """
        raise NotImplementedError("insert_listing() not implemented")

    def get_outdated(self):
        """
        Gets a list of tuples of (id, slug) whose ratings need to be refreshed.
        """
        raise NotImplementedError("get_outdated() not implemented")

    def insert_rating(self, id, rating):
        """
        Takes a post id and rating and inserts them into the database.
        """
        raise NotImplementedError("insert_rating() not implemented")
         
