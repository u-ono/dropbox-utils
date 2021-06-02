import json
import logging
import argparse

from core import DropboxUtils


def upload(access_token, src_dst_map, clean_src_dst=False):

    du = DropboxUtils(access_token)

    for src_dir, dst_dir in src_dst_map:
        du.syncup(src_dir, dst_dir)
        logger.info(f'Synced up, src_dir: {src_dir}, dst_dir: {dst_dir}')
        if clean_src_dst:
            du.cleanup(src_dir, dst_dir)
            logger.info(f'Cleaned up, src_dir: {src_dir}')


if __name__ == '__main__':

    # parser setup
    parser = argparse.ArgumentParser()
    parser.add_argument('-c', '--config-path', type=str, required=True)
    args = parser.parse_args()

    # config setup
    with open(args.config_path, 'r') as f:
        config = json.load(f)

    # logger setup
    logger = logging.getLogger(__name__)
    logger.setLevel(logging.DEBUG)

    formatter = logging.Formatter('%(asctime)s - %(module)s - %(levelname)s - %(message)s')

    file_handler = logging.FileHandler('./syncup.log', mode='a')
    file_handler.setLevel(logging.INFO)
    file_handler.setFormatter(formatter)

    stream_handler = logging.StreamHandler()
    stream_handler.setLevel(logging.DEBUG)
    stream_handler.setFormatter(formatter)

    logger.addHandler(file_handler)
    logger.addHandler(stream_handler)

    # main
    upload(config['access_token'], config['src_dst_map'], config['clean_src_dir'])
