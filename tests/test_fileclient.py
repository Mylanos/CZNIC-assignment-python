import json, unittest
from os import stat_result
import sys
from src.file_client import FileClient
from src.stat_ import FileStat

class TestFileClient:

    def test_request(self):
        base_url = "http://localhost:3000/"
        command = "stat"
        file_client1 = FileClient(base_url, None, command, "00000000-0000-0000-0000-000000000000")
        #stat_data = self.retrieve_api_stat(file_client1)
        #print(stat_data)
        self.retrieve_local(command)
        assert 1 == 1

    def retrieve_api_stat(self, file_client: FileClient):
        """Finds the weather for a city and returns a WeatherInfo instance."""
        response = file_client.make_request()
        stat_list = []
        for obj in response.json():
            print(obj)
            stat_list.append(FileStat.from_json(obj))
        return stat_list

    def retrieve_local(self, command: str):
        """Finds the weather for a city and returns a WeatherInfo instance."""
        stat_list = []
        with open("data/db.json", 'r') as f:
            data = json.loads(f.read())
            print(data)
        
        
    
    """
    @pytest.fixture()
    def local_file_data():
        ""Fixture that returns a static weather data.""
        with open("db.json") as f:
            return json.load(f)
    """

if __name__ == "__main__":
    kek = TestFileClient()
    kek.test_request()