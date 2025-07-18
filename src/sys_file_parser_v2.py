from xml.etree import ElementTree

from src.data import FB, Parameter, Connection, Resource

class SysFileParser:
    def __init__(self, path=''):
        self.file_path = path
        self.tree = None
        self.root = None

        self.application_name = None
        self.fbs = []
        self.parameters = []
        self.device_name = None
        self.resources = []
        self.connections = []

    # Rewrite path value
    def update_file_path(self, path):
        self.file_path = path

    # Rewrite variables storing collected information
    def reset_collections(self):
        self.application_name = None
        self.fbs = []
        self.parameters = []
        self.device_name = None
        self.resources = []
        self.connections = []

    # Main parsing function
    def parse_sys_file(self):
        if self.file_path:
            if self.file_path[-4:] == '.sys':
                # ElementTree instance
                self.tree = ElementTree.parse(self.file_path)
                self.root = self.tree.getroot()

                # Parsing...
                self.parse_application()
                self.parse_fbs()
                self.parse_devise()
                self.parse_resources()
                self.parse_mapping()
                self.delete_unmapped_fbs()
                self.parse_connections()

                # Print results
                self.check_results()

            else:
                raise ValueError('Incorrect sys file path input')
        else:
            raise ValueError('Empty sys file path')

    # Get application name
    def parse_application(self):
        self.application_name = self.root.find('Application').get('Name')

    # Collecting FBs and their parameters
    def parse_fbs(self):
        # FBs
        for fb in self.root.findall('.//Application/SubAppNetwork/FB'):
            fb_name = self.application_name + '.' + fb.get('Name')
            fb_type = fb.get('Type')
            self.fbs.append(FB(name=fb_name, fb_type=fb_type))

            # Parameters
            for param in fb.findall('Parameter'):
                value = param.get('Value')
                destination = fb_name + '.' + param.get('Name')
                self.parameters.append(Parameter(value=value,
                                                 destination=destination,
                                                 fb=self.fbs[-1])
                                       )


    # Get device name
    def parse_devise(self):
        self.device_name = self.root.find('Device').get('Name')

    # Collecting resources
    def parse_resources(self):
        for resource in self.root.findall('.//Device/Resource'):
            self.resources.append(
                Resource(
                    short_name=resource.get('Name'),
                    full_name=self.device_name + '.' + resource.get('Name'),
                    res_type=resource.get('Type')
                )
            )

    # Writing information about mapping FBs to resources
    def parse_mapping(self):
        for mapping in self.root.findall('Mapping'):
            source = mapping.get('From')
            destination = mapping.get('To')
            for fb in self.fbs:
                if source == fb.name:
                    for resource in self.resources:
                        if resource.full_name == destination:
                            fb.resource = resource.short_name
                            break
                    break

    # Deleting FBs without resource and their parameters
    def delete_unmapped_fbs(self):
        # Parameters
        for param in self.parameters:
            if not param.fb.resource:
                self.parameters.remove(param)

        # FBs
        for fb in self.fbs:
            if not fb.resource:
                self.fbs.remove(fb)

    # Collecting connections and check if FBs are mapped with saving info about resources
    def parse_connections(self):
        # Event connections from Application
        for conn in self.root.findall('.//Application/SubAppNetwork/EventConnections/Connection'):
            source = self.application_name + '.' + conn.get('Source')
            destination = self.application_name + '.' + conn.get('Destination')

            # check if fbs mapped and find resource
            connected = [False, False]
            resource = ''
            for fb in self.fbs:
                if fb.name == source[:source.rfind('.')]:
                    resource = fb.resource
                    connected[0] = True
                elif fb.name == destination[:destination.rfind('.')]:
                    connected[1] = True

            if connected[0] and connected[1]:
                self.connections.append(Connection(source=source, destination=destination, resource=resource))

        # Data connections from Application
        for conn in self.root.findall('.//Application/SubAppNetwork/DataConnections/Connection'):
            source = self.application_name + '.' + conn.get('Source')
            destination = self.application_name + '.' + conn.get('Destination')

            # check if fbs mapped and find resource
            connected = [False, False]
            resource = ''
            for fb in self.fbs:
                if fb.name == source[:source.rfind('.')]:
                    resource = fb.resource
                    connected[0] = True
                elif fb.name == destination[:destination.rfind('.')]:
                    connected[1] = True

            if connected[0] and connected[1]:
                self.connections.append(Connection(source=source, destination=destination, resource=resource))

        # Event connections in resources (START fb)
        for resource in self.root.findall('.//Device/Resource'):
            for conn in resource.findall('.//FBNetwork/EventConnections/Connection'):
                source = conn.get('Source')
                destination = conn.get('Destination')
                res = resource.get('Name')

                # check if fbs mapped and find resource
                connected = False
                for fb in self.fbs:
                    if fb.name == destination[:destination.rfind('.')]:
                        connected = True

                if connected:
                    self.connections.append(Connection(source=source, destination=destination, resource=res))

    # Print results of parsing
    def check_results(self):
        print(f'application name: {self.application_name}')
        print(f'mapped FBs: {self.fbs}')
        print(f'mapped Parameters: {self.parameters}')
        print(f'device name: {self.device_name}')
        print(f'resources: {self.resources}')
        print(f'mapped connections: {self.connections}')

    def get_data(self):
        return [self.application_name, self.fbs, self.parameters, self.device_name, self.resources, self.connections]


if __name__ == '__main__':
    a = SysFileParser(r'../project_examples/parserTest/parserTest.sys')
    a.parse_sys_file()