class Evaluate(object):
    def __init__(self, ast, env):
        """ :type ast: AST.QuestionnaireAST """
        self.ast = ast
        self.env = env

    def start_traversal(self):
        # Ensure the environment and error log are empty.
        prev_context = self.env.context
        self.env.context = "Evaluate"
        self.ast.root.accept(self)
        self.env.context = prev_context

    def question_node(self, question_node):
        pass

    def comp_question_node(self, comp_question_node):
        """ :type comp_question_node: AST.CompQuestionNode """
        new_val = comp_question_node.expression.accept(self)
        self.env.set_value(comp_question_node.name.val, new_val)

    def if_node(self, if_node):
        condition = if_node.expression.accept(self)
        if condition:
            if_node.if_block.accept(self)

    def if_else_node(self, if_else_node):
        condition = if_else_node.expression.accept(self)
        assert (type(condition) == bool), \
            "Invalid type if condition, expected boolean got: {}".format(condition)
        if condition:
            if_else_node.if_block.accept(self)
        else:
            if_else_node.else_block.accept(self)

    def neg_node(self, neg_node):
        return not neg_node.expression.accept(self)

    def min_node(self, min_node):
        return - min_node.expression.accept(self)

    def plus_node(self, plus_node):
        return + plus_node.expression.accept(self)

    def mul_node(self, mul_node):
        return mul_node.left.accept(self) * mul_node.right.accept(self)

    def div_node(self, div_node):
        # TODO: What to do with division through zero?
        right_value = div_node.right.accept(self)
        return div_node.left.accept(self) / right_value

    def add_node(self, add_node):
        return add_node.left.accept(self) + add_node.right.accept(self)

    def sub_node(self, sub_node):
        return sub_node.left.accept(self) - sub_node.right.accept(self)

    def lt_node(self, lt_node):
        return lt_node.left.accept(self) < lt_node.right.accept(self)

    def lte_node(self, lte_node):
        return lte_node.left.accept(self) <= lte_node.right.accept(self)

    def gt_node(self, gt_node):
        return gt_node.left.accept(self) > gt_node.right.accept(self)

    def gte_node(self, gte_node):
        return gte_node.left.accept(self) >= gte_node.right.accept(self)

    def eq_node(self, eq_node):
        return eq_node.left.accept(self) == eq_node.right.accept(self)

    def neq_node(self, neq_node):
        return neq_node.left.accept(self) != neq_node.right.accept(self)

    def and_node(self, and_node):
        return and_node.left.accept(self) and and_node.right.accept(self)

    def or_node(self, or_node):
        return or_node.left.accept(self) or or_node.right.accept(self)

    @staticmethod
    def string_node(string_node):
        """ :type string_node: AST.StringNode """
        return string_node.val

    @staticmethod
    def int_node(int_node):
        """ :type int_node: AST.IntNode"""
        return int_node.val

    @staticmethod
    def bool_node(bool_node):
        """ :type bool_node: AST.BoolNode """
        return bool_node.val

    def var_node(self, var_node):
        """ :type var_node: AST.VarNode """
        return self.env.get_value(var_node.val)

    @staticmethod
    def decimal_node(decimal_node):
        """ :type decimal_node: AST.DecimalNode """
        return decimal_node.val

    @staticmethod
    def date_node(date_node):
        """ :type date_node: AST.DateNode """
        return date_node.val
