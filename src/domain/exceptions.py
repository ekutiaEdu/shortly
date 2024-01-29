class UrlNotFoundException(Exception):
    def __init__(self, short_code, message="URL not found"):
        self.short_code = short_code
        self.message = message
        super().__init__(message)

    def __str__(self):
        return f"{self.message}: Short code '{self.short_code}'"


class ShortCodeAlreadyExists(Exception):
    def __init__(self, message="Short code already exists"):
        super().__init__(message)
