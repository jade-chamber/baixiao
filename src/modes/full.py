import os

from ..utils.download import Download
from ..utils.logger import Logger

class Full(Download):
    def __init__(self, branch):
        self.logger = Logger("Full", "#fbf3b6", 1)
        super().__init__(branch, self.logger)
        self.version = self.branch_info['info']
        self.full_info = self.branch_info['full']
    

    def _build_url(self, info):
        return f"{self.config['downloads']['base_url']}/client_app/download/pc_zip/{info}"
    

    def download_full(self):
        files = []

        for x in range(1, self.full_info['parts']+1):
            data = self.full_info['data']
            files.append({
                "name": f"GenshinImpact_{self.version['release_version']}.zip.00{x}",
                "url": self._build_url(f"{data}/GenshinImpact_{self.version['release_version']}.zip.00{x}"),
                "path": os.path.join(self.fs.downloads, self.branch, "full")
            })

        # generate languages
        for language in self.full_info['languages']:
            files.append({
                "name": f"{language}_{self.version['release_version']}.zip",
                "url": self._build_url(f"{data}/{language}_{self.version['release_version']}.zip"),
                "path": os.path.join(self.fs.downloads, self.branch, "full", "voice_packs")
            })
        
        return self.download("multiprocess", files)