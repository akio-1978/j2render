
from j2shrine.command.command import Command
from ..render.json_render import JsonRender
from ..context.json_context import JsonRenderContext

# CommandRunnerのデフォルト実装
class JsonCommand(Command):

    def create_parser(self,*, main_parser):
        return main_parser.add_parser('json', help = 'rendaring json format')

    def newContext(self):
        return JsonRenderContext()

    def get_render(self, *, context):
        return JsonRender(context=context)
