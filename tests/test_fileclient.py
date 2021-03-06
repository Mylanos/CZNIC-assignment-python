import json, unittest
import requests
import os, sys # if you want this directory

try:
    sys.path.index(os.getcwd()) # Or os.getcwd() for this directory
except ValueError:
    sys.path.append(os.getcwd()) # Or os.getcwd() for this directory

from src.file_client import FileClient
from src.stat_ import FileStat
from src.read_ import FileRead


class TestFileClient(unittest.TestCase):

    def test_request_stat(self):
        base_url = "http://localhost:3000/"
        command = "stat"
        uuid_ = "00000000-0000-0000-0000-000000000000"
        file_client = FileClient(base_url, None, command, uuid_)
        file_stat = FileStat()
        data_api, status_code = self.retrieve_api(file_client, file_stat)
        data_local = self.retrieve_local(command, uuid_, file_stat)

        self.assertEqual(status_code, 200)   # should be succesful request
        self.assertEqual(data_local , data_api) # response from API should be the same as in json

    def test_request_read(self):
        base_url = "http://localhost:3000/"
        command = "read"
        uuid_ = "00000000-0000-0000-0000-000000000000"
        file_client = FileClient(base_url, None, command, uuid_)
        file_read = FileRead()
        data_api, status_code = self.retrieve_api(file_client, file_read)
        data_local = self.retrieve_local(command, uuid_, file_read)

        self.assertEqual(status_code, 200)   # should be succesful request
        self.assertEqual(data_local , data_api) # response from API should be the same as in json

    def test_bad_request(self):
        base_url = "http://locaaalhost/"
        command = "read"
        uuid_ = "00000000-0000-0000-0000-000000000000"
        file_client = FileClient(base_url, None, command, uuid_)

        with self.assertRaises(requests.exceptions.RequestException) as e:
            _ = file_client.make_request()

    def test_bad_uuid(self):
        base_url = "http://locaaalhost/"
        command = "read"
        uuid_ = "wrong_format_of_uuid"
        with self.assertRaises(ValueError) as e:
            _ = FileClient(base_url, None, command, uuid_)

    def test_output_stat(self):
        base_url = "http://localhost:3000/"
        command_stat = "stat"
        command_read = "read"
        uuid_ = "00000000-0000-0000-0000-000000000000"
        file_client1 = FileClient(base_url, "data/out.txt", command_stat, uuid_)
        file_client1.run()
        file_client2 = FileClient(base_url, "data/out.txt", command_read, uuid_)
        file_client2.run()
        
        # compare output file with expected output line by line
        # stat command
        with open("data/out_stat.txt", 'r') as f1, open("data/out_stat_expected.txt", 'r') as f2:
            for line1, line2 in zip(f1, f2):
                self.assertTrue(line1 == line2)
        # read command
        with open("data/out_read.txt", 'r') as f1, open("data/out_read_expected.txt", 'r') as f2:
            for line1, line2 in zip(f1, f2):
                self.assertTrue(line1 == line2)

    def retrieve_api(self, file_client: FileClient, cmd_class_instance):
        """Finds the weather for a city and returns a WeatherInfo instance."""
        response = file_client.make_request()
        stat_list = []
        for obj in response.json():
            stat_list.append(cmd_class_instance.from_json(obj))
        return stat_list, response.status_code

    def retrieve_local(self, command: str, uuid_: str, cmd_class_instance):
        """Finds the weather for a city and returns a WeatherInfo instance."""
        stat_list = []
        with open("data/db.json", 'r') as f:
            data = json.loads(f.read())
            """ print(uuid_)
            print('vs')
            print(data[command][2]['fileId'])
            print(data[command][2]['fileId'] == uuid_)
            print('----------------------------------') """
            stat_list = [cmd_class_instance.from_json(obj) for obj in data[command] if obj['fileId'] == uuid_]
        return stat_list
    
    def test_subsequent_requests(self):
        base_url = "http://localhost:3000/"
        command = "stat"
        uuid_1 = "00000000-0000-0000-0000-000000000000"
        uuid_2 = "4245da7c-d332-46cf-b91c-4818dbc5439a"
        file_client = FileClient(base_url, None, command, uuid_1)
        file_stat = FileStat()
        data_api1, status_code1 = self.retrieve_api(file_client, file_stat)
        data_local1 = self.retrieve_local(command, uuid_1, file_stat)

        # changing the requested uuid
        file_client.uuid = uuid_2
        data_api2, status_code2 = self.retrieve_api(file_client, file_stat)
        data_local2 = self.retrieve_local(command, uuid_2, file_stat)
        
        self.assertEqual(status_code1, 200)   # should be succesful request
        self.assertEqual(data_local1 , data_api1) # response from API should be the same as in json

        self.assertEqual(status_code2, 200)   # should be succesful request
        self.assertEqual(data_local2 , data_api2) # response from API should be the same as in json
    

if __name__ == "__main__":
    unittest.main()
    