from unittest import TestCase
from unittest.mock import patch, MagicMock
from typesafe_conductr_cli.conduct import build_parser, get_cli_parameters
from argparse import Namespace

class TestConduct(TestCase):

    parser = build_parser()

    def test_parser_version(self):
        args = self.parser.parse_args("version".split())

        self.assertEqual(args.func.__name__, "version")

    def test_parser_info(self):
        args = self.parser.parse_args("info --host 127.0.1.1 --port 9999".split())

        self.assertEqual(args.func.__name__, "info")
        self.assertEqual(args.host, "127.0.1.1")
        self.assertEqual(args.port, 9999)
        self.assertEqual(args.verbose, False)

    def test_parser_load(self):
        args = self.parser.parse_args("load --host 127.0.1.1 --port 9999 -v --nr-of-cpus 2 --memory 100 --disk-space 200 --roles role1 role2 -- path-to-bundle path-to-conf".split())

        self.assertEqual(args.func.__name__, "load")
        self.assertEqual(args.host, "127.0.1.1")
        self.assertEqual(args.port, 9999)
        self.assertEqual(args.verbose, True)
        self.assertEqual(args.nr_of_cpus, 2)
        self.assertEqual(args.memory, 100)
        self.assertEqual(args.disk_space, 200)
        self.assertEqual(args.roles, ["role1", "role2"])
        self.assertEqual(args.bundle, "path-to-bundle")
        self.assertEqual(args.configuration, "path-to-conf")

    def test_parser_run(self):
        args = self.parser.parse_args("run --host 127.0.1.1 --port 9999 --scale 5 path-to-bundle".split())

        self.assertEqual(args.func.__name__, "run")
        self.assertEqual(args.host, "127.0.1.1")
        self.assertEqual(args.port, 9999)
        self.assertEqual(args.verbose, False)
        self.assertEqual(args.scale, 5)
        self.assertEqual(args.bundle, "path-to-bundle")

    def test_parser_stop(self):
        args = self.parser.parse_args("stop --host 127.0.1.1 --port 9999 path-to-bundle".split())

        self.assertEqual(args.func.__name__, "stop")
        self.assertEqual(args.host, "127.0.1.1")
        self.assertEqual(args.port, 9999)
        self.assertEqual(args.verbose, False)
        self.assertEqual(args.bundle, "path-to-bundle")

    def test_parser_unload(self):
        args = self.parser.parse_args("unload --host 127.0.1.1 --port 9999 path-to-bundle".split())

        self.assertEqual(args.func.__name__, "unload")
        self.assertEqual(args.host, "127.0.1.1")
        self.assertEqual(args.port, 9999)
        self.assertEqual(args.verbose, False)
        self.assertEqual(args.bundle, "path-to-bundle")

    def test_get_cli_parameters(self):
        args = Namespace(host="127.0.0.1", port=9005)
        self.assertEqual(get_cli_parameters(args), "")

        args = Namespace(host="127.0.1.1", port=9005)
        self.assertEqual(get_cli_parameters(args), " --host 127.0.1.1")

        args = Namespace(host="127.0.0.1", port=9006)
        self.assertEqual(get_cli_parameters(args), " --port 9006")

        args = Namespace(host="127.0.1.1", port=9006)
        self.assertEqual(get_cli_parameters(args), " --host 127.0.1.1 --port 9006")