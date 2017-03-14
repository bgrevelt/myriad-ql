# coding=utf-8
from pql.parser.parser import parse
from tests.shared import Shared


class TestEnvironmentCreator(Shared):

    def test_parse_field_money_default(self):
        input_string = """
        form taxOfficeExample {
            "Value residue:" valueResidue: money
        }
        """
        form_node = self.acquire_ast(input_string)

        environment = self.acquire_environment(form_node)
        self.assertEqual(environment['valueResidue'], float(0.0), 'valueResidue should be in environment')

    def test_parse_field_integer_default(self):
        input_string = """
        form taxOfficeExample {
            "Value residue:" valueResidue: integer
        }
        """
        form_node = self.acquire_ast(input_string)

        environemnt = self.acquire_environment(form_node)
        self.assertEqual(environemnt['valueResidue'], int(0), 'valueResidue should be in environment')

    def test_parse_field_boolean_default(self):
        input_string = """
        form taxOfficeExample {
            "Value residue:" valueResidue: boolean
        }
        """
        form_node = self.acquire_ast(input_string)

        environemnt = self.acquire_environment(form_node)
        self.assertEqual(environemnt['valueResidue'], False, 'valueResidue should be in environment')
