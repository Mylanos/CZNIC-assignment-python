Makefile contains all sorts of rules for testing and running the script, automatic installation of needed packages into a virtual Environment and so on.
During development I used json server for querying data, that runs a server from predefined json file(data/db.json). Running the server
is required for the optimal functionality of the script. Then the script file_client.py can be run as expected.

How to run:
1. npm install

2. make server - for starting the server

3. make        - run the application with the pre set arguments

4. make test   - run the unit tests 

Other options:

make clean     - clean the directory

make test      - pre spustenie unit testov

make help      - napoveda

make run       - same as make

make runRead   - for running the script with read command/argument
