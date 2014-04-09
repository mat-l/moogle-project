"""
Magpie settings

First set an environment variable like:
    MAGPIE_SETTINGS_MODULE=magpie.settings.local
Then you can import settings in any module, like:
    $ from magpie.settings import settings
"""

from os.path import join, normpath, dirname


BASE_DIR = normpath(dirname(dirname(dirname(__file__))))

DATABASE_NAME = ""
DATABASE_CONNECTION = "sqlite:///{}/magpie.db".format(BASE_DIR)

DATABASE = {
    'ENGINE': 'sqlite:///',
    'NAME': normpath(join(BASE_DIR, 'magpie.db')),
}

# Dropbox
MAX_FILE_SIZE = 10*1024*1024  # 10 MB in bytes
DROPBOX_TEMP_REPO_PATH = normpath(join(BASE_DIR, '_tmp', 'dropbox')),