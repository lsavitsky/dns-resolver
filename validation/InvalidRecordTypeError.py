class InvalidRecordTypeError(Exception):
    """
    Exception raised for invalid record types in the cache file.

    Attributes:
        record -- The invalid record type.
        message -- Explanation of the error.
    """
    VALID_RECORDS = ["A", "AAAA", "NS"]

    def __init__(self, record: str, message: str = "Invalid record type in cache file"):
        self.record = record
        self.message = f"{message}: {record}"
        self.message += f"\nValid record types: {', '.join(self.VALID_RECORDS)}"
        super().__init__(self.message)