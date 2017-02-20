require_relative 'base_checker'
require_relative 'type_visitor'

class OperandsTypeChecker < BaseChecker
  def visit_form(subject)
    # get all variables and their types as defined by the questions
    # e.g. {"hasSoldHouse"=>#<BooleanType:0x007f959593fb70>, "hasBoughtHouse"=>#<BooleanType:0x007f9594969ac0>}
    @types = subject.accept(TypeVisitor.new)
    # do the actual operands type checking
    subject.statements.map { |statement| visit_statement(statement) }.flatten.compact
  end

  # visit calculation of the question
  def visit_question(subject)
    visit_calculation(subject.assignment) if subject.assignment
  end

  # visit calculation of if condition and visit all statements in if block
  def visit_if_statement(subject)
    test = []
    test.push(visit_calculation(subject.expression))
    test.push(subject.block.map { |statement| visit_statement(statement) })
  end

  # variable is useless here
  def visit_variable(_)
  end

  # an expression is checked for correctness
  def visit_expression(subject)
    subject_type = subject.class.real_type

    if subject.left.kind_of?(Variable)
      left_type = @types[subject.left.name].class
    else
      left_type = subject.left.class.real_type
    end

    if subject.right.kind_of?(Variable)
      right_type = @types[subject.right.name].class
    else
      right_type = subject.right.class.real_type
    end

    test = []
    # the left side does not match the operator
    if subject_type != left_type
      test.push("[ERROR]: #{subject.left.name} of type #{left_type} can not be used with #{subject.class.to_operator} operator")
    end

    # the right side does not match the operator
    if subject_type != right_type
      test.push("[ERROR]: #{subject.right.name} of type #{right_type} can not be used with #{subject.class.to_operator} operator")
    end

    # the left and right side do not match
    if left_type != right_type
      test.push("[ERROR]: #{subject.left.name} of type #{left_type} can not be used with #{subject.right.name} of type #{right_type}")
    end

    test.push([visit_calculation(subject.left), visit_calculation(subject.right)])
  end
end