import os
import json

class FS:
    def __init__(self):
        self.root = os.path.abspath(os.curdir)
        self.data = os.path.join(self.root, "data")
        self.downloads = os.path.join(self.root, "downloads")
        self.config = self._read_config()
    

    def _read_config(self) -> dict:
        if not os.path.exists(os.path.join(self.data, "config.json")):
            # TODO: Make/Download default config in the future.
            # If download: do it from neatly-stacked-scrolls repo
            pass

        with open(os.path.join(self.data, "config.json"), "r") as f:
            return json.load(f)
    

    def _read_versions(self) -> dict:
        if (url := self.config['version']['src']) == "local":
            with open(os.path.join(self.data, "release-versions.json"), "r") as f:
                return json.load(f)
        else:
            # TODO: Download from url if not local.
            return {}