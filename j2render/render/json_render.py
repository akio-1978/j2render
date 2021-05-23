import json
from pathlib import Path
from jinja2 import Environment, FileSystemLoader
from . jinja2_custom_filter import sequential_group_by

# renderの動作を決定するコンテキスト
class JsonRenderContext:
    pass

class JsonRender:

    # jinja2テンプレートの生成
    def __init__(self, *, context):
        self.context = context
        self.build_convert_engine(context = context)

    def render(self, *, source, output):
        result = self.read_source(reader = source)
        result = self.read_finish(all_source = result)
        self.result(result = result, output = output)

    def read_source(self, *, reader):
        return json.load(reader)

    def result(self, *, result, output):
        print(
            self.template.render(
                {'data' : result, 'parameters' : self.context.parameters}
            ),
            file = output
        )

    # 全て読み込みが終わった後に変換が必要な場合の処理
    def read_finish(self, *, all_source):
        # 何もしない
        return all_source

