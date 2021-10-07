from dataclasses import dataclass
from datetime import datetime
from decimal import Decimal
import json


@dataclass
class FileRead:
    """[dataclass for keeping the read data of a file retrieved from the API.]
    """
    file_id: str = None
    content_disposition: str = None
    content_type: str = None

    @classmethod
    def from_json(cls, jsn):
        """[creates istances of FileRead from passed json]

        Args:
            jsn ([str]): [json object of Read file ]

        Returns:
            [cls]: [instance of FileRead]
        """
        return cls(jsn.get('fileId'), jsn.get(
            'Content-Disposition'), jsn.get('Content-Type'))

    def __str__(self):
        data = {
            "fileId": self.file_id,
            "Content-Disposition": self.content_disposition,
            "Content-Type": self.content_type}
        return json.dumps(data)
