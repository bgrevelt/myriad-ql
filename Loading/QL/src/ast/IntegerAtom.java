package ast;

public class IntegerAtom extends Atom {
    
	private final Integer value;

    public IntegerAtom(Integer value) {
        this.value = value;
    }

    public Integer getValue() {
        return this.value;
    }
}