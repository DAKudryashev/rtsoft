from sys_file_parser_v2 import SysFileParser
from fboot_file_verifier import FbootFileVerifier

if __name__ == '__main__':
    sys_a = SysFileParser(r'D:\projects\rtsoft\parserTest.sys')
    sys_a.parse_sys_file()

    print('\n\n\n=====================\n\n\n')

    fboot_a = FbootFileVerifier(r'D:\projects\rtsoft\parserTest_FORTE_PC.fboot')
    fboot_a.set_data(sys_a.get_data())
    fboot_a.parse_fboot_file()
