#!/usr/bin/python

import lexer

token_exprs = [
    # The skip-overs
    (r'[ \n\t]+',           None),
    (r'#[^\n]*',            None),
    # The reserved characters
    (r':',                  "COLON"),
    # (r'\'',                 "SINGLEQUOTE"),
    # (r'\"',                 "DOUBLEQUOTE"),
    # Operators
    (r'\+',                 "PLUS"),
    (r'\-',                 "MINUS"),
    # Assignments
    (r'=',                  "ASSIGN"),
    # Brackets
    (r'\(',                  "LPAREN"),
    (r'\)',                  "RPAREN"),
    (r'\{',                  "LCURLY"),
    (r'\}',                  "RCURLY"),
    # Types
    (r'boolean',            "BOOLEAN"),
    (r'money',              "MONEY"),
    # Reserved words
    (r'form',               "FORM"),
    (r'hasSoldHouse',       "HASSOLDHOUSE"),
    (r'hasBoughtHouse',     "HASBOUGHTHOUSE"),
    (r'hasMaintLoan',       "HASMAINTLOAN"),
    (r'sellingPrice',       "SELLINGPRICE"),
    (r'privateDebt',        "PRIVATEDEBT"),
    (r'valueResidue',       "VALUERESIDUE"),
    #
    (r'\"(\\.|[^"])*\"',    "DOUBLE_STRING_LITERAL"),
    (r'([a-zA-Z])+',        "IDENTIFIER"),
    (r'.*',                 "UNINDENTIFIED"),
]


def imp_lex(characters):
    return lexer.lex(characters, token_exprs)
