class DataProvider(object):
    """
    An abstract class.
    """

    name = 'default'            # Also used for table prefixes
    user_agent = 'swipebot/1.0' # Used in all HTTP headers
    poll_rate = 300             # Poll for new posts every 5 minutes
    track_rate = 3600 * 2       # Check up on posts every 2 hours
    track_periods = 24          # Check for up to 48 hours after posting
    min_interval = 3            # Minimum request delay in seconds

    def get_listing(self):
        """
        Must return a list of tuples of (slug, title, content_hash, posted) or None on error
        """
        raise NotImplementedError("get_listing() not implemented")

    def get_rating(self, slug):
        """
        Must accept a slug and return a tuple of (upvotes, downvotes) or None on error
        """
        raise NotImplementedError("get_rating() not implemented")
