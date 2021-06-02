import os
import glob
import dropbox
import subprocess
from dropbox.exceptions import ApiError


class DropboxUtils:

    def __init__(self, access_token):
        self.client = dropbox.Dropbox(access_token)

    def list_files(self, that_dir):
        ls = self.client.files_list_folder(that_dir)
        files = ls.entries

        while ls.has_more:
            ls = self.client.files_list_folder_continue(ls.cursor)
            files += ls.entries

        return files

    def upload_file(self, this_path, that_dir):
        that_files = self.list_files(that_dir)
        that_path = os.path.join(that_dir, os.path.basename(this_path))

        if that_path not in [f.path_display for f in that_files]:
            try:
                self.client.files_upload(open(this_path, 'rb').read(), that_path)
                return True
            except ApiError as e:
                return False
        else:
            return False

    def syncup(self, this_dir, that_dir):
        try:
            that_files = self.list_files(that_dir)
        except ApiError:
            self.client.files_create_folder_v2(that_dir)
            that_files = self.list_files(that_dir)

        this_paths = glob.glob(os.path.expanduser(os.path.join(this_dir, '*')))
        that_paths = [f.path_display for f in that_files]
        for this_path in this_paths:
            that_path = os.path.join(that_dir, os.path.basename(this_path))
            if that_path not in that_paths:
                self.client.files_upload(open(this_path, 'rb').read(), that_path)

    def cleanup(self, this_dir, that_dir):
        try:
            that_files = self.list_files(that_dir)
        except ApiError:
            return

        that_paths = [f.path_display for f in that_files]
        this_paths = glob.glob(os.path.expanduser(os.path.join(this_dir, '*')))
        for this_path in this_paths:
            that_path = os.path.join(that_dir, os.path.basename(this_path))
            if that_path in that_paths:
                subprocess.check_call(f'rm -rf {this_path}', shell=True)

    def syncdown(self, that_dir, this_dir):
        this_dir = os.path.expanduser(this_dir)
        that_files = self.list_files(that_dir)
        that_paths = [f.path_display for f in that_files]
        os.makedirs(this_dir, exist_ok=True)
        this_paths = glob.glob(os.path.join(this_dir, '*'))
        for that_path in that_paths:
            this_path = os.path.join(this_dir, os.path.basename(that_path))
            if this_path not in this_paths:
                with open(this_path, 'wb') as f:
                    metadata, res = self.client.files_download(that_path)
                    f.write(res.content)

    def exists(self, that_path):
        try:
            self.client.files_get_metadata(that_path)
            return True
        except Exception as e:
            return False
