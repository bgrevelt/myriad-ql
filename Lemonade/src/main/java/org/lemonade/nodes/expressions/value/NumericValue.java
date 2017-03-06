package org.lemonade.nodes.expressions.value;

import org.lemonade.nodes.types.QLDecimalType;
import org.lemonade.nodes.types.QLIntegerType;
import org.lemonade.nodes.types.QLMoneyType;
import org.lemonade.nodes.types.QLType;

/**
 *
 */

public abstract class NumericValue<T> extends ComparableValue<T> {

    public NumericValue(QLType type, T value) {
        super(type, value);
    }

    public abstract NumericValue<?> plus(IntegerValue that);

    public abstract NumericValue<?> plus(DecimalValue that);

    public abstract NumericValue<?> plus(MoneyValue that);

    public abstract NumericValue<?> minus(IntegerValue that);

    public abstract NumericValue<?> minus(DecimalValue that);

    public abstract NumericValue<?> minus(MoneyValue that);

    public abstract NumericValue<?> product(IntegerValue that);

    public abstract NumericValue<?> product(DecimalValue that);

    public abstract NumericValue<?> product(MoneyValue that);

    public abstract NumericValue<?> divide(IntegerValue that);

    public abstract NumericValue<?> divide(DecimalValue that);

    public abstract NumericValue<?> divide(MoneyValue that);

    public abstract NumericValue<?> neg();

    public NumericValue<?> plus(final NumericValue<?> that) {
        if (that.getType().isOf(new QLIntegerType().getClass())) {
            return this.plus((IntegerValue) that);
        } else if (that.getType().isOf(new QLDecimalType().getClass())) {
            return this.plus((DecimalValue) that);
        } else if (that.getType().isOf(new QLMoneyType().getClass())) {
            return this.plus((MoneyValue) that);
        } else {
            throw new IllegalArgumentException();
        }
    }

    public NumericValue<?> product(final NumericValue<?> that) {
        if (that.getType().isOf(new QLIntegerType().getClass())) {
            return this.product((IntegerValue) that);
        } else if (that.getType().isOf(new QLDecimalType().getClass())) {
            return this.product((DecimalValue) that);
        } else if (that.getType().isOf(new QLMoneyType().getClass())) {
            return this.product((MoneyValue) that);
        } else {
            throw new IllegalArgumentException();
        }
    }

    public NumericValue<?> minus(final NumericValue<?> that) {
        if (that.getType().isOf(QLIntegerType.class)) {
            return this.minus((IntegerValue) that);
        } else if (that.getType().isOf(new QLDecimalType().getClass())) {
            return this.minus((DecimalValue) that);
        } else if (that.getType().isOf(new QLMoneyType().getClass())) {
            return this.minus((MoneyValue) that);
        } else {
            throw new IllegalArgumentException();
        }
    }

    public NumericValue<?> divide(final NumericValue<?> that) {
        if (that.getType().isOf(new QLIntegerType().getClass())) {
            return this.divide((IntegerValue) that);
        } else if (that.getType().isOf(new QLDecimalType().getClass())) {
            return this.divide((DecimalValue) that);
        } else if (that.getType().isOf(new QLMoneyType().getClass())) {
            return this.divide((MoneyValue) that);

        } else {
            throw new IllegalArgumentException();
        }
    }
}
