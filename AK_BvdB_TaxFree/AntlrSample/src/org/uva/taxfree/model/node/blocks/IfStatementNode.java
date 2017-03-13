package org.uva.taxfree.model.node.blocks;

import org.uva.taxfree.model.environment.SymbolTable;
import org.uva.taxfree.model.node.Node;
import org.uva.taxfree.model.node.expression.ExpressionNode;

import java.util.List;

public class IfStatementNode extends BlockNode {
    private final ExpressionNode expression;

    public IfStatementNode(ExpressionNode expression, List<Node> children) {
        super(children);
        this.expression = expression;
    }

    @Override
    public void fillSymbolTable(SymbolTable symbolTable) {
        symbolTable.addExpression(expression);
    }


}