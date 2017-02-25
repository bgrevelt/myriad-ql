package semantic;
import ast.Form;
import ast.atom.Atom;

import java.util.Map;

public class TypeChecker {

    public Environment analyze(Form form) {
        Environment environment = new Environment();
        QuestionVisitor QVisitor = new QuestionVisitor(environment);
        QVisitor.visit(form);
        environment = QVisitor.getEnvironment(); 
        // TODO if you forget this statement you continue working with the old environment

        ExpressionVisitor expressionVisitor = new ExpressionVisitor(environment);
        expressionVisitor.visit(form);
        return expressionVisitor.getEnvironment();

    }

}