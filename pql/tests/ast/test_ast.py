import unittest

from pql.parser.parser import *


class TestAst(unittest.TestCase):
    def test_ast_simple_empty_form(self):
        input_string = "form taxOfficeExample {}"
        parse_result = parse(input_string).asList()
        form_node = parse_result[0]
        self.assertEqual('taxOfficeExample', form_node.name, "Name of node should equal the declared name")
        self.assertEqual(0, len(form_node.children), "Empty form should have no child nodes")

    def test_ast_single_question(self):
        input_string = """
        form taxOfficeExample {
            "Did you sell a house in 2010?" hasSoldHouse: boolean
        }
        """
        parse_result = parse(input_string).asList()
        form_node = parse_result[0]

        self.assertEqual('taxOfficeExample', form_node.name)
        field_node_1 = form_node.children[0]

        self.assertEqual(0, len(field_node_1.children))
        self.assertEqual('field', field_node_1.var_type)
        self.assertEqual('hasSoldHouse', field_node_1.name)
        self.assertEqual('Did you sell a house in 2010?', field_node_1.title)

    def test_ast_double_question(self):
        input_string = """
        form taxOfficeExample {
            "Did you buy a house in 2010?" hasBoughtHouse: boolean
            "Did you sell a house in 2010?" hasSoldHouse: boolean
        }
        """
        parse_result = parse(input_string).asList()
        form_node = parse_result[0]

        self.assertEqual('taxOfficeExample', form_node.name)
        self.assertEqual(2, len(form_node.children))
        field_node_1 = form_node.children[0]
        field_node_2 = form_node.children[1]

        self.assertEqual(0, len(field_node_1.children))
        self.assertEqual('field', field_node_1.var_type)
        self.assertEqual('hasBoughtHouse', field_node_1.name)
        self.assertEqual('Did you buy a house in 2010?', field_node_1.title)

        self.assertEqual(0, len(field_node_2.children))
        self.assertEqual('field', field_node_2.var_type)
        self.assertEqual('hasSoldHouse', field_node_2.name)
        self.assertEqual('Did you sell a house in 2010?', field_node_2.title)

    def test_ast_single_simple_assignment(self):
        input_string = """
        form taxOfficeExample {
            "Value residue:" valueResidue: money =  sellingPrice - privateDebt
        }
        """
        parse_result = parse(input_string).asList()
        form_node = parse_result[0]
        self.assertEqual('taxOfficeExample', form_node.name)
        self.assertEqual(1, len(form_node.children))

        field_node_1 = form_node.children[0]
        self.assertEqual(1, len(field_node_1.children), 'Field node should have 1 node of arithmetic statement')
        self.assertEqual('field', field_node_1.var_type)
        self.assertEqual('valueResidue', field_node_1.name)
        self.assertEqual('Value residue:', field_node_1.title)

        arithmetic_expression_node = field_node_1.children[0]
        self.assertEqual('arithmetic_expression', arithmetic_expression_node.var_type,
                         'First child should have type: arithmetic_expression')
        self.assertEqual(1, len(arithmetic_expression_node.children),
                         'Arithmetic expression should have 1 node as child')

        arithmetic_statement_node = arithmetic_expression_node.children[0]
        self.assertEqual('arithmetic_statement', arithmetic_statement_node.var_type,
                         'First child should have type: arithmetic_statement')

        self.assertEqual(1, len(arithmetic_expression_node.children),
                         'Arithmetic statement should have 1 node as child')

        substraction_node = arithmetic_statement_node.children[0]
        self.assertEqual(0, len(substraction_node.children),
                         'Substraction node should have no nodes as children')
        self.assertEqual('substraction', substraction_node.var_type,
                         'Substraction node should have type substraction')

        self.assertEqual('sellingPrice', substraction_node.lhs)
        self.assertEqual('privateDebt', substraction_node.rhs)
        self.assertEqual('-', substraction_node.operator)

    def test_ast_single_simple_assignment_(self):
        input_string = """
        form taxOfficeExample {
            "Value residue:" valueResidue: money =  sellingPrice + privateDebt - interest
        }
        """
        parse_result = parse(input_string).asList()

    def test_ast_single_simple_assignment_reversed(self):
        input_string = """
        form taxOfficeExample {
            "Value residue:" valueResidue: money =  sellingPrice - privateDebt + interest
        }
        """
        parse_result = parse(input_string).asList()

    def test_ast_single_combi_assignment(self):
        input_string = """
        form taxOfficeExample {
            "Value residue:" valueResidue: money =  (sellingPrice - privateDebt) * debt
        }
        """
        parse_result = parse(input_string).asList()
        form_node = parse_result[0]
        self.assertEqual('taxOfficeExample', form_node.name)
        self.assertEqual(1, len(form_node.children))

        field_node_1 = form_node.children[0]
        self.assertEqual(1, len(field_node_1.children), 'Field node should have 1 node of arithmetic statement')
        self.assertEqual('field', field_node_1.var_type)
        self.assertEqual('valueResidue', field_node_1.name)
        self.assertEqual('Value residue:', field_node_1.title)

        arithmetic_expression_node = field_node_1.children[0]
        self.assertEqual('arithmetic_expression', arithmetic_expression_node.var_type,
                         'First child should have type: arithmetic_expression')
        self.assertEqual(1, len(arithmetic_expression_node.children),
                         'Arithmetic expression should have 1 node as child')

        arithmetic_statement_node = arithmetic_expression_node.children[0]
        self.assertEqual('arithmetic_statement', arithmetic_statement_node.var_type,
                         'First child should have type: arithmetic_statement')

        self.assertEqual(1, len(arithmetic_expression_node.children),
                         'Arithmetic statement should have 1 node as child')

        multiplication_node = arithmetic_statement_node.children[0]
        self.assertEqual(0, len(multiplication_node.children),
                         'Multiplication node should have no nodes as children')
        self.assertEqual('multiplication', multiplication_node.var_type,
                         'Multiplication node should have type multiplication')
        self.assertEqual('debt', multiplication_node.rhs)
        self.assertEqual('*', multiplication_node.operator)

        substraction_node = multiplication_node.lhs
        self.assertEqual(0, len(substraction_node.children),
                         'Substraction node should have no nodes as children')
        self.assertEqual('substraction', substraction_node.var_type,
                         'Substraction node should have type substraction')

        self.assertEqual('sellingPrice', substraction_node.lhs)
        self.assertEqual('privateDebt', substraction_node.rhs)
        self.assertEqual('-', substraction_node.operator)

    def test_ast_single_combi_assignment_(self):
        input_string = """
        form taxOfficeExample {
            "Value residue:" valueResidue: money =  sellingPrice - privateDebt * debt  /  salary + interest
        }
        """
        parse_result = parse(input_string).asList()
        form_node = parse_result[0]
        self.assertEqual('taxOfficeExample', form_node.name)
        self.assertEqual(1, len(form_node.children))

        field_node_1 = form_node.children[0]
        self.assertEqual(1, len(field_node_1.children), 'Field node should have 1 node of arithmetic statement')
        self.assertEqual('field', field_node_1.var_type)
        self.assertEqual('valueResidue', field_node_1.name)
        self.assertEqual('Value residue:', field_node_1.title)

        arithmetic_expression_node = field_node_1.children[0]
        self.assertEqual('arithmetic_expression', arithmetic_expression_node.var_type,
                         'First child should have type: arithmetic_expression')
        self.assertEqual(1, len(arithmetic_expression_node.children),
                         'Arithmetic expression should have 1 node as child')

        arithmetic_statement_node = arithmetic_expression_node.children[0]
        self.assertEqual('arithmetic_statement', arithmetic_statement_node.var_type,
                         'First child should have type: arithmetic_statement')

        self.assertEqual(1, len(arithmetic_expression_node.children),
                         'Arithmetic statement should have 1 node as child')

        multiplication_node = arithmetic_statement_node.children[0]
        self.assertEqual(0, len(multiplication_node.children),
                         'Multiplication node should have no nodes as children')
        self.assertEqual('multiplication', multiplication_node.var_type,
                         'Multiplication node should have type multiplication')
        self.assertEqual('debt', multiplication_node.rhs)
        self.assertEqual('*', multiplication_node.operator)

        substraction_node = arithmetic_statement_node.children[0]
        self.assertEqual(0, len(substraction_node.children),
                         'Substraction node should have no nodes as children')
        self.assertEqual('substraction', substraction_node.var_type,
                         'Substraction node should have type substraction')

        self.assertEqual('sellingPrice', substraction_node.lhs)
        self.assertEqual('privateDebt', substraction_node.rhs)
        self.assertEqual('-', substraction_node.operator)

    def test_ast_if_single_question(self):
        input_string = """
            form taxOfficeExample {
                if (hasSoldHouse) {
                    "What was the selling price?"        sellingPrice: money
                }
            }
        """
        parse_result = parse(input_string).asList()
        form_node = parse_result[0]
        self.assertEqual('taxOfficeExample', form_node.name)
        self.assertEqual(1, len(form_node.children))

        self.assertEqual('taxOfficeExample', form_node.name)
        self.assertEqual(2, len(form_node.children))

        field_node_1 = form_node.children[0]
        field_node_1 = form_node.children[1]

    def test_ast_if_else_single_question(self):
        input_string = """
            form taxOfficeExample {
                if (hasSoldHouse) {
                    "What was the selling price?"        sellingPrice: money
                }
                else {
                    "What was the buying price?"        sellingPrice: money
                }
            }
        """
        parse_result = parse(input_string).asList()
        form_node = parse_result[0]
        self.assertEqual('taxOfficeExample', form_node.name)
        self.assertEqual(1, len(form_node.children))

        self.assertEqual('taxOfficeExample', form_node.name)
        self.assertEqual(2, len(form_node.children))

        field_node_1 = form_node.children[0]
        field_node_1 = form_node.children[1]

    def test_ast_question_with_if_single_question(self):
        input_string = """
            form taxOfficeExample {
                "Did you sell a house in 2010?" hasSoldHouse: boolean
                if (hasSoldHouse) {
                    "What was the selling price?"        sellingPrice: money
                }
            }
        """
        parse_result = parse(input_string).asList()
        form_node = parse_result[0]
        self.assertEqual('taxOfficeExample', form_node.name)
        self.assertEqual(2, len(form_node.children))
        field_node_1 = form_node.children[0]
        field_node_1 = form_node.children[1]