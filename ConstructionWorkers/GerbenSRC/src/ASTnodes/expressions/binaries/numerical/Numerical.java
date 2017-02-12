package ASTnodes.expressions.binaries.numerical;

import ASTnodes.CodeLocation;
import ASTnodes.expressions.binaries.Binary;
import ASTnodes.types.IntegerType;
import ASTnodes.types.Type;
import ASTnodes.types.UndefinedType;

/**
 * Created by LGGX on 10-Feb-17.
 */
public abstract class Numerical extends Binary {

    public Numerical(CodeLocation location) {
        super(location);
    }

    @Override
    public Type inferType(Type left, Type right) {

        if (left.equals(right)) {
            if (left.equals(new IntegerType())) {
                return left;
            }
        }

        return new UndefinedType();
    }

}
