﻿namespace OffByOne.Ql.Checker
{
    using System;
    using System.Collections.Generic;

    using MoreDotNet.Extensions.Collections;
    using MoreDotNet.Extensions.Common;

    using OffByOne.LanguageCore.Ast.ValueTypes;
    using OffByOne.LanguageCore.Ast.ValueTypes.Base;
    using OffByOne.LanguageCore.Checker;
    using OffByOne.LanguageCore.Checker.Messages;
    using OffByOne.LanguageCore.Checker.Models;
    using OffByOne.Ql.Ast.Expressions;
    using OffByOne.Ql.Ast.Expressions.Binary;
    using OffByOne.Ql.Ast.Expressions.Binary.Base;
    using OffByOne.Ql.Ast.Expressions.Unary;
    using OffByOne.Ql.Ast.Expressions.Unary.Base;
    using OffByOne.Ql.Ast.Statements;
    using OffByOne.Ql.Ast.Statements.Branch;
    using OffByOne.Ql.Visitors.Contracts;

    using ValueType = OffByOne.LanguageCore.Ast.ValueTypes.Base.ValueType;

    public class TypeCheckerVisitor
        : BaseTypeCheckerVisitor,
        IExpressionVisitor<ValueType>,
        IStatementVisitor<ValueType>
    {
        public TypeCheckerVisitor()
            : this(new CheckerReport())
        {
        }

        public TypeCheckerVisitor(CheckerReport report)
        {
            this.Report = report;
        }

        public CheckerReport Report { get; private set; }

        public ValueType Visit(AddExpression expression)
        {
            return this.CheckBinaryMatematicalExpression(expression);
        }

        public ValueType Visit(SubtractExpression expression)
        {
            return this.CheckBinaryMatematicalExpression(expression);
        }

        public ValueType Visit(MultiplyExpression expression)
        {
            return this.CheckBinaryMatematicalExpression(expression);
        }

        public ValueType Visit(DivideExpression expression)
        {
            return this.CheckBinaryMatematicalExpression(expression);
        }

        public ValueType Visit(AndExpression expression)
        {
            return this.CheckBinaryBooleanLogicExpression(expression);
        }

        public ValueType Visit(OrExpression expression)
        {
            return this.CheckBinaryBooleanLogicExpression(expression);
        }

        public ValueType Visit(EqualExpression expression)
        {
            return this.CheckBinaryComparisonExpression(expression);
        }

        public ValueType Visit(NotEqualExpression expression)
        {
            return this.CheckBinaryComparisonExpression(expression);
        }

        public ValueType Visit(GreaterThanExpression expression)
        {
            return this.CheckBinaryComparisonExpression(expression);
        }

        public ValueType Visit(GreaterThanOrEqualExpression expression)
        {
            return this.CheckBinaryComparisonExpression(expression);
        }

        public ValueType Visit(LessThanExpression expression)
        {
            return this.CheckBinaryComparisonExpression(expression);
        }

        public ValueType Visit(LessThanOrEqualExpression expression)
        {
            return this.CheckBinaryComparisonExpression(expression);
        }

        public ValueType Visit(NotExpression expression)
        {
            return this.CheckUnaryBooleanLogicExpression(expression);
        }

        public ValueType Visit(NegativeExpression expression)
        {
            return this.CheckUnaryMatematicalExpression(expression);
        }

        public ValueType Visit(PositiveExpression expression)
        {
            return this.CheckUnaryMatematicalExpression(expression);
        }

        public ValueType Visit(VariableExpression expression)
        {
            // TODO: Need to add a enviorment to the visitor
            throw new System.NotImplementedException();
        }

        public ValueType Visit(BracketExpression expression)
        {
            return expression.Expression.Accept(this);
        }

        public ValueType Visit(LiteralExpression expression)
        {
            return expression.Literal.Accept(this);
        }

        public ValueType Visit(QuestionStatement expression)
        {
            return new VoidValueType();
        }

        public ValueType Visit(IfStatement expression)
        {
            var result = this.CheckIfStatement(expression);
            expression.Statements.ForEach(x => x.Accept(this));
            expression.ElseStatements.ForEach(x => x.Accept(this));

            return result;
        }

        public ValueType Visit(FormStatement expression)
        {
            expression.Statements.ForEach(x => x.Accept(this));

            return new VoidValueType();
        }

        private ValueType CheckBinaryMatematicalExpression(BinaryExpression expression)
        {
            var leftExpressionType = expression.LeftExpression.Accept(this);
            var rightEpressionType = expression.RightExpression.Accept(this);

            if (leftExpressionType is IntegerValueType && rightEpressionType is IntegerValueType)
            {
                return new IntegerValueType();
            }

            if (leftExpressionType is FloatValueType || rightEpressionType is FloatValueType)
            {
                return new FloatValueType();
            }

            if (leftExpressionType is MoneyValueType || rightEpressionType is MoneyValueType)
            {
                return new MoneyValueType();
            }

            throw new Exception("Ivalid argument");
        }

        private ValueType CheckUnaryMatematicalExpression(UnaryExpression expression)
        {
            var subExpressionType = expression.Expression.Accept(this);
            if (subExpressionType.IsNot<NumericalValueType>())
            {
                this.Report.Add(new InvaildTypeMessage(
                    expression,
                    new List<ValueType> { new IntegerValueType(), new FloatValueType(), new MoneyValueType() },
                    subExpressionType,
                    LogLevel.Error));
            }

            return subExpressionType;
        }

        private ValueType CheckBinaryComparisonExpression(BinaryExpression expression)
        {
            var leftExpressionType = expression.LeftExpression.Accept(this);
            var rightEpressionType = expression.RightExpression.Accept(this);

            if (leftExpressionType != rightEpressionType)
            {
                this.Report.Add(new InvaildTypeMessage(expression, leftExpressionType, rightEpressionType, LogLevel.Error));
            }

            return new BooleanValueType();
        }

        private ValueType CheckBinaryBooleanLogicExpression(BinaryExpression expression)
        {
            var leftExpressionType = expression.LeftExpression.Accept(this);
            var rightEpressionType = expression.RightExpression.Accept(this);

            if (leftExpressionType is BooleanValueType && rightEpressionType is BooleanValueType)
            {
                return new BooleanValueType();
            }

            throw new Exception("Only boolean arguments are allowed.");
        }

        private ValueType CheckUnaryBooleanLogicExpression(UnaryExpression expression)
        {
            var subExpressionType = expression.Expression.Accept(this);
            if (subExpressionType is BooleanValueType)
            {
                return new BooleanValueType();
            }

            throw new Exception("Only boolean arguments are allowed.");
        }

        private ValueType CheckIfStatement(IfStatement statement)
        {
            var conditionType = statement.Condition.Accept(this);
            if (!(conditionType is BooleanValueType))
            {
                this.Report.Add(new InvaildTypeMessage(statement, new BooleanValueType(), conditionType, LogLevel.Error));
            }

            return new VoidValueType();
        }
    }
}
