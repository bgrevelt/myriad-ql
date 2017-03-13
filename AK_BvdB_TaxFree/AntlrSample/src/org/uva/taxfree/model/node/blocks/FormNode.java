package org.uva.taxfree.model.node.blocks;

import org.uva.taxfree.gui.MessageList;
import org.uva.taxfree.model.environment.SymbolTable;
import org.uva.taxfree.model.node.Node;

import java.util.List;

public class FormNode extends BlockNode {
    private final String mFormName;

    public FormNode(String label, List<Node> children) {
        super(children);
        mFormName = label;
    }

    @Override
    public String toString() {
        return mFormName;
    }


    @Override
    public void checkSemantics(SymbolTable symbolTable, MessageList semanticsMessages) {
        symbolTable.getDuplicateDeclarationErrors(semanticsMessages);
        symbolTable.getDuplicateLabelErrors(semanticsMessages);
        super.checkSemantics(symbolTable, semanticsMessages);
    }

}
