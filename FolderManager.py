#FolderManager.py
import os

# Covers helper functions for CRUD of folders
class FolderManager:
    def __init__(self, root_dir):
        self.root_dir = root_dir

    # Handles folder creation helpers
    def create_folder(self, folder_name):
        new_folder_path = os.path.join(self.root_dir, folder_name)
        print("Create Folder: ", new_folder_path)
        if not os.path.exists(new_folder_path):
            os.makedirs(new_folder_path)
            return True
        else:
            return False

    # Handles folder renaming helpers
    def rename_folder(self, old_path, new_path):
        if not os.path.exists(new_path):
            os.rename(old_path, new_path)
            return True
        else:
            return False
    
    # Handles folder deletion helpers
    def delete_folder(self, path):
        try:
            if os.path.exists(path):
                os.rmdir(path)
                return True
            return False
        except OSError:
            return False