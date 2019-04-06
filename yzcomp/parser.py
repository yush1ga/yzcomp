import yaml
import sys

from .model import Command, Option, Func


class Parser:
    def __init__(self, file_name):
        with open(file_name) as f:
            self._data = yaml.safe_load(f)

    @staticmethod
    def _parse_option(o):
        if type(o) != dict:
            sys.stderr.write(f'Invalid option: {o}\n')
            exit(1)

        names = o['names']
        arguments = o.get('arguments')
        description = o.get('description')

        # validate description
        if description is None:
            description = ''
        elif type(description) != str:
            sys.stderr.write(f'Invalid description: {description}\n')

        # validate arguments
        if type(arguments) == str:
            arguments = Func(arguments)
        elif type(arguments) == list:
            for v in arguments:
                if type(v) != str:
                    sys.stderr.write(f'Invalid arguments: {arguments}\n')
                    exit(1)
        elif arguments is None:
            pass
        else:
            sys.stderr.write(f'Invalid arguments: {arguments}\n')
            exit(1)

        # validate description
        if description is None:
            description = ''
        elif type(description) != str:
            sys.stderr.write(f'Invalid description: {o}\n')
            exit(1)

        return Option(names, arguments, description)

    @staticmethod
    def _parse(data):
        if type(data) == dict:
            name = data['name']
            options = data.get('options')
            arguments = data.get('arguments')
            description = data.get('description')

            # validate description
            if description is None:
                description = ''
            elif type(description) != str:
                sys.stderr.write(f'Invalid cmd: {data}\n')

            # parse options
            if type(options) == list:
                options = [Parser._parse_option(o) for o in options]
            elif options is None:
                pass
            else:
                sys.stderr.write(f'Invalid options: {options}\n')
                exit(1)

            # parse arguments
            if type(arguments) == list:
                arguments = [Parser._parse(v) for v in arguments]
            elif type(arguments) == str:
                arguments = Func(arguments)
            elif arguments is None:
                pass
            else:
                sys.stderr.write(f'Invalid arguments: {arguments}\n')
                exit(1)

        elif type(data) == str:
            return data
        else:
            sys.stderr.write(f'Parse error!: {data}\n')
            exit(1)

        return Command(name, arguments, options, description)

    def parse(self):
        cmd = self._parse(self._data)
        if type(cmd) != Command:
            sys.stderr.write(f'Parse error!: {self._data}\n')
            exit(1)

        shell = self._data.get('shell')
        if shell is None:
            shell = ''
        elif type(shell) == str:
            pass
        else:
            sys.stderr.write(f'Parse error!: {self._data}\n')
            exit(1)
        return cmd, shell
