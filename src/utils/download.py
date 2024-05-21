import os
import requests
import multiprocessing

from .logger import Logger
from .fs import FS

class Download:
    def __init__(self, branch, logger):
        self.logger = logger
        self.fs = FS()
        self.branch = branch
        self.config = self.fs._read_config()
        self.versions = self.fs._read_versions()
        self.branch_info = self.versions[self.branch]
    

    def _checksum(self, file: dict) -> str:
        # TODO: Implement checksum verification
        pass

    
    def _download(self, file: dict) -> str:
        if not os.path.exists(file['path']):
            os.makedirs(file['path'])
        
        with requests.get(file['url'], stream=True) as r:
            r.raise_for_status()
            self.logger.log("download", f"Downloading: {file['name']}")
            with open(f"{file['path']}/{file['name']}", "wb") as f:
                for chunk in r.iter_content(chunk_size=1024):
                    f.write(chunk)
            
            self.logger.log("download", f"Downloaded: {file['name']}")
        
        return "Ok"
    

    def download(self, mode, files):
        match mode:
            case "single":
                for file in files:
                    self._download(file['url'], file['path'])
                return "Ok"
            
            case "multiprocess":
                num_cpus = multiprocessing.cpu_count()
                num_processes = len(files) if len(files) < num_cpus else num_cpus
                with multiprocessing.Pool(processes=num_processes) as pool:
                    pool.map(self._download, files)
                    pool.close()
                    pool.join()
                return "Ok"
            
            case _:
                return "UnknownDownloadMode"
    