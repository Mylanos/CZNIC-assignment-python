from dataclasses import dataclass
from datetime import datetime
from decimal import Decimal

@dataclass
class FileRead:
    content_disposition: str = None
    content_type: str = None

    @classmethod
    def from_json(cls, jsn):
        return cls(jsn.get('Content-Disposition'), jsn.get('Content-Type'))

    def __str__(self):
        return f"""
                Content-Disposition:{self.content_disposition}
                Content-Type: {self.content_type}
                """
   