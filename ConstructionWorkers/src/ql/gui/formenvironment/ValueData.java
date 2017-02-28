/**
 * ValueData.java.
 */

package ql.gui.formenvironment;

import ql.gui.formenvironment.values.Value;

import java.util.HashMap;
import java.util.Map;

public class ValueData {

    private Map<String, Value> states;

    public ValueData() {
        this.states = new HashMap<>();
    }

    public Map<String, Value> getMap() { return this.states; }

    public void addValue(String key, Value value) {
        states.put(key, value);
    }

    public Value getValue(String key) {
        return states.get(key);
    }
}
