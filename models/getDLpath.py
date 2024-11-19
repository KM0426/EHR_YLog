import os
def get_user_download_folder():
    # ユーザーフォルダのパスを取得
    user_folder = os.path.expanduser("~")
    folder = os.path.join(user_folder, "Downloads")
    
    return folder