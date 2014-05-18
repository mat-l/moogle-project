import logging
from dropbox.client import DropboxClient  # Dropobox official library

from .response import ApiDropboxResponse
from crawler import AbstractCrawler


log = logging.getLogger('dropbox')


class DropboxCrawler(AbstractCrawler):
    """
    Web crawler to query Dropbox and collect updated files for a `bearertoken`.

    Parameters:
    bearertoken -- a `models.BearerToken`
    """
    def _init_client(self):
        client = DropboxClient(self.bearertoken.access_token)
        updates_cursor = self.bearertoken.updates_cursor

        # Monkey patching the `get` method of client.
        # `AbstractCrawler` expects `client` to be a `request_oauthlib.OAuth1Session` or a
        # `request_oauthlib.OAuth1Session` with a `get` method. Here `client` is a
        # `dropbox.client`, so we monkey patch the `get` method and make it call `delta`.
        def _delta(*args):
            log.debug("Querying DELTA")
            return client.delta(cursor=updates_cursor,)
                                #path_prefix='/temp/moogletest')  # TODO remove the prefix
        client.get = _delta
        return client

    @staticmethod
    def _init_response(*args, **kwargs):
        return ApiDropboxResponse(*args, **kwargs)

    def _hook_after_response_parsed(self, response):
        # Update the cursor.
        self.bearertoken.updates_cursor = response.updates_cursor

    def _build_resource_url(self, pagination_cursor):
        pass