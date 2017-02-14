package ql.ast.literals;

import ql.ast.ASTNode;
import ql.ast.QLLiteral;
import ql.ast.visistor.ASTVisitor;

/**
 * Created by Erik on 7-2-2017.
 */
public class QLInt  implements ASTNode, QLLiteral {
    private int qlInteger;

    public QLInt(int qlInteger){
        this.qlInteger = qlInteger;
    }

    public <T> T visitThis(ASTVisitor<T> visitor) {
        return visitor.visit(this);
    }
}
