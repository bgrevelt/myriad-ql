package qls.astnodes.styles;

import ql.astnodes.LineNumber;
import qls.astnodes.visitors.StyleSheetVisitor;

/**
 * Created by LGGX on 03-Mar-17.
 */
public class Font extends StyleType{

    private static final String NAME = "font";

    public Font(String value, LineNumber lineNumber) {
        super(NAME, value, lineNumber);
    }

    public <T> T accept(StyleSheetVisitor<T> visitor) {
        return visitor.visit(this);
    }
}
