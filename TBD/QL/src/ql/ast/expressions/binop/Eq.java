package ql.ast.expressions.binop;

import ql.ast.Expr;
import ql.ast.expressions.BinOp;
import ql.ast.expressions.EqualityOp;
import ql.ast.visistor.interfaces.ExpressionVisitor;

/**
 * Created by Erik on 7-2-2017.
 */
public class Eq extends BinOp implements EqualityOp {
    public Eq(Expr left, Expr right, int rowNumber) {
        super(left, right, rowNumber);
    }

    public <T> T accept(ExpressionVisitor<T> visitor) {
        return visitor.visit(this);
    }
}
