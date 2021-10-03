from src.stat_ import FileStat
import requests, sys
from src.fc_parser import FcParser
from uuid import UUID


class FileClient:

    def __init__(self, base_url: str ="http://localhost:3000/", output: str=None, command: str="", _uuid: str = "default"):
        self.base_url = base_url
        self.api = f"{base_url}file/{_uuid}/{command}"
        self.output = output
        self.uuid = _uuid
        self.command = command

    # using property decorator
     # a getter function
    @property
    def uuid(self):
        return self._uuid
      
    # a setter function
    @uuid.setter
    def uuid(self, id):
        """
        Check if uuid_to_test is a valid UUID.
        """
        if self.valid_uuid(id):
            self._uuid = id
        else:
            raise ValueError(f"Expected a valid UUID, but received {id}")

    def valid_uuid(self, id):
        """
        Check if uuid_to_test is a valid UUID.
        """
        try:
            return UUID(id)
        except ValueError:
            return None

    def run(self):
        if self.command:
            response = self.make_request()
            # true if response status code was between 200-400
            if response:
                self.output_contents(response.json())
            else:
                print(f"ERROR {response.status_code}: There was an error while requesting the url {self.api}!")

    def output_contents(self, json_content):
        result = None
        for obj in json_content:
            if self.command == "stat":
                file_stat = FileStat()
                result = file_stat.from_json(obj)
            else:
                result = str(obj)
        if self.output:
            original_stdout = sys.stdout
            with open(self.output, 'w') as f:     
                sys.stdout = f # Change the standard output to the file we created.     
                print(result)     
                sys.stdout = original_stdout # Reset the standard output to its original val
        else:
            print(result)

    def make_request(self):
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

        return r


if __name__ == "__main__":
    fc_parser = FcParser()
    fc_parser.setup_parser()
    args = fc_parser.get_args()

    base_url = args.base_url
    output = args.output
    command = args.command
    _uuid = args.UUID

    file_client = FileClient(base_url, output, command, _uuid)
    file_client.run()
