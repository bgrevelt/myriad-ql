package qls;

import java.util.Map;

import org.antlr.v4.runtime.ANTLRInputStream;
import org.antlr.v4.runtime.CommonTokenStream;

import QL.Faults;
import QL.QLLexer;
import QL.QLParser;
import QL.ast.Form;
import QL.ast.type.Type;
import qls.ast.Stylesheet;


public class Main {
	public static void main(String[] args) throws Exception {
		String tmp = "stylesheet taxOfficeExample "
				 + "page Housing { "
				 + "section \"Buying\" "
				 + "question hasBoughtHouse "
				 + "widget checkbox "
		 		 + "section \"Loaning\" "
				 + "question hasMaintLoan "
				 + "default boolean widget radio(\"Yes\", \"No\") "
				 + "}";
		
		ANTLRInputStream input = new ANTLRInputStream( tmp );

		qlsLexer lexer = new qlsLexer(input);

		CommonTokenStream tokens = new CommonTokenStream(lexer);

		qlsParser parser = new qlsParser(tokens);
		Stylesheet stylesheet = parser.stylesheet().result;
		System.out.println(stylesheet);
		
		qls.semantic.Analyzer analyzer = new qls.semantic.Analyzer(ql());
		
		analyzer.analyze(stylesheet);
		
	}
	
	public static Map<String, Type> ql() {
		String tmp = "form Testing { "
				 + "Name0: \"Question0\" integer "
				 + "Name1: \"Question1\" integer (Name0 + 2)"
				 + "if (Name0 < 5) {"
				 + "if (Name0 == 4) {"
		 		 + "Name2: \"Question2\" boolean"
				 + "} else { "
				 + "Name9: \"Question9\" boolean } } "
				 + "Name3: \"Question3\" string "
				 + "}";

		ANTLRInputStream input = new ANTLRInputStream( tmp );

		QLLexer lexer = new QLLexer(input);

		CommonTokenStream tokens = new CommonTokenStream(lexer);

		QLParser parser = new QLParser(tokens);
		Form form = parser.form().result;

		QL.semantic.Analyzer analyzer = new QL.semantic.Analyzer();

		Faults faults = analyzer.analyze(form);

		return analyzer.getVariableTypes();
	}
}