from __future__ import print_function
from cloudmesh.shell.command import command
from cloudmesh.shell.command import PluginCommand
from cloudmesh.gdrive.api.manager import Manager
from cloudmesh.common.console import  Console
from cloudmesh.common.util import path_expand
from pprint import pprint


class GdriveCommand(PluginCommand):

    # noinspection PyUnusedLocal
    @command
    def do_gdrive(self, args, arguments):
        """
        ::

          Usage:
            storage [--storage=<SERVICE>] create dir DIRECTORY
            storage [--storage=<SERVICE>] list SOURCE [--recursive]
            storage [--storage=<SERVICE>] put SOURCE DESTINATION [--recursive]
            storage [--storage=<SERVICE>] get SOURCE DESTINATION [--recursive]
            storage [--storage=<SERVICE>] delete SOURCE
            storage [--storage=<SERVICE>] search DIRECTORY FILENAME [--recursive]


          This command does some useful things.

          Arguments:
              FILE   a file name

          Options:
              -f      specify the file

        """
        arguments.FILE = arguments['--file'] or None

        print(arguments)

        m = Manager()


        if arguments.FILE:
            print("option a")
            m.list(path_expand(arguments.FILE))

        elif arguments.list:
            print("option b")
            m.list("just calling list without parameter")


        Console.error("This is just a sample")
        return ""

