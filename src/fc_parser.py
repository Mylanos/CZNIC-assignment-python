import argparse as ap

class FcParser:
    """File client parser"""    

    def __init__(self):
        self.parser = ap.ArgumentParser(description="Simple CLI application which retrieves and prints data from the described backend.")

    def setup_parser(self) -> None:
        if self.parser:
            self.parser.add_argument("--base_url", type=str, nargs='?', default="http://localhost:3000/", action='store', 
                        help='Sets a base URL for a REST server. Default is http://localhost:3000/.')
            self.parser.add_argument("--output", type=str, nargs='?', default=None, action='store',
                        help='Sets the file where to store the output. Default is -, i.e. the stdout.')
            self.parser.set_defaults(UUID="default")


            subparsers = self.parser.add_subparsers(help="sub-commands read stat", dest='command')
            parser_read = subparsers.add_parser('read', help='Outputs the file content.')
            parser_read.add_argument('UUID', type=str, help='universally unique identifier of the read command')
            parser_stat = subparsers.add_parser('stat', help='Prints the file metadata in a human-readable manner.')
            parser_stat.add_argument('UUID', type=str, help='Universally unique identifier of the stat command')

    def get_args(self):
        return self.parser.parse_args()

