from dropbox_utils import __version__
from dropbox_utils import DropboxUtils


def test_version():
    assert __version__ == '0.1.0'


if __name__ == '__main__':

    utils = DropboxUtils('lu0ENCaRQysAAAAAAAAAAfOGHiAfwLOsPq5SJgL_hDdrBupOR-yQph8meQAyOpKm')
    # utils.sync_up('~/playground/synctest/test_b/', '/synctest/test_b')

    # utils.sync_down('/synctest/test_b', '~/playground/syncdowntest/test_b/')

    utils.clean_dir('~/playground/synctest/test_a/', '/synctest/test_a')
