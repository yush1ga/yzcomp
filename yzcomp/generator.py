from yzcomp.model import Command, Option, Func
from jinja2 import Environment, BaseLoader, Template
from yzcomp.templates import BODY, CASE, ARGS, VALUES


class Generator:
    def __init__(self, command: Command, shell: str):
        self._command = command
        self._shell = shell

        # template
        self._body: Template = Environment(loader=BaseLoader).from_string(BODY)
        self._case: Template = Environment(loader=BaseLoader).from_string(CASE)
        self._args: Template = Environment(loader=BaseLoader).from_string(ARGS)
        self._values: Template = Environment(loader=BaseLoader).from_string(VALUES)

        self._allowed_commands = []
        self._cases = []
        self._argss = []

    def _generate(self, command: Command, prefix: str):
        self._allowed_commands.append(command.name)
        name = f'{prefix}_{command.name}'

        if not (command.arguments or command.options):
            return

        args=':'
        options = []
        if command.arguments:
            if isinstance(command.arguments, Func):
                args = command.arguments.name
            elif isinstance(command.arguments, list) and isinstance(command.arguments[0], str):
                args = f'{name}_args'
                self._argss.append(
                    self._values.render(name=args, values=command.arguments)
                )
            elif isinstance(command.arguments, list) and isinstance(command.arguments[0], Command):
                args = f'{name}_args'
                commands = [f'{c.name}:{c.description}' for c in command.arguments]
                self._argss.append(
                    self._args.render(name=args, args=commands)
                )
                for c in command.arguments:
                    self._generate(c, name)

        if command.options:
            for opt in command.options:
                opt_name = opt.names[0].lstrip("-")
                dst = ''
                if opt.arguments:
                    if isinstance(opt.arguments, Func):
                        dst = opt.arguments.name
                    elif isinstance(opt.arguments, list):
                        dst = f'{name}_{opt_name}_args'
                        self._argss.append(
                            self._values.render(name=dst, values=opt.arguments)
                        )

                # build option
                if len(opt.names) == 1:
                    o = f"({opt.names[0]}){opt.names[0]}"
                else:
                    o = f"({' '.join(opt.names)})'{'{' + ','.join(opt.names) + '}'}'"

                if opt.description:
                    o += f'[{opt.description}]'

                options.append(f"'{o}'")

                # option case
                if dst:
                    self._cases.append(self._case.render(
                        case=f'{name}_{opt_name}',
                        args=dst,
                    ))

        self._cases.append(
            self._case.render(
                case=name,
                options=options,
                args=args,
            )
        )

    def generate(self):
        self._generate(self._command, '')
        complete = self._body.render(
            name=self._command.name,
            allowed_commands=' '.join(self._allowed_commands),
            cases=self._cases,
            argss=self._argss
        )

        if self._shell:
            complete += f'\n{self._shell}'

        return complete + f'\n\n_{self._command.name} "$@"'
