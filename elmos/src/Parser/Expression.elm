module Parser.Expression exposing (expression)

import AST
    exposing
        ( Expression(Integer, ParensExpression, Var, Boolean, LogicExpression, ComparisonExpression, RelationExpression, ArithmeticExpression)
        , Logic(And, Or)
        , Comparison(Equal, NotEqual)
        , Relation(GreaterThanOrEqual, LessThanOrEqual, LessThan, GreaterThan)
        , Operator(Plus, Minus, Multiply, Divide)
        )
import Combine exposing (Parser, chainl, choice, lazy, string, parens, (<$), (<$>), (*>), (<*), (<|>))
import Combine.Num exposing (int)
import Combine.Extra exposing (trimmed, stringAs)
import List exposing (foldr)
import Parser.Token exposing (variableName)


type alias BinaryOperator =
    Expression -> Expression -> Expression


expression : Parser s Expression
expression =
    lazy <| \() -> foldr chainl atom precedenceOrderedExpressions


precedenceOrderedExpressions : List (Parser s BinaryOperator)
precedenceOrderedExpressions =
    [ orOp
    , andOp
    , comparisonOp
    , relationalOp
    , addOp
    , multiplyOp
    ]


orOp : Parser s BinaryOperator
orOp =
    stringAs "||" (LogicExpression Or)


andOp : Parser s BinaryOperator
andOp =
    stringAs "&&" (LogicExpression And)


comparisonOp : Parser s BinaryOperator
comparisonOp =
    choice
        [ stringAs "==" (ComparisonExpression Equal)
        , stringAs "!=" (ComparisonExpression NotEqual)
        ]


relationalOp : Parser s BinaryOperator
relationalOp =
    choice
        [ stringAs ">=" (RelationExpression GreaterThanOrEqual)
        , stringAs "<=" (RelationExpression LessThanOrEqual)
        , stringAs ">" (RelationExpression GreaterThan)
        , stringAs "<" (RelationExpression LessThan)
        ]


addOp : Parser s BinaryOperator
addOp =
    choice
        [ stringAs "+" (ArithmeticExpression Plus)
        , stringAs "-" (ArithmeticExpression Minus)
        ]


multiplyOp : Parser s BinaryOperator
multiplyOp =
    choice
        [ stringAs "*" (ArithmeticExpression Multiply)
        , stringAs "/" (ArithmeticExpression Divide)
        ]


atom : Parser s Expression
atom =
    lazy <| \() -> trimmed anyAtom


anyAtom : Parser s Expression
anyAtom =
    lazy <|
        \() ->
            choice
                [ varAtom
                , integerAtom
                , booleanAtom
                , parensAtom
                ]


integerAtom : Parser s Expression
integerAtom =
    Integer <$> int


varAtom : Parser s Expression
varAtom =
    Var <$> variableName


booleanAtom : Parser s Expression
booleanAtom =
    Boolean <$> (stringAs "true" True <|> stringAs "false" False)


parensAtom : Parser s Expression
parensAtom =
    ParensExpression <$> parens expression
