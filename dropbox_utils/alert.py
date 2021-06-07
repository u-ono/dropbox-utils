import os
import json
import datetime
import argparse
from notipy.clients import SlackClient

from core import DropboxUtils


if __name__ == '__main__':

    # parser setup
    parser = argparse.ArgumentParser()
    parser.add_argument('-c', '--config-path', type=str, required=True)
    args = parser.parse_args()

    # config setup
    with open(args.config_path, 'r') as f:
        config = json.load(f)

    now = datetime.datetime.now()
    target_date = now - datetime.timedelta(hours=1)
    file = target_date.strftime(config['name_format'])

    backup_dirs = config['backup_dirs']

    du = DropboxUtils(config['access_token'])
    slack = SlackClient(config['slack']['token'], config['slack']['channel'])

    for backup_dir in backup_dirs:
        path = os.path.join(backup_dir, file)
        if not du.exists(path):
            slack.send(f'File {path} not found.')
        else:
            print(f'File {path} found.')
