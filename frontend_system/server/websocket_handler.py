
from frontend_system.integration.realtime_feed import RealtimeFeed

class WebsocketLikeHandler:
    def __init__(self, feed: RealtimeFeed):
        self.feed = feed
