from TypeChecking import TypeChecking
import pyparsing as pp
import AST
import decimal
import datetime


class QuestionnaireParser(object):
    # Define the tokens used for parsing the input.
    LIT = {
        "IS": pp.Literal("=").suppress(),
        "COLON": pp.Literal(":").suppress(),
        "L_CURLY": pp.Literal("{").suppress(),
        "R_CURLY": pp.Literal("}").suppress(),
        "L_BRACE": pp.Literal("(").suppress(),
        "R_BRACE": pp.Literal(")").suppress()
    }

    KW = {
        "FORM": pp.Keyword("form").suppress(),
        "IF": pp.Keyword("if").suppress(),
        "ELSE": pp.Keyword("else").suppress()
    }

    TYPE = {
        "BOOL": (pp.Keyword("true").addParseAction(lambda _: True) |
                 pp.Keyword("false").addParseAction(lambda _: False)),
        "INT": pp.Word(pp.nums).addParseAction(lambda s, l, t: decimal.Decimal(t[0])),
        "VAR": pp.Word(pp.alphas, pp.alphanums + "_"),
        "DECIMAL": pp.Regex("([0-9]+\.[0-9]*)|([0-9]*\.[0-9]+)"),
        "MONEY": pp.Regex("([0-9]+\.[0-9]{0,2})|([0-9]*\.[0-9]{1,2})"),
        "DATE": pp.Regex("^[0-9]{2}-[0-9]{2}-[0-9]{4}$"),
        "STRING": pp.quotedString.addParseAction(pp.removeQuotes)
    }

    TYPE_NAME = pp.oneOf("boolean int string date decimal money")

    def __init__(self):
        # Enable caching of parsing logic.
        pp.ParserElement.enablePackrat()

        self.expression = self.define_expression()
        self.question = self.define_question()
        self.block = pp.Forward()
        self.conditional = self.define_conditional()

        self.grammar = self.define_grammar()

    def round_embrace(self, arg):
        return self.LIT["L_BRACE"] + arg + self.LIT["R_BRACE"]

    def curly_embrace(self, arg):
        return self.LIT["L_CURLY"] + arg + self.LIT["R_CURLY"]

    @staticmethod
    def get_line_loc_info(src, loc):
        col = pp.col(loc, src)
        line = pp.lineno(loc, src)
        return col, line

    def define_question(self):
        question = self.TYPE["STRING"] + self.TYPE["VAR"] + self.LIT["COLON"] + \
                   self.TYPE_NAME
        question = pp.Group(question).addParseAction(AST.QuestionNode)

        computed_question = question + self.LIT["IS"] + self.round_embrace(self.expression)
        computed_question = pp.Group(computed_question).addParseAction(AST.ComputedQuestionNode)
        return computed_question | question

    def define_conditional(self):
        if_cond = self.KW["IF"] + self.round_embrace(self.expression) + \
                  self.curly_embrace(self.block)
        if_else_cond = if_cond + self.KW["ELSE"] + self.curly_embrace(self.block)

        return (pp.Group(if_else_cond).addParseAction(AST.IfElseNode) |
                pp.Group(if_cond).addParseAction(AST.IfNode))

    def define_grammar(self):
        self.block << pp.Group(
            pp.OneOrMore(self.question | self.conditional)
        ).addParseAction(AST.BlockNode)

        form = self.KW["FORM"] + self.TYPE["VAR"] + self.curly_embrace(self.block)
        form_block = pp.Group(form).addParseAction(AST.FormNode)

        return form_block.addParseAction(AST.QuestionnaireAST)

    def create_args(self, src, loc, token):
        line, col = self.get_line_loc_info(src, loc)
        args = token.asList() + [line, col]
        return args

    def create_monop_node(self, src, loc, token):
        monop = token[0]
        ast_class = monop[0]
        monop_expr = monop[1]
        line, col = self.get_line_loc_info(src, loc)
        return ast_class(monop_expr, line, col)

    def define_expression(self):
        # Define expressions including operator precedence. Based on:
        # http://pythonhosted.org/pyparsing/pyparsing-module.html#infixNotation
        var_types = (
            self.TYPE["BOOL"].addParseAction(
                lambda s, l, t: AST.BoolNode(*self.create_args(s, l, t))) |
            self.TYPE["VAR"].addParseAction(AST.VarNode) |
            self.TYPE["DECIMAL"].addParseAction(AST.DecimalNode) |
            self.TYPE["INT"].addParseAction(AST.IntNode) |
            self.TYPE["DATE"].addParseAction(AST.DateNode) |
            self.TYPE["STRING"].addParseAction(AST.StringNode)
        )

        unary_neg = pp.Literal('!').addParseAction(lambda _: AST.NegNode)
        unary_min = pp.Literal('-').addParseAction(lambda _: AST.MinNode)
        unary_plus = pp.Literal('+').addParseAction(lambda _: AST.PlusNode)
        unary_ops = unary_neg | unary_min | unary_plus

        infix_mul = pp.Literal('*').addParseAction(lambda _: AST.MulNode)
        infix_div = pp.Literal('/').addParseAction(lambda _: AST.DivNode)
        arithmetic_level1 = infix_mul | infix_div

        infix_add = pp.Literal('+').addParseAction(lambda _: AST.AddNode)
        infix_sub = pp.Literal('-').addParseAction(lambda _: AST.SubNode)
        arithmetic_level2 = infix_add | infix_sub

        infix_lt = pp.Literal('>').addParseAction(lambda _: AST.LTNode)
        infix_lte = pp.Literal('>=').addParseAction(lambda _: AST.LTENode)
        infix_gte = pp.Literal('<=').addParseAction(lambda _: AST.GTENode)
        infix_gt = pp.Literal('>').addParseAction(lambda _: AST.GTNode)
        logical_level1 = infix_lt | infix_lte | infix_gt | infix_gte

        infix_eq = pp.Literal('==').addParseAction(lambda _: AST.EqNode)
        infix_neq = pp.Literal('!=').addParseAction(lambda _: AST.NeqNode)
        logical_level2 = infix_eq | infix_neq

        infix_and = pp.Literal('&&').addParseAction(lambda _: AST.AndNode)
        infix_or = pp.Literal('||').addParseAction(lambda _: AST.OrNode)

        return pp.infixNotation(var_types, [
            (unary_ops, 1, pp.opAssoc.RIGHT, self.create_monop_node),
            (arithmetic_level1, 2, pp.opAssoc.LEFT, self.create_binops),
            (arithmetic_level2, 2, pp.opAssoc.LEFT, self.create_binops),
            (logical_level1, 2, pp.opAssoc.LEFT, self.create_binops),
            (logical_level2, 2, pp.opAssoc.LEFT, self.create_binops),
            (infix_and, 2, pp.opAssoc.LEFT, self.create_binops),
            (infix_or, 2, pp.opAssoc.LEFT, self.create_binops),
        ])

    def create_binops(self, src, loc, token):
        token = token[0]
        line, col = self.get_line_loc_info(src, loc)

        # As pyparsing returns all terms on the same precedence level at once,
        # it is required to split the resulting tokens into binary operations.
        while len(token) > 1:
            [left, binop_class, right] = token[:3]
            token = [binop_class(left, right, line, col)] + token[3:]
        return token

    def parse(self, input_str):
        return self.grammar.parseString(input_str, parseAll=True)[0]

if __name__ == '__main__':
    form1 = """
    form taxOfficeExample {
        "Did you sell a house in 2010?" hasSoldHouse: boolean
        "Did you buy a house in 2010?" hasBoughtHouse: boolean
        "Did you enter a loan?" hasMaintLoan: boolean

        if (true == false * 100 * 5 * ! 9.0) {
            "What was the selling price?" sellingPrice: money
            "Private debts for the sold house:" privateDebt: money
            "Value residue:" valueResidue: money = (sellingPrice -
            privateDebt)
        }
    }
    """
    parser = QuestionnaireParser()
    parsedAST = parser.parse(form1)
    print parsedAST

    TypeChecking(parsedAST)
