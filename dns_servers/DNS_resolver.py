from pathlib import Path
import sys 
import enum

cache_path = Path("../dns_caches/")

sys.path.append("..")
from AuthMapper import AuthMapper

sys.path.append("../validation/") 
import InvalidCacheLineError
import InvalidRecordTypeError

class Resolver:
    """
    Base DNS Resolver class. Provides a method for reading DNS cache files.
    """
    def __init__(self, file: Path):
        """
        Initializes the resolver with a cache file path.
        
        :param file: Path to the DNS cache file.
        """
        self.file_cache = file
        self.cache_map = self.read_dns_cache(file) # initialize the cache data
        
    def read_dns_cache(self, file: Path) -> dict:
        """
        Reads the DNS cache file and returns a dictionary of mappings.

        :param file: Path to the cache file.
        :return: Dictionary of domain-to-IP mappings.
        """
        file = cache_path / file
        
        print(f"Reading DNS cache file {file}...")  
        
        if not file.exists():
            print(f"Error: Cache file {file} does not exist.")
            return {}
        try:
            return AuthMapper(file).map
        except FileNotFoundError:
            print(f"Error: Cache file {file} not found.")
        except PermissionError:
            print(f"Error: Permission denied for file {file}.")
        except Exception as e:
            print(f"Unexpected error while reading DNS cache file: {e}")
        return {}
    
    def resolve(self, domain: str) -> str:
        """
        Resolves a domain name. This base method should be overridden by subclasses.

        :param domain: The domain name to resolve.
        :return: Resolved IP address or 'NXDOMAIN' if not found.
        """
        raise NotImplementedError("Subclasses must implement the resolve method.")
    
    
    def print_result(self, res: object) -> None:
        """
        Prints the resolved value of a domain name.

        :param res: The resolved value to print.
        """
        if res == "NXDOMAIN":
            print("Domain not found.")
        elif isinstance(res, enum.EnumType):
            # Handle Enum-based responses
            print("Resolved Record:")
            if hasattr(res, "A"):
                print("  A:", res.A.value)
            if hasattr(res, "AAAA"):
                print("  AAAA:", res.AAAA.value)
            if hasattr(res, "Num"):
                print("  Num:", res.Num.value)
            if hasattr(res, "NS"):
                print("  NS:", res.NS.value)
        else:
            # Handle unexpected record types
            raise InvalidRecordTypeError.InvalidRecordTypeError(f"Invalid record type: {type(res)}")

