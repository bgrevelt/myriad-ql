﻿namespace OffByOne.Ql
{
    using System;
    using System.Collections;
    using Antlr4.Runtime.Misc;
    using OffByOne.LanguageCore.Ast;
    using OffByOne.LanguageCore.Ast.Expressions;
    using OffByOne.LanguageCore.Ast.Expressions.Binary;
    using OffByOne.LanguageCore.Ast.Expressions.Literals;
    using OffByOne.LanguageCore.Ast.Expressions.Unary;
    using OffByOne.LanguageCore.Ast.Statements;
    using OffByOne.LanguageCore.Ast.Statements.Branch;
    using OffByOne.LanguageCore.Ast.Statements.Questions;
    using OffByOne.Ql.Generated;

    // TODO: Figure out in which project this file should be.
    public class MyQlVisitor : QlBaseVisitor<AstNode>
    {
        public override AstNode VisitForm([NotNull] QlParser.FormContext context)
        {
            string id = context.Identifier().GetText();
            IList statements = this.VisitStatements(context.stat());

            return new FormStatement(id, statements);
        }

        public override AstNode VisitQuestion([NotNull] QlParser.QuestionContext context)
        {
            string id = context.Identifier().GetText();
            string question = context.StringLiteral().GetText();
            var type = context.Type().GetText();
            switch (type)
            {
                case "boolean":
                    return new BooleanQuestionStatement(id, question);
                case "integer":
                    return new IntegerQuestionStatement(id, question);
                case "decimal":
                    return new DecimalQuestionStatement(id, question);
                case "money":
                    return new MoneyQuestionStatement(id, question);
                case "string":
                    return new StringQuestionStatement(id, question);
                case "date":
                    return new DateQuestionStatement(id, question);
                default:
                    throw new ArgumentOutOfRangeException(nameof(type), "Invalid question type.");
            }
        }

        public override AstNode VisitIf([NotNull] QlParser.IfContext context)
        {
            ElseStatement elseStat = null;
            if (context.@else() != null)
            {
                elseStat = (ElseStatement)this.Visit(context.@else());
            }

            Expression condition = (Expression)this.Visit(context.booleanExpression());
            IList statements = this.VisitStatements(context.stat());

            return new IfStatement(condition, statements, elseStat);
        }

        public override AstNode VisitElse([NotNull] QlParser.ElseContext context)
        {
            IList statements = new ArrayList();
            if (context.@if() != null)
            {
                statements.Add(this.Visit(context.@if()));
            }
            else
            {
                statements = this.VisitStatements(context.stat());
            }

            return new ElseStatement(statements);
        }

        // TODO: Probably split this or something.
        public override AstNode VisitBooleanExpression([NotNull] QlParser.BooleanExpressionContext context)
        {
            AstNode node;
            if (context.ChildCount == 1)
            {
                string text = context.GetChild(0).GetText();
                node = new VariableExpression(text);
                if (text == "true" || text == "false")
                {
                    node = new BooleanLiteral(text == "true");
                }
            }
            else if (context.ChildCount == 2)
            {
                Expression exp = (Expression)this.Visit(context.GetChild(1));
                node = new NotExpression(exp);
            }
            else if (context.ChildCount == 3)
            {
                var firstChild = context.GetChild(0);
                if (firstChild.GetText() == "(")
                {
                    Expression exp = (Expression)this.Visit(context.GetChild(1));
                    node = new BracketExpression(exp);
                }
                else
                {
                    node = this.VisitBinaryExpression(context);
                }
            }
            else
            {
                throw new ArgumentException("Unsupported boolean expression.");
            }

            return node;
        }

        public override AstNode VisitNumericExpression([NotNull] QlParser.NumericExpressionContext context)
        {
            return base.VisitNumericExpression(context);
        }

        public override AstNode VisitDateExpression([NotNull] QlParser.DateExpressionContext context)
        {
            string text = context.GetText();
            if (text[0] == '\'')
            {
                return new DateLiteral(text);
            }
            else
            {
                return new VariableExpression(text);
            }
        }

        private AstNode VisitBinaryExpression([NotNull] QlParser.BooleanExpressionContext context)
        {
            Expression lhs = (Expression)this.Visit(context.GetChild(0));
            Expression rhs = (Expression)this.Visit(context.GetChild(2));

            string op = context.GetChild(1).GetText();
            switch (op)
            {
                case "and":
                    return new AndExpression(lhs, rhs);
                case "or":
                    return new OrExpression(lhs, rhs);
                case "+":
                     return new AddExpression(lhs, rhs);
                case "-":
                    return new SubtractExpression(lhs, rhs);
                case "/":
                    return new DivideExpression(lhs, rhs);
                case "*":
                    return new MultiplyExpression(lhs, rhs);
                case ">":
                    return new GreaterThanExpression(lhs, rhs);
                case "<":
                    return new LessThanExpression(lhs, rhs);
                case "==":
                    return new EqualExpression(lhs, rhs);
                case ">=":
                    return new GreaterThanOrEqualExpression(lhs, rhs);
                case "<=":
                    return new LessThanOrEqualExpression(lhs, rhs);
                default:
                    throw new ArgumentException("Unsupported binary expression.");
            }
        }

        private IList VisitStatements([NotNull] QlParser.StatContext[] stats)
        {
            IList statements = new ArrayList(stats.Length);
            foreach (var stat in stats)
            {
                statements.Add(this.Visit(stat));
            }

            return statements;
        }
    }
}
