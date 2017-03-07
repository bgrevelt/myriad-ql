package org.lemonade.nodes.types;

/**
 *
 */
public class QLBooleanType extends QLType {

    public QLBooleanType() {
    }

    @Override
    public String toString() {
        return "boolean";
    }

    @Override
    public boolean isBoolean() {
        return true;
    }

    @Override
    public boolean isComparable() {
        return true;
    }
}
