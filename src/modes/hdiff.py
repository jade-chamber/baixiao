import os

from ..utils.download import Download
from ..utils.logger import Logger

class Hdiff(Download):
    def __init__(self, branch):
        self.logger = Logger("Hdiff", "#fbf3b6", 1)
        super().__init__(branch, self.logger)
        self.hdiff_info = self.branch_info['hdiff']
    

    def _build_url(self, info):
        return f"{self.config['downloads']['base_url']}client_app/update/hk4e_global/10/{info}"
    

    def download_hdiff(self):
        files = []

        data = self.hdiff_info['data']
        files.append({
            "name": f"{data}.zip",
            "url": self._build_url(f"{data}.zip"),
            "path": os.path.join(self.fs.downloads, self.branch, "hdiff", f"{data}")
        })

        voice_pack_data = self.hdiff_info['voice_packs']
        for language in voice_pack_data:
            files.append({
                "name": f"{voice_pack_data[language]}.zip",
                "url": self._build_url(f"{voice_pack_data[language]}.zip"),
                "path": os.path.join(self.fs.downloads, self.branch, "hdiff", "voice_pack", voice_pack_data[language])
            })
        
        return self.download("multiprocess", files)