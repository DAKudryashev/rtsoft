from dataclasses import dataclass
from collections import defaultdict
from xml.etree import ElementTree


@dataclass
class Connection:
    source: str
    destination: str

@dataclass
class Fb:
    name: str
    fb_type: str

@dataclass
class Param:
    value : str
    destination: str

@dataclass
class Resource:
    name: str
    res_type: str

class SysFileParser:
    def __init__(self, path=''):
        self.file_path = path
        self.tree = None
        self.root = None

        self.device = None
        self.resources = []
        self.fbs = defaultdict(list)
        self.params = defaultdict(list)
        self.connections = {}

    def update_file_path(self, path):
        self.file_path = path

    # .sys file parsing
    def parse_sys_file(self):
        if self.file_path:
            if self.file_path[-4:] == '.sys':
                self.tree = ElementTree.parse(self.file_path)
                self.root = self.tree.getroot()

                # Device
                self.device = self.tree.find('Device')
                print(f'{self.device.tag} : {self.device.attrib}')

                # Resources
                self.parse_resources()
                print('\n'.join(f'{i.tag} : {i.attrib}' for i in self.resources))

                # Functional blocks
                self.parse_fbs()
                print(dict(self.fbs))
                print(dict(self.params))

                # Connections
                self.parse_connections()
                print(self.connections)

            else:
                raise ValueError('Incorrect sys file path input')
        else:
            raise ValueError('Empty sys file path')

    # Collecting resources
    def parse_resources(self):
        for element in self.device:
            if element.tag == 'Resource':
                self.resources.append(element)

    # Collecting functional blocks -> {resource name : [{'name' : fb_name(str), 'type' : fb_type(str)}, ...], ...}
    def parse_fbs(self):
        for resource in self.resources:
            fbs = {}
            fb_network = resource.find('FBNetwork')
            for fb in fb_network.findall('FB'):
                fb_name = fb.get('Name')
                fb_type = fb.get('Type')
                self.fbs[resource.attrib['Name']].append({'name' : fb_name, 'type': fb_type})

                # Collecting fbs params -> {resource name : [class Param(value, destination), ...], ...}
                for param in fb.findall('Parameter'):
                    param_name = fb_name + '.' + param.get('Name')
                    param_value = param.get('Value')
                    self.params[resource.attrib['Name']].append(Param(value=param_value, destination=param_name))

    # Collecting connections between blocks -> {resource name : [class Connection(source, destination), ...]}
    def parse_connections(self):
        for resource in self.resources:
            fb_network = resource.find('FBNetwork')
            self.connections[resource.attrib['Name']] = []

            # Event connections
            for conn in fb_network.findall('.//EventConnections/Connection'):
                self.connections[resource.attrib['Name']].append(
                    Connection(source=conn.get('Source'), destination=conn.get('Destination'))
                )

            # Data connections
            for conn in fb_network.findall(".//DataConnections/Connection"):
                self.connections[resource.attrib['Name']].append(
                    Connection(source=conn.get("Source"), destination=conn.get("Destination"))
                )


if __name__ == '__main__':
    test_parser = SysFileParser(r'D:\projects\rtsoft\project_examples\testProject\testProject.sys')
    test_parser.parse_sys_file()
