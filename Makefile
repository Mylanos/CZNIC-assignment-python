VENV = venv
PYTHON = $(VENV)/bin/python3
PIP = $(VENV)/bin/pip
FILE_CLIENT = src/file_client.py
DEFAULT_UUID = 00000000-0000-0000-0000-000000000000
TEST_SCRIPT = tests/test_fileclient.py

run: $(VENV)/bin/activate
	$(PYTHON) $(FILE_CLIENT) stat $(DEFAULT_UUID)

test: $(VENV)/bin/activate
	$(PYTHON) -m unittest $(TEST_SCRIPT) 

$(VENV)/bin/activate: requirements.txt
	python3 -m venv $(VENV) \
	$(PIP) install -r requirements.txt \
	source $(VENV)/bin/activate \

requirements.txt: 
	$(PIP) freeze > requirements.txt

clean:
	rm -rf .pytest_cache
	rm -rf src/__pycache__
	rm -rf tests/__pycache__
	rm -rf tests/.pytest_cache
	rm -rf $(VENV)