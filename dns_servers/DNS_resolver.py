import AuthMapper
from pathlib import Path
import sys 

sys.path.append("../dns_caches/")

class Resolver():
    def __init__(self, file: Path):
        pass

    def read_dns_cache(self, file : str):
        """
            read_dns_cache attempts to read from the cache file and creates an
            enum type AuthMapper
            
            :param: file: - the location of the cache
        """
        try:
            return AuthMapper(file).map
        except Exception as e:
            print(f"Error reading DNS cache file: {e}")
            return {}
        