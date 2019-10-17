class SeleniumDispatcher:
    def __init__(url: str, download_dir: str = None):
        # set a self variable with selenium instance
        # if download dir, enable downloads in specified directory
        