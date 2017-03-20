package org.ql.gui.elements.visitor;

import org.junit.Test;
import org.mockito.invocation.InvocationOnMock;
import org.mockito.stubbing.Answer;
import org.ql.ast.Form;
import org.ql.ast.Identifier;
import org.ql.ast.Statement;
import org.ql.ast.expression.Parameter;
import org.ql.ast.expression.arithmetic.Addition;
import org.ql.ast.expression.literal.BooleanLiteral;
import org.ql.ast.expression.literal.IntegerLiteral;
import org.ql.ast.statement.IfThenElse;
import org.ql.ast.statement.Question;
import org.ql.ast.statement.question.QuestionLabel;
import org.ql.ast.type.IntegerType;
import org.ql.evaluator.ValueTable;
import org.ql.evaluator.value.IntegerValue;
import org.ql.gui.elements.Element;
import org.ql.gui.elements.ElementContainer;
import org.ql.gui.elements.IntegerElement;
import org.ql.gui.mediator.GUIMediator;
import org.ql.gui.widgets.IntegerInputWidget;

import java.util.ArrayList;
import java.util.List;

import static org.mockito.Matchers.any;
import static org.mockito.Mockito.mock;
import static org.mockito.Mockito.when;

public class BranchVisitorTest {

    @Test
    public void shouldMakeValueTableWithBranchedQuestions() {
        ValueTable valueTable = new ValueTable();
        valueTable.declare(new Identifier("first"), new IntegerValue(12));
        valueTable.declare(new Identifier("second"), new IntegerValue(48));
        valueTable.declare(new Identifier("third"), new IntegerValue(48));

        BranchVisitor visitor = new BranchVisitor(new ElementContainer(mockQuestionElementBuilder()));
        List<Element> visibleElements = visitor.visitForm(new Form(new Identifier("Example"), new ArrayList<Statement>() {{
            add(new IfThenElse(new BooleanLiteral(true), new ArrayList<Statement>() {{
                add(new Question(new Identifier("first"), new QuestionLabel("Question"), new IntegerType(), new IntegerLiteral(12)));
            }}, new ArrayList<Statement>() {{
                add(new Question(new Identifier("second"), new QuestionLabel("Question2"), new IntegerType(), new Parameter(new Identifier("third"))));
                add(new Question(new Identifier("third"), new QuestionLabel("Question2"), new IntegerType(), new Addition(
                        new IntegerLiteral(13), new IntegerLiteral(35)
                )));
            }}));
        }}), valueTable);
    }

    private QuestionElementFactory mockQuestionElementBuilder() {
        QuestionElementFactory elementBuilder = mock(QuestionElementFactory.class);
        when(elementBuilder.visitIntegerType(any(IntegerType.class), any(Question.class))).thenAnswer(new Answer<IntegerElement>() {
            @Override
            public IntegerElement answer(InvocationOnMock invocationOnMock) throws Throwable {
                return new IntegerElement(mock(GUIMediator.class), mock(Identifier.class), mock(IntegerInputWidget.class));
            }
        });
        return elementBuilder;
    }
}