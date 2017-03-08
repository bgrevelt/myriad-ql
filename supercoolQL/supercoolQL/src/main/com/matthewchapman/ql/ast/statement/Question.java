package com.matthewchapman.ql.ast.statement;

import com.matthewchapman.ql.ast.Statement;
import com.matthewchapman.ql.ast.Type;
import com.matthewchapman.ql.validation.QLVisitor;

/**
 * Created by matt on 20/02/2017.
 *
 * Base question class, contains an identifier, type and a possibly calculated value.
 */
public class Question extends Statement {

    private final String name;
    private final Type type;
    private final String text;

    public Question(String name, String text, Type type, int line, int column) {
        this.name = name;
        this.text = text;
        this.type = type;
        this.setColumn(column);
        this.setLine(line);

    }

    public String getName() {
        return this.name;
    }

    public Type getType() { return this.type; }

    public String getText() { return this.text; }


    @Override
    public <T> T accept(QLVisitor<T> visitor) {
        return visitor.visit(this);
    }

}