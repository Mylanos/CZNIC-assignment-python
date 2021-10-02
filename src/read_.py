from dataclasses import dataclass, field
from datetime import datetime
from decimal import Decimal

@dataclass
class FileRead:
    content_disposition: datetime
    content_type: Decimal

    def __str__(self):
        return f"""
                Content-Disposition:{self.content_disposition}
                Content-Type: {self.content_type}
                """
   