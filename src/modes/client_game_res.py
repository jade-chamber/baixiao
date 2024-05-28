import os
import json

from ..utils.download import Download
from ..utils.logger import Logger

class ClientGameRes(Download):
    index_names = [
            "res_versions_external", 
            "res_versions_medium", 
            "res_versions_streaming",
            "release_res_versions_external",
            "release_res_versions_medium",
            "release_res_versions_streaming"
            ]
    
    client_names = [
            "StandaloneWindows64", 
            "Android", 
            "iOS", 
            "PS4", 
            "PS5"
            ]

    def __init__(self, branch):
        self.logger = Logger("ClientGameRes", "#fbf3b6", 1)
        super().__init__(branch, self.logger)
        self.resources = self.branch_info['resource_info']
    

    def _build_url(self, info):
        return f"{self.config['downloads']['base_url']}client_game_res/{self.branch}/output_{info['version']}_{info['suffix']}/client/{info['client']}/{info['trail']}"
    

    def _parse_index(self, path):
        lines = []
        parsed = []
        try:
            lines = self.fs.read_lines(path)
            for line in lines:
                parsed.append(json.loads(line))
            return parsed
        except:
            self.logger.log("error", f"Failed to read: {path.split("/")[-1]}")
            return []

    def download_indexes(self):
        self.logger.log("info", "Downloading indexes...")
        files = []
        # info object
        # {
        #     "version": 0,
        #     "suffix": "",
        #     "client": "",
        #     "trail": ""
        # }

        # Iterate through available res for the branch
        for resource in self.resources:
            if not "res" in resource:
                continue

            for client in self.client_names:
                for index in self.index_names:

                    files.append({
                        "name": index,
                        "url": self._build_url(
                            {
                            "version": resource['res']['version'],
                            "suffix": resource['res']['suffix'],
                            "client": client,
                            "trail": index
                            }
                        ),
                        "path": os.path.join(self.fs.downloads, self.branch, f"{resource['res']['version']}_{resource['res']['suffix']}", client)
                    })
        
        return self.download("multiprocess", files)
    

    def download_blks(self):
        # for each client, and each index, parse and download the blks
        for resource in self.resources:
            if not "res" in resource:
                continue
            files = []
            for client in self.client_names:
                for index in self.index_names:
                    path = os.path.join(self.fs.downloads, self.branch, f"{resource['res']['version']}_{resource['res']['suffix']}", client, index)
                    parsed = self._parse_index(path)
                    if not parsed:
                        continue
                    for entry in parsed:
                        name = entry['remoteName'].split("/")[-1]
                        if not name.endswith(".blk"):
                            continue
                        path_final = '/'.join(entry['remoteName'].split("/")[:-1])
                        files.append({
                            "name": name,
                            "url": self._build_url(
                                {
                                "version": resource['res']['version'],
                                "suffix": resource['res']['suffix'],
                                "client": client,
                                "trail": f"AssetBundles/{path_final}/{name}"
                                }
                            ),
                            "path": os.path.join(self.fs.downloads, self.branch, f"{resource['res']['version']}_{resource['res']['suffix']}", client, "AssetBundles", path_final)
                        })
            
            return self.download("multiprocess", files)

        pass