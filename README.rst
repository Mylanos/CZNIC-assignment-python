==========
Assignment
==========

Create a simple CLI application which retrieves and prints data from the described backend.

Environment
===========

There is a server providing a service using a REST API. The REST API is described in `<rest_file.rst>`_

Command line
============

Provide a command ``file-client`` with following usage::

    Usage: file-client [options] stat UUID
           file-client [options] read UUID
           file-client --help

    Subcommands:
      stat                  Prints the file metadata in a human-readable manner.
      read                  Outputs the file content.

    Options:
      --help                Show this help message and exit.
      --base-url=URL        Set a base URL for a REST server. Default is http://localhost/.
      --output=OUTPUT       Set the file where to store the output. Default is -, i.e. the stdout.


All commands and options need to work as described, but the usage may be formatted differently.
Other options may be provided.

Requirements
============

* Use supported python version (3.6-3.9).
* Third party open source libraries are allowed.
* Linux OS support.
* Unit tests are required.
