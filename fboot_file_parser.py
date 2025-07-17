from dataclasses import dataclass
from collections import defaultdict


@dataclass
class Resource:
    name: str
    res_type: str

@dataclass
class Connection:
    source: str
    destination: str

@dataclass
class Param:
    value : str
    destination: str

class FbootFilePparser:
    def __init__(self, path=''):
        self.file_path = path
        self.resources = []
        self.fbs = defaultdict(list)
        self.connections = defaultdict(list)
        self.params = defaultdict(list)
        self.mistakes = []

    def update_file_path(self, path):
        self.file_path = path

    # .fboot file parsing
    def parse_fboot_file(self):
        if self.file_path:
            if self.file_path[-6:] == '.fboot':
                self.parse_commands()
            else:
                raise TypeError('Incorrect fboot file path input')
        else:
            raise  TypeError('Empty fboot file path')

    def parse_commands(self):
        with open(self.file_path, 'r') as f:
            for line in f:
                res, command = line.strip().split(sep=';', maxsplit=1)

                # Collecting resources
                if not res:
                    start_name = command.find('FB Name="') + 9
                    name = command[start_name:command.find('"', start_name)]

                    start_type = command.find('Type="') + 6
                    res_type = command[start_type:command.find('"', start_type)]

                    self.resources.append(Resource(name=name, res_type=res_type))

                # Collecting fbs
                elif command.find('Action="CREATE"><FB') != -1:
                    start_name = command.find('FB Name="') + len('FB Name="')
                    name = command[start_name:command.find('"', start_name)]

                    start_type = command.find('Type="') + len('Type="')
                    fb_type = command[start_type:command.find('"', start_type)]

                    self.fbs[res].append({'name' : name, 'type' : fb_type})

                # Collecting fb params
                elif command.find('Action="WRITE"') != -1:
                    value_start = command.find('Connection Source="') + len('Connection Source="')
                    value = command[value_start:command.find('"', value_start)]

                    destination_start = command.find('Destination="') + len('Destination="')
                    destination = command[destination_start:command.find('"', destination_start)]
                    self.params[res].append(Param(value=value, destination=destination))

                # Collecting connections
                elif command.find('Action="CREATE"><Connection') != -1:
                    source_start = command.find('Connection Source="') + len('Connection Source="')
                    source = command[source_start:command.find('"', source_start)]

                    destination_start = command.find('Destination="') + len('Destination="')
                    destination = command[destination_start:command.find('"', destination_start)]

                    self.connections[res].append(Connection(source=source, destination=destination))

        print(self.resources)
        print(self.fbs)
        print(self.params)
        print(self.connections)


if __name__ == '__main__':
    a = FbootFilePparser(r'D:\projects\rtsoft\parserTest_FORTE_PC.fboot')
    a.parse_fboot_file()

    # b = FbootFilePparser(r'D:\projects\rtsoft\mai_test1_FORTE_PC.fboot')
    # b.parse_fboot_file()
