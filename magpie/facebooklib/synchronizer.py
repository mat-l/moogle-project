from .crawler import FacebookCrawler
from .indexer import FacebookIndexer
from utils.db import session_autocommit


class FacebookSynchronizer:
    """

    Parameters:
    bearertoken -- a `BearerToken` owner of the owner of the Facebook account to synchronize with.
    """
    def __init__(self, bearertoken):
        self.bearertoken = bearertoken
        with session_autocommit() as sex:
            # Add bearertoken to the current session.
            bearertoken = sex.merge(self.bearertoken)
            self._bearertoken_id = bearertoken.id
            self._access_token = bearertoken.access_token

    def run(self):
        print(">>>>>> START CRAWLING")
        # `FacebookCrawler` receives a `BearerToken` argument because it needs to update
        # its cursor.
        FacebookCrawler(self.bearertoken).run()
        print(">>>>>> END CRAWLING")

        print("\n\n>>>>>> START INDEXING")
        FacebookIndexer(self._bearertoken_id, self._access_token).run()
        print(">>>>>> END INDEXING")
