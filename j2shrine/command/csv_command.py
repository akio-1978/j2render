
from . base_command import Command
from ..render.csv_render import CsvRender, CsvRenderContext
class CsvCommand(Command):

    def create_parser(self,*, parser_creator):
        return parser_creator.add_parser('csv', help = 'rendaring csv format')

    def add_optional_arguments(self,*, parser):
        print('optional')
        # flag first line is header
        parser.add_argument('-H', '--header', help='with header.', dest='use_header', action='store_true')
        # flag tab separate values
        parser.add_argument('-d', '--delimiter', metavar='', help='column delimiter.', default=',')
        # skip head lines
        parser.add_argument('-s', '--skip-lines', metavar='', help='skip n lines.', default=0)
        return parser

    def context(self):
        return CsvRenderContext()

    def render(self, *, context):
        return CsvRender(context=context)
