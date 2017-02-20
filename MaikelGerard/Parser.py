from ParserTokens import ParserTokens as Tokens
from TypeChecking import TypeChecking
import pyparsing as pp
import AST


class QuestionnaireParser(object):
    def __init__(self):
        # Enable caching of parsing logic.
        pp.ParserElement.enablePackrat()
        pp.quotedString.setParseAction(pp.removeQuotes)

        self.expression = self.define_expression()
        self.question = self.define_question()
        self.block = pp.Forward()
        self.conditional = self.define_conditional()

        self.grammar = self.define_grammar()

    @staticmethod
    def embrace(arg, brace_type="round"):
        if brace_type == "round":
            return Tokens.LIT["L_BRACE"] + arg + Tokens.LIT["R_BRACE"]
        elif brace_type == "curly":
            return Tokens.LIT["L_CURLY"] + arg + Tokens.LIT["R_CURLY"]

    def define_question(self):
        return pp.Group(
            pp.quotedString + Tokens.TYPE["VAR"] + Tokens.LIT["COLON"] +
            Tokens.TYPE_NAME +
            pp.Optional(Tokens.LIT["IS"] + self.embrace(self.expression))
        ).addParseAction(AST.QuestionNode)

    def define_conditional(self):
        if_cond = Tokens.KW["IF"] + self.embrace(self.expression) + \
                  self.embrace(self.block, "curly")

        return pp.Group(if_cond + pp.Optional(
            Tokens.KW["ELSE"] + self.embrace(self.block, "curly"))
        ).addParseAction(AST.ConditionalNode)

    def define_grammar(self):
        self.block << pp.Group(
            pp.OneOrMore(self.question | self.conditional)
        ).addParseAction(AST.BlockNode)

        form = Tokens.KW["FORM"] + Tokens.TYPE["VAR"] + self.embrace(
            self.block, "curly"
        )
        form_block = pp.Group(form).addParseAction(AST.FormNode)

        return pp.OneOrMore(form_block).addParseAction(AST.QuestionnaireAST)

    def define_expression(self):
        # Define expressions including operator precedence. Based on:
        # http://pythonhosted.org/pyparsing/pyparsing-module.html#infixNotation
        var_types = (
            Tokens.TYPE["BOOL"].addParseAction(AST.BoolNode) |
            Tokens.TYPE["VAR"].addParseAction(AST.VarNode) |
            Tokens.TYPE["DECIMAL"].addParseAction(AST.DecimalNode) |
            Tokens.TYPE["INT"].addParseAction(AST.IntNode)
        )

        return pp.infixNotation(var_types, [
            (pp.oneOf('- + !'), 1, pp.opAssoc.RIGHT, AST.MonOpNode),
            (pp.oneOf('* /'), 2, pp.opAssoc.LEFT, self.create_binops),
            (pp.oneOf('+ -'), 2, pp.opAssoc.LEFT, self.create_binops),
            (pp.oneOf('< <= > >='), 2, pp.opAssoc.LEFT, self.create_binops),
            (pp.oneOf('== !='), 2, pp.opAssoc.LEFT, self.create_binops),
            (pp.Literal('&&'), 2, pp.opAssoc.LEFT, self.create_binops),
            (pp.Literal('||'), 2, pp.opAssoc.LEFT, self.create_binops),
        ])

    @staticmethod
    def create_binops(src, loc, token):
        token = token[0]
        while len(token) > 1:
            token = [AST.BinOpNode(src, loc, token[:3])] + token[3:]
        return token

    def parse(self, input_str):
        return self.grammar.parseString(input_str, parseAll=True)[0]

if __name__ == '__main__':
    form1 = """
    form taxOfficeExample {
        "Did you sell a house in 2010?" hasSoldHouse: boolean
        "Did you buy a house in 2010?" hasBoughtHouse: boolean
        "Did you enter a loan?" hasMaintLoan: boolean

        if (true == false * 100 * 5 * ! 8.0) {
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