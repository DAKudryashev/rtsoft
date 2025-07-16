import hashlib


# Считаем md5 полученного файла
def calculate_md5(content):
    return hashlib.md5(content.encode('utf-8')).hexdigest()


# Сравниваем контрольные суммы
def compare_md5(expected_md5, received_md5):
    return 'Совпало' if expected_md5 == received_md5 else 'Не совпало'


# Читаем файл
def read_file(file_path: str):
    with open(file_path, 'r') as f:
        content = f.read()
        return content


if __name__ == '__main__':
    a = read_file('INT2INT.fbt')
    print('========Обрабатываемая строка========')
    print(a)
    print('\n========MD5========')
    received = calculate_md5(a)
    print(received)
    print('\n========Результаты сравнения контрольных сумм========')
    print(compare_md5(expected_md5='2b954ed02ac50ae98c123325ea20cb29', received_md5=received))

    b = read_file('project1_FORTE_PC.fboot')
    print('========Обрабатываемая строка========')
    print(b)
    print('\n========MD5========')
    received = calculate_md5(b)
    print(received)
    print('\n========Результаты сравнения контрольных сумм========')
    print(compare_md5(expected_md5='ffefcfca7b68c1bd856f91cd12b672d9', received_md5=received))
