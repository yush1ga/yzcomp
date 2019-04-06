import unittest

from yzcomp import Parser, Generator
from yzcomp.model import Command


class TestParser(unittest.TestCase):

    def test_parse(self):
        parser = Parser('resources/sample.yaml')
        cmd, shell = parser.parse()

        self.assertEqual('dummy', cmd.name)
        self.assertEqual('dummy command', cmd.description)

        arguments = cmd.arguments
        self.assertEqual('sub', arguments[0].name)
        self.assertEqual('normal sub command', arguments[0].description)
        self.assertEqual('opt', arguments[1].name)

        commit: Command = arguments[1]
        self.assertEqual('-m', commit.options[0].names[0])
        self.assertEqual('--message', commit.options[0].names[1])

        print(Generator(cmd, shell).generate())
