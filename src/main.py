import argparse

from sys_file_parser_v2 import SysFileParser
from fboot_file_verifier import FbootFileVerifier


def create_cmd_parser():
    p = argparse.ArgumentParser()
    p.add_argument('-s', '--sys', required=True,
                   help='input path to .sys file (required)', metavar='sys_path')
    p.add_argument('-f', '--fboot', required=True,
                   help='input path to .fboot file (required)', metavar='fboot_path')
    p.add_argument('-v', '--verbose', default=False, action='store_true',
                   help='output the contents in the terminal')
    return p


if __name__ == '__main__':
    parser = create_cmd_parser()
    args = parser.parse_args()

    sys_file_parser = SysFileParser(args.sys)
    sys_file_parser.parse_sys_file()

    if args.verbose:
        print(args, '\n\n')
        print('.sys parsing results...\n')
        sys_file_parser.print_results()

        print('\n\n\n=====================\n\n\n')

    fboot_file_verifier = FbootFileVerifier(args.fboot)
    fboot_file_verifier.set_data(sys_file_parser.get_data())
    fboot_file_verifier.parse_fboot_file()

    if args.verbose:
        print('.fboot verifying results...\n')
        fboot_file_verifier.print_process()

        print('\n\n\n=====================\n\n\n')

    fboot_file_verifier.print_results()
