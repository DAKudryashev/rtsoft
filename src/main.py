from sys_file_parser_v2 import SysFileParser
from fboot_file_verifier import FbootFileVerifier

if __name__ == '__main__':
    sys_a = SysFileParser(r'D:\projects\rtsoft\project_examples\parserTest\parserTest.sys')
    sys_a.parse_sys_file()

    print('\n\n\n=====================\n\n\n')

    fboot_a = FbootFileVerifier(r'D:\projects\rtsoft\project_examples\parserTest\parserTest_FORTE_PC.fboot')
    fboot_a.set_data(sys_a.get_data())
    fboot_a.parse_fboot_file()

    print('\n\n\n\n\n\n')

    sys_b = SysFileParser(r'D:\projects\rtsoft\project_examples\mai_test1\mai_test1.sys')
    sys_b.parse_sys_file()

    print('\n\n\n=====================\n\n\n')

    fboot_b = FbootFileVerifier(r'D:\projects\rtsoft\project_examples\mai_test1\mai_test1_FORTE_PC.fboot')
    fboot_b.set_data(sys_b.get_data())
    fboot_b.parse_fboot_file()
