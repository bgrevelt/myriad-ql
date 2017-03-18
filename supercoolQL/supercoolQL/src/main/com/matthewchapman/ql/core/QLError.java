package com.matthewchapman.ql.core;

import java.util.Objects;

/**
 * Created by matt on 13/03/2017.
 */
public class QLError implements Comparable<QLError> {

    private final String message;
    private final int line;
    private final int column;
    private final String id;

    public QLError(int line, int column, String id, String message) {
        this.message = message;
        this.line = line;
        this.column = column;
        this.id = id;
    }

    @Override
    public String toString() {
        return "Error: " + this.line + ":" + this.column + " - " + this.id + " : " + this.message;
    }

    @Override
    public int compareTo(QLError o) {
        return this.line - o.line;
    }

    @Override
    public boolean equals(Object obj) {
        if (obj == this) {
            return true;
        }

        if (!(obj instanceof QLError)) {
            return false;
        }

        QLError input = (QLError) obj;

        return Objects.equals(this.line, input.line) &&
                Objects.equals(this.column, input.column) &&
                Objects.equals(this.message, input.message);
    }

    @Override
    public int hashCode() {
        return Objects.hash(this.message, this.line, this.column, this.id);
    }
}