from data import FB, Parameter, Connection, Resource


class FbootFileVerifier:
    def __init__(self, path=''):
        self.file_path = path

        self.sys_application_name = None
        self.sys_fbs = []
        self.sys_parameters = []
        self.sys_device_name = None
        self.sys_resources = []
        self.sys_connections = []

        self.unstarted_resources = []
        self.incorrect_lines = []
        self.current_resource = None
        self.current_fb = None
        self.current_parameter = None
        self.current_connection = None

        self.process_output = []

    def update_file_path(self, path):
        self.file_path = path

    # set data which came from SysFileParser
    def set_data(self, data):
        self.sys_application_name = data[0]
        self.sys_fbs = data[1]
        self.sys_parameters = data[2]
        self.sys_device_name = data[3]
        self.sys_resources = data[4]
        self.sys_connections = data[5]

    # .fboot file parsing
    def parse_fboot_file(self):
        if self.file_path:
            if self.file_path[-6:] == '.fboot':
                self.verify_commands()
            else:
                raise TypeError('Incorrect fboot file path input')
        else:
            raise TypeError('Empty fboot file path')

    def verify_commands(self):
        with open(self.file_path, 'r') as f:
            cnt = 0
            for line in f:
                tmp_line = line
                # "&apos;" -> "'" in tmp_line of fboot
                while '&apos;' in tmp_line:
                    tmp_line = tmp_line.replace('&apos;', "'")

                # "&quot;" -> '"' in tmp_line of fboot
                while '&quot;' in tmp_line:
                    tmp_line = tmp_line.replace('&quot;', '"')

                cnt += 1
                res, command = tmp_line.strip().split(sep=';', maxsplit=1)

                # Collecting resources
                if not res:
                    # Parse command
                    start_name = command.find('FB Name="') + len('FB Name="')
                    short_name = command[start_name:command.find('" Type="', start_name)]

                    full_name = self.sys_device_name + '.' + short_name

                    start_type = command.find('Type="') + len('Type="')
                    res_type = command[start_type:command.find('" />', start_type)]

                    self.current_resource = Resource(short_name=short_name, res_type=res_type, full_name=full_name)

                    # Check
                    successfully = False
                    for sys_resource in self.sys_resources:
                        if sys_resource == self.current_resource:
                            self.sys_resources.remove(sys_resource)
                            self.unstarted_resources.append(sys_resource)
                            self.process_output.append(f'found: {sys_resource.full_name}, '
                                                       f'resources left to check: {len(self.sys_resources)}')
                            successfully = True
                            break

                    if not successfully:
                        self.process_output.append(f'Incorrect resource creation writing in line: {cnt}')
                        self.incorrect_lines.append(line.strip())

                # Collecting fbs
                elif command.find('Action="CREATE"><FB') != -1:
                    # Parse command
                    start_name = command.find('FB Name="') + len('FB Name="')
                    name = command[start_name:command.find('" Type="', start_name)]

                    start_type = command.find('Type="') + len('Type="')
                    fb_type = command[start_type:command.find('" />', start_type)]

                    self.current_fb = FB(name=name, fb_type=fb_type, resource=res)

                    # Check
                    successfully = False
                    for sys_fb in self.sys_fbs:
                        if sys_fb == self.current_fb:
                            self.sys_fbs.remove(sys_fb)
                            self.process_output.append(f'found: {sys_fb.name}, fbs left to check: {len(self.sys_fbs)}')
                            successfully = True
                            break
                    if not successfully:
                        self.process_output.append(f'incorrect fb creation writing in line: {cnt}')
                        self.incorrect_lines.append(line.strip())

                # Collecting fb parameters
                elif command.find('Action="WRITE"') != -1:
                    # Parse command
                    value_start = command.find('Connection Source="') + len('Connection Source="')
                    value = command[value_start:command.find('" Destination="', value_start)]

                    destination_start = command.find('Destination="') + len('Destination="')
                    destination = command[destination_start:command.find('" />', destination_start)]

                    self.current_parameter = Parameter(value=value, destination=destination, fb=self.current_fb)

                    # Check
                    successfully = False
                    for sys_param in self.sys_parameters:
                        if (sys_param.fb == self.current_parameter.fb
                                and sys_param.destination == self.current_parameter.destination):
                            if sys_param.value != self.current_parameter:
                                self.recount_int_parameter()
                            if sys_param.value == self.current_parameter.value:
                                self.sys_parameters.remove(sys_param)
                                self.process_output.append(f'found: {sys_param.value},'
                                                           f' parameters left to check: {len(self.sys_parameters)}')
                                successfully = True
                                break
                    if not successfully:
                        self.process_output.append(f'incorrect writing fb parameter in line: {cnt}')
                        self.incorrect_lines.append(line.strip())

                # Collecting connections
                elif command.find('Action="CREATE"><Connection') != -1:
                    # Parse command
                    source_start = command.find('Connection Source="') + len('Connection Source="')
                    source = command[source_start:command.find('" Destination="', source_start)]

                    destination_start = command.find('Destination="') + len('Destination="')
                    destination = command[destination_start:command.find('" />', destination_start)]

                    self.current_connection = Connection(source=source, destination=destination, resource=res)

                    # Check
                    successfully = False
                    for sys_conn in self.sys_connections:
                        if sys_conn == self.current_connection:
                            self.sys_connections.remove(sys_conn)
                            self.process_output.append(f'found: {sys_conn.source},'
                                                       f' connections left to check: {len(self.sys_connections)}')
                            successfully = True
                            break
                    if not successfully:
                        self.process_output.append(f'incorrect writing connection between fbs in line: {cnt}')
                        self.incorrect_lines.append(line.strip())

                elif command.find('Action="START"'):
                    for resource in self.unstarted_resources:
                        if resource.short_name == res:
                            self.unstarted_resources.remove(resource)
                            break

                else:
                    self.incorrect_lines.append(f'unknown command, line {cnt}')

    # if param like 'base#Digit_Base' recount it in decimal
    def recount_int_parameter(self):
        if '#' in self.current_parameter.value:
            base, value = self.current_parameter.value.split('#', 1)
            if base.isdigit():
                base_int = int(base)
                if 2 <= base_int <= 36:
                    valid_chars = '0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZ'[:base_int]
                    if all(c.upper() in valid_chars for c in value):
                        try:
                            decimal_value = str(int(value, base_int))
                            self.current_parameter.value = decimal_value
                        except ValueError:
                            pass

    def print_process(self):
        print('\n'.join(i for i in self.process_output))

    def print_results(self):
        correct = True
        for key, value in {'resources' : self.sys_resources,
                           'FBs' : self.sys_fbs,
                           'parameters' : self.sys_parameters,
                           'connections' : self.sys_connections}.items():
            if value:
                correct = False
                print(f'Unresolved {key} from sys:')
                for i in value:
                    if key == 'resources':
                        print(f'<Resource Name="{i.short_name}" Type="{i.res_type}"...>')
                    elif key == 'FBs':
                        print(f'<FB Name="{i.name.split('.', 1)[-1]}" Type="{i.fb_type}"...>')
                    elif key == 'parameters':
                        print(f'<Parameter Name="{i.destination.split('.')[-1]}" Value="{i.value}"...>')
                    else:
                        print(f'<Connection Source="{i.source if 'START.' in i.source else i.source.split('.', 1)[-1]}"'
                              f' Destination="{i.destination.split('.', 1)[-1]}"...>')
                print()

        if self.incorrect_lines:
            correct = False
            print('Unexpected elements from fboot in lines:\n', ',\n'.join(f'{i}' for i in self.incorrect_lines), sep='')

        if self.unstarted_resources:
            correct = False
            print('unstarted resources:', ','.join(f'{i}' for i in self.unstarted_resources))

        if correct:
            print('File .fboot fully complies with file .sys')