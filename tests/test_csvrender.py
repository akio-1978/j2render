import unittest
from io import StringIO
from j2shrine.csv.csv_render import CsvRender
from j2shrine.csv.csv_context import CsvRenderContext

from jinja2 import Environment, DictLoader
from tests.utils import J2SRenderTest, RenderArgs

class CsvRenderTest(J2SRenderTest):

    def test_convert_headless(self):
        """ヘッダのない単純なCSV"""
        args = RenderArgs()
        args.template = {
            'template': "{% for line in rows %}{{line.col_00}}\n{% endfor %}"}
        args.template_name = 'template'

        context = CsvRenderContext(args=args)
        converter = DictRender(context=context)

        source = StringIO('A0001,C0002\nB0001,C0002\nC0001,C0002')
        result = StringIO()

        converter.render(source=source, output=result)

        self.assertEqual('A0001\nB0001\nC0001\n\n', result.getvalue())

    def test_convert_escaped(self):
        """CSVデータのエスケープ"""
        args = RenderArgs()
        args.template = {
            'template': "{% for line in rows %}{{line.col_00}}\n{% endfor %}"}
        args.template_name = 'template'
        converter = DictRender(context=CsvRenderContext(args=args))

        source = StringIO('"A00,01",C0002\nB0001,C0002\nC0001,C0002')
        result = StringIO()

        converter.render(source=source, output=result)

        self.assertEqual('A00,01\nB0001\nC0001\n\n', result.getvalue())

    def test_header(self):
        """ヘッダ行付き"""
        args = RenderArgs()
        args.template ={'template': "{% for line in rows %}{{line.FIRST}}<=>{{line.SECOND}}{% endfor %}"}
        args.template_name = 'template'
        args.read_header = True
        converter = DictRender(context=CsvRenderContext(args=args))

        source = StringIO('FIRST,SECOND\nC0001,C0002')
        result = StringIO()

        converter.render(source=source, output=result)

        self.assertEqual('C0001<=>C0002\n', result.getvalue())

    def test_simple(self):
        """ヘッダ付きCSVからjsonファイル変換"""
        self.file_convert_test(template='tests/csv/templates/simple.tmpl',
                               expect='tests/csv/expect/simple.txt',
                               source='tests/csv/src/simple.csv')

    def test_skip_with_header(self):
        """先頭3行を読み飛ばした後にヘッダ付き"""
        self.file_convert_test(template='tests/csv/templates/simple.tmpl',
                               expect='tests/csv/expect/skip_with_header.txt',
                               source='tests/csv/src/skip_with_header.csv',
                               skip_lines=3, read_header=True)

    def test_skip_no_header(self):
        """先頭3行を読み飛ばした後にヘッダなし"""
        self.file_convert_test(template='tests/csv/templates/skip_no_header.tmpl',
                               expect='tests/csv/expect/skip_no_header.txt',
                               source='tests/csv/src/skip_no_header.csv',
                               skip_lines=3, read_header=False)

    def test_group_by(self):
        """テンプレート内でgroup byを行う"""
        self.file_convert_test(template='tests/csv/templates/group_by.tmpl',
                               expect='tests/csv/expect/group_by.yml',
                               source='tests/csv/src/group_by.csv')

    def test_parameters(self):
        """変換時のパラメータ渡し"""
        self.file_convert_test(template='tests/csv/templates/parameters.tmpl',
                               expect='tests/csv/expect/parameters.yml',
                               source='tests/csv/src/parameters.csv',
                               parameters={'list_name': 'Yurakucho-line-stations-in-ward'})

    def test_headers_only(self):
        """ヘッダ行だけを読み取る"""
        self.file_convert_test(template='tests/csv/templates/write_headers_only.tmpl',
                               expect='tests/csv/expect/headers_only.txt',
                               source='tests/csv/src/simple.csv')

    def test_auto_naming(self):
        """ヘッダ行とは関係なくカラム名を自動生成する"""
        self.file_convert_test(template='tests/csv/templates/write_headers_only.tmpl',
                               expect='tests/csv/expect/auto_naming.txt',
                               source='tests/csv/src/simple.csv',
                               read_header=False)

    def test_name_by_header(self):
        """テンプレート内でカラム名から値を読み取る"""
        self.file_convert_test(template='tests/csv/templates/names_by_rows.tmpl',
                               expect='tests/csv/expect/over_columns.txt',
                               source='tests/csv/src/over_columns.csv',
                               read_header=True)

    def test_name_by_context(self):
        """カラム名をcontext.namesで指定する"""
        self.file_convert_test(template='tests/csv/templates/names_by_context.tmpl',
                               expect='tests/csv/expect/names_by_context.txt',
                               source='tests/csv/src/names_by_context.csv',
                               read_header=False,
                               names=['group_id', 'number', 'name'],
                               )

    def test_over_columns_use_header(self):
        """ヘッダ行のカラム数を超過する行には、カラム名を自動生成する
            ex:
            headers: group_id, number, name
            columns: group_id, number, name, col03, col04
        """
        self.file_convert_test(template='tests/csv/templates/names_by_rows.tmpl',
                               expect='tests/csv/expect/over_columns.txt',
                               source='tests/csv/src/over_columns.csv',
                               read_header=True)

    def test_over_columns_use_context(self):
        """context.namesのカラム数を超過する行には、カラム名を自動生成する"""
        self.file_convert_test(template='tests/csv/templates/names_by_rows.tmpl',
                               expect='tests/csv/expect/over_columns.txt',
                               source='tests/csv/src/over_columns.csv',
                               read_header=False,
                               skip_lines=1,
                               names=['group_id', 'number', 'name'],
                                )

    def test_header_ignore_context(self):
        """ヘッダ行の使用とnamesが両方指定されている場合、ヘッダが優先される"""
        self.file_convert_test(template='tests/csv/templates/names_by_rows.tmpl',
                               expect='tests/csv/expect/over_columns.txt',
                               source='tests/csv/src/over_columns.csv',
                               names=['invalid', 'names', 'specified'],
                               read_header=True)


    def file_convert_test(self, *, template, expect, source,
                          parameters={}, skip_lines=0, read_header=True, headers=None, names=[]):
        
        args = RenderArgs()
        args.template = template
        # headerの使用有無
        args.read_header = read_header
        args.headers = headers
        # 追加パラメータ
        args.parameters = parameters
        # 行の読み飛ばし
        args.skip_lines = skip_lines
        # カラム名指定
        args.names = names
        
        context = CsvRenderContext(args=args)

        return self.rendering_test(render=CsvRender(context=context), expect_file=expect, source=source)

# テスト用にDictLoaderを使うRender


class DictRender (CsvRender):

    def build_convert_engine(self, *, context):
        self.headers = None
        environment = Environment(loader=DictLoader(context.template))
        self.template = environment.get_template(context.template_name)


if __name__ == '__main__':
    unittest.main()
