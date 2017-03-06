import sys


class ErrorHandler(object):
    def __init__(self):
        self.error_list = []
        self.error_count = 0
        self.warn_count = 0

    def add_warning(self, context, node, message):
        self.warn_count += 1
        self.error_list.append("[{}] {}: {} at line {}, column {}".format(
            "WARNING", context, message, node.line, node.col
        ))

    def add_error(self, context, node, message):
        self.error_count += 1
        self.error_list.append("[{}] {}: {} at line {}, column {}".format(
            "ERROR", context, message, node.line, node.col
        ))

    def add_zero_division_warning(self, context, node):
        message = "Division by zero found"
        self.add_warning(context, node, message)

    def add_dup_label_warning(self, context, question_node):
        message = "Duplicate label found: '{}'".format(question_node.question)
        self.add_warning(context, question_node.question, message)

    def add_cycle_error(self, context, cycles):
        for cycle in cycles:
            message = "Found circular dependency cycle between vars '{}'"\
                .format(cycle)
            error = "[{}] {}: {} '{}'"\
                    .format("ERROR", context, message)
            self.error_list.append(error)
            self.error_count += 1

    def add_binop_error(self, context, node, left, right):
        error_message = "Invalid types for binop '{}': {}, {}"\
                        .format(node.operator, left, right)
        self.add_error(context, node, error_message)

    def add_monop_error(self, context, node, var_type):
        error_message = "Invalid type for unary op '{}': {}"\
                        .format(node.operator, var_type)
        self.add_error(context, node, error_message)

    def add_if_cond_error(self, context, if_node):
        error_message = "Condition not of type boolean"
        self.add_error(context, if_node.expression, error_message)

    def add_undecl_var_error(self, context, var_node):
        error_message = "Variable '{}' is not defined!".format(var_node.val)
        self.add_error(context, var_node, error_message)

    def add_duplicate_error(self, context, node):
        error_message = "Duplicate question declaration found: {}"\
                        .format(node.name.val)
        self.add_error(context, node, error_message)

    def print_errors(self):
        for error in self.error_list:
            print(error)

        if self.error_count:
            print("Found {} error(s) and {} warning(s), stopping execution!"
                  .format(self.error_count, self.warn_count))
            sys.exit()
        elif self.warn_count:
            print ("Found {} warning(s), continuing.".format(self.warn_count))

    def clear_errors(self):
        self.error_list = []
        self.error_count = 0
        self.warn_count = 0
