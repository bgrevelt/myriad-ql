package qls.semantic;

import java.util.ArrayList;
import java.util.HashMap;
import java.util.List;
import java.util.Map;

import QL.ReferenceTable;
import QL.ast.type.Type;
import QL.message.Message;
import QL.message.Error;

class Environment {
	
	private final Map<String, Boolean> variableCovered;
	private final ReferenceTable referenceTable;
	private final List<Message> messages;
	
	public Environment(ReferenceTable referenceTable) {
		
		this.variableCovered = new HashMap<>();	
		this.referenceTable = referenceTable;
		for (String name : referenceTable) {
			variableCovered.put(name, false);
		}
		this.messages = new ArrayList<>(); // TODO move to analyzing part
	}
	
	public List<Message> getMessages() {
		return messages;
	}
	
	public boolean presentInQL(String name) {
		
		return variableCovered.containsKey(name);
	}
	
	public boolean isCovered(String name) {
		return variableCovered.containsKey(name);
	}
	
	public void setCovered(String name) {
		variableCovered.replace(name, true);
	}
	
	// TODO fault without line number
	public void checkCoverage() {
		for (String name : variableCovered.keySet()) {
			if (!variableCovered.get(name)) {
				messages.add(new Error("The variable " + name + 
						" is not defined in QLS", 0));
			}
		}
	}
	
}
