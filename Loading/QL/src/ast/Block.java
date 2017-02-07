package ast;

import java.util.List;
import java.util.ArrayList;

public class Block extends Node {
	
	private List<Question> questions;
	
	public List<Question> getQuestions() {
		return questions;
	}
	
	public Block() {
		this.questions = new ArrayList<Question>();
	}
	
	public Block(String tmp) {
		this.questions = new ArrayList<Question>();
	}
	
	public Block(List<Question> questions) {
		// TODO parse into different questions
		this.questions = questions;
	}
	
	public void add(Question question) {
		this.questions.add(question);
	}
	
	void print() {
		// System.out.println(questions.first);
	}
	
}
