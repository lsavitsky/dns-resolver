
# This file contains the InvalidCacheLineError class, which is an exception 
# raised when an invalid line is found in the cache file.
class InvalidCacheLineError(Exception):
    """
    Exception raised for invalid lines in the cache file.

    Attributes:
        line -- The invalid line from the cache file.
        message -- Explanation of the error.
    """
    def __init__(self, line: str, message: str = "Invalid line format in cache file"):
        self.line = line
        self.message = f"{message}: {line.strip()}"
        super().__init__(self.message)
