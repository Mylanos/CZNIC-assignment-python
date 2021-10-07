import sys
import os

# setting to path script working dir because of the problems with other
# classes imports
try:
    sys.path.index(os.getcwd())
except ValueError:
    sys.path.append(os.getcwd())

from src.stat_ import FileStat
from src.read_ import FileRead
import requests
import sys
from src.fc_parser import FcParser, FS_subcmd
from uuid import UUID


class FileClient:
    """[Main class of the programme, represents the desired command, stores passed arguments and makes requests to API]
    """

    def __init__(self, base_url: str = "http://localhost:3000/", output: str = None,
                 command: FS_subcmd = FS_subcmd.NONE, _uuid: str = None):
        self.base_url = base_url
        self.command = command
        self.api = None
        self.set_api(base_url, command, _uuid)
        self.output = output
        self.uuid = _uuid

    def set_api(self, base_url: str = "http://localhost:3000/",
                command: str = None, _uuid: str = None):
        """[sets url for given uuid and command]

        Args:
            base_url (str, optional): [base of the url]. Defaults to "http://localhost:3000/".
            command (str, optional): [command to be executed]. Defaults to None.
            _uuid (str, optional): [identifier of certain file]. Defaults to None.
        """
        self.api = f"{base_url}file/{_uuid}/{command}"

    @property
    def uuid(self):
        """[getter of uuid]

        Returns:
            [str]: [uuid string]
        """
        return self._uuid

    @uuid.setter
    def uuid(self, _uuid: str):
        """[setter, checks validity of UUID before assignment]

        Args:
            _uuid (str): [identifier of certain file]

        Raises:
            ValueError: [passed _uuid has wrong format]
        """
        if self.valid_uuid(_uuid):
            self._uuid = _uuid
            self.set_api(self.base_url, self.command, _uuid)
        else:
            raise ValueError(f"Expected a valid UUID, but received {id}")

    def valid_uuid(self, _uuid: str):
        """[Checks if received uuid is a valid UUID.]

        Args:
            _uuid (str): [identifier of certain file]

        Returns:
            [type]: [_uuid if its in correct format, else None]
        """
        try:
            return UUID(_uuid)
        except ValueError:
            return None

    def run(self):
        """[starts the retriever file_client]
        """
        if self.command:
            response = self.make_request()
            # true if response status code was between 200-400
            if response:
                self.output_contents(response.json())
            else:
                print(
                    f"ERROR {response.status_code}: There was an error while requesting the url {self.api}!")

    def command_execution(self, json_content):
        """[function executes supported commands]

        Args:
            json_content ([str]): [json data received from the api]

        Returns:
            [str]: [returns desired output]
        """
        for obj in json_content:
            if self.command == FS_subcmd.STAT.value:
                file_stat = FileStat()
                return file_stat.from_json(obj)
            else:
                file_read = FileRead()
                return file_read.from_json(obj)

    def output_contents(self, json_content):
        """[prints data to STDOUT or given file]

        Args:
            json_content ([str]): [json data received from the api]
        """
        result = self.command_execution(json_content)
        if self.output:
            original_stdout = sys.stdout
            with open(self.output, 'w') as f:
                # Change the standard output to the file we created.
                sys.stdout = f
                print(result)
                sys.stdout = original_stdout  # Reset the standard output to its original val
        else:
            print(result)

    def make_request(self):
        """[makes request to given url]

        Raises:
            SystemExit: [http error while requesting]

        Returns:
            [Response]: [response from the requested url]
        """
        headers = {
            'Connection': 'keep-alive',
            'sec-ch-ua': '"Chromium";v="94", "Google Chrome";v="94", ";Not A Brand";v="99"',
            'DNT': '1',
            'sec-ch-ua-mobile': '?0',
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/94.0.4606.61 Safari/537.36',
            'sec-ch-ua-platform': '"macOS"',
            'Accept': '*/*',
            'Sec-Fetch-Site': 'same-origin',
            'Sec-Fetch-Mode': 'cors',
            'Sec-Fetch-Dest': 'empty',
            'Referer': self.api,
            'Accept-Language': 'en-US,en;q=0.9',
        }

        try:
            r = requests.get(self.api, headers=headers)
            r.raise_for_status()
        except requests.exceptions.HTTPError as err:
            raise SystemExit(err)
        except ConnectionError as err:
            raise SystemExit(err)

        return r

    def __str__(self):
        return f"""
        BASE URL: {self.base_url}
        API URL:{self.api}
        Output: {self.output}
        UUID: {self.uuid}
        Command: {self.command}
                """


if __name__ == "__main__":
    args = FcParser.get_args(
        "Simple CLI application which retrieves and prints data from the described backend.")
    file_client = FileClient(
        args.base_url,
        args.output,
        args.command,
        args.UUID)
    file_client.run()
