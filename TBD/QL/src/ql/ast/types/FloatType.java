package ql.ast.types;

import ql.ast.expressions.ArithmeticOp;
import ql.ast.expressions.EqualityOp;
import ql.ast.expressions.RelationalOp;

/**
 * Created by Erik on 21-2-2017.
 */
public class FloatType extends NumType {
    @Override
    public Type checkTypes(ArithmeticOp op, Type other) {
        return other.checkTypesEval(op, this);
    }

    @Override
    public Type checkTypes(RelationalOp op, Type other) {
        return other.checkTypesEval(op, this);
    }

    @Override
    public Type checkTypes(EqualityOp op, Type other) {
        return other.checkTypesEval(op, this);
    }

    @Override
    protected Type checkTypesEval(EqualityOp op, FloatType other) {
        return new BooleanType();
    }

    @Override
    public String toString() {
        return "float";
    }
}
