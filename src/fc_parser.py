import argparse as ap
import enum
import sys


class FS_subcmd(enum.Enum):
    """[represents available commands]

    Args:
        enum ([str]): [commands]
    """
    NONE = ''
    STAT = 'stat'
    READ = 'read'

    def __str__(self):
        return self.value

    @classmethod
    def has_value(cls, value):
        return value in cls._value2member_map_


class FcParser(ap.ArgumentParser):
    """[file client inherited arguments parser with custom setup]

    Args:
        ap ([argparse]): [argparse module]

    Returns:
        [args]: [list of passed arguments]
    """

    @classmethod
    def get_args(cls, description=None):
        """Your other perfectly fine docstring"""
        parser = cls(description)

        parser.add_argument("--base_url", type=str, nargs='?', default="http://localhost:3000/", action='store',
                            help='Sets a base URL for a REST server. Default is http://localhost:3000/.')
        parser.add_argument("--output", type=str, nargs='?', default=None, action='store',
                            help='Sets the file where to store the output. Default is -, i.e. the stdout.')

        subparsers = parser.add_subparsers(
            help="sub-commands read stat", dest='command')
        parser_read = subparsers.add_parser(
            FS_subcmd.STAT.value, help='Outputs the file content.')
        parser_read.add_argument(
            'UUID',
            type=str,
            help='Universally unique identifier of the read command')
        parser_stat = subparsers.add_parser(
            FS_subcmd.READ.value,
            help='Prints the file metadata in a human-readable manner.')
        parser_stat.add_argument(
            'UUID',
            type=str,
            help='Universally unique identifier of the stat command')

        if len(sys.argv) == 1:
            parser.print_help(sys.stderr)
            sys.exit(1)

        return parser.parse_args()
