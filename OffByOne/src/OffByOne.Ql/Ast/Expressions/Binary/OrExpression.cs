﻿namespace OffByOne.Ql.Ast.Expressions.Binary
{
    using System.Collections.Generic;

    using OffByOne.Ql.Ast.Expressions.Binary.Base;
    using OffByOne.Ql.Visitors.Contracts;

    public class OrExpression : BinaryExpression
    {
        public OrExpression(
            Expression leftExpression,
            Expression rightExpression)
            : base(leftExpression, rightExpression)
        {
        }

        public OrExpression(IList<Expression> expressions)
            : this(expressions[0], expressions[1])
        {
        }

        public override TResult Accept<TResult, TContext>(
            IExpressionVisitor<TResult, TContext> visitor,
            TContext context)
        {
            return visitor.Visit(this, context);
        }
    }
}