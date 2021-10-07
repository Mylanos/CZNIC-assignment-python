from dataclasses import dataclass
from datetime import datetime
from decimal import Decimal
from os import stat


@dataclass
class FileStat:
    """[dataclass for keeping the stats of a file retrieved from the API.]
    """
    create_datetime: datetime = "1970-01-01T00:00:00.000-00:00"
    file_sizes: Decimal = 0
    mimetype: str = None
    name: str = None
    id: str = None

    def __post_init__(self):
        """[converts date string to datetime]
        """
        self.create_datetime = datetime.strptime(
            self.create_datetime, '%Y-%m-%dT%H:%M:%S.%f%z')

    @classmethod
    def from_json(cls, jsn):
        """[creates istances of FileStat from passed json]

        Args:
            jsn ([str]): [json object of Stat file ]

        Returns:
            [cls]: [instance of FileStat]
        """
        return cls(jsn.get('create_datetime'), jsn.get('size'),
                   jsn.get("mimetype"), jsn.get("name"), jsn.get('fileId'))

    def pretty_print(self):
        return f"""
        ID: {self.id}
        Creation datetime:{self.create_datetime}
        File sizes: {self.file_sizes}
        Mimetype: {self.mimetype}
        Name: {self.name}
                """

    def __str__(self):
        return self.pretty_print()
