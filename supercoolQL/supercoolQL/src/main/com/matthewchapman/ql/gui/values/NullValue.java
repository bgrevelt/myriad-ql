package com.matthewchapman.ql.gui.values;

/**
 * Created by matt on 18/03/2017.
 */
public class NullValue extends Value {

    public final Void value;

    public NullValue() {
        this.value = null;
    }

    @Override
    public Object getValue() {
        return this.value;
    }
}
