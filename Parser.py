import ASTNodeDefs as AST

class Lexer:
    def __init__(self, code):
        self.code = code
        self.position = 0
        self.current_char = self.code[self.position]
        self.tokens = []

    # Move to the next position in the code.
    def advance(self):
        self.position+=1
        if(self.position>=len(self.code)):
            self.current_char=None
        else:
            self.current_char = self.code[self.position]


    # Skip whitespaces.
    def skip_whitespace(self):
        while self.current_char is not None and self.current_char.isspace():
            self.advance()

    # Tokenize an identifier.
    def identifier(self):
        result = ''
        while self.current_char.isalpha() or self.current_char.isdigit() or self.current_char == '_':
            if (self.current_char.isalpha() or self.current_char == '_') and result == '':
                result += self.current_char
            elif (self.current_char.isalpha() or self.current_char == '_' or self.current_char.isdigit()):
                result += self.current_char
            self.advance()
        self.position-=1
        self.current_char = self.code[self.position]
        return ('IDENTIFIER', result)

    # Tokenize a number.
    def number(self):
        num=''
        while not self.current_char.isspace() and self.current_char.isdigit():
            num+=self.current_char
            self.advance()
        return ('NUMBER', int(num))


    def token(self):
        while self.current_char is not None:
            if self.current_char.isspace():
                self.skip_whitespace()
                continue
            if self.current_char.isalpha():
                ident = self.identifier()
                if ident[1] == 'if':
                    return ('IF', 'if')
                elif ident[1] == 'else':
                    return ('ELSE', 'else')
                elif ident[1] == 'while':
                    return ('WHILE', 'while')
                return ident
            if self.current_char.isdigit():
                return self.number()

            # Corrected tokenization logic for operators and punctuation
            if self.current_char in "+-*/=!<>(),:":
                match self.current_char:
                    case '+':
                        self.advance()
                        return ('PLUS', '+')
                    case '-':
                        self.advance()
                        return ('MINUS', '-')
                    case '*':
                        self.advance()
                        return ('MULTIPLY', '*')
                    case '/':
                        self.advance()
                        return ('DIVIDE', '/')
                    case '=':
                        self.advance()
                        if self.current_char == '=':
                            self.advance()
                            return ('EQ', '==')
                        else:
                            return ('EQUALS', '=')
                    case '!':
                        self.advance()
                        if self.current_char == '=':
                            self.advance()
                            return ('NEQ', '!=')
                    case '<':
                        self.advance()
                        return ('LESS', '<')
                    case '>':
                        self.advance()
                        return ('GREATER', '>')
                    case '(':
                        return ('LPAREN', '(')
                    case ')':
                        self.advance()
                        return ('RPAREN', ')')
                    case ',':
                        self.advance()
                        return ('COMMA', ',')
                    case ':':
                        self.advance()
                        return ('COLON', ':')
            raise ValueError(f"Illegal character at position {self.position}: {self.current_char}")
        
        return ('EOF', None)
    # Collect all tokens into a list.
    def tokenize(self):
        while self.position<len(self.code):
            self.tokens.append(self.token())
            self.advance()
        return self.tokens


class Parser:
    def __init__(self, tokens):
        self.tokens = tokens
        self.current_token = tokens.pop(0)  # Start with the first token

    def advance(self):
        # Move to the next token in the list.
        if(self.tokens):
            self.current_token = self.tokens.pop(0)
        else:
            self.current_token = ('EOF',None)

    def parse(self):
        return self.program()

    def program(self):
        """
        Program consists of multiple statements.
        """
        statements = []
        if self.tokens[-1][0] != 'EOF':
            self.tokens.append(('EOF', None))
        while self.current_token[0] != 'EOF':
            statements.append(self.statement())
            self.advance()
        return statements

    def statement(self):
        """
        Determines which type of statement to parse.
        - If it's an identifier, it could be an assignment or function call.
        - If it's 'if', it parses an if-statement.
        - If it's 'while', it parses a while-statement.
        
        """
        if self.current_token[0] == 'IDENTIFIER':
            if self.peek() == 'EQUALS':  # Assignment
                return self.assign_stmt()
            elif self.peek() == 'LPAREN':  # Function call
                return self.function_call()
            else:
                raise ValueError(f"Unexpected token after identifier: {self.peek()}")
        elif self.current_token[0] == 'IF':
            self.expect("IF")
            return self.if_stmt()
        elif self.current_token[0] == 'WHILE':
            self.expect("WHILE")
            return self.while_stmt()
        else:
            # TODO
            if self.current_token[0] == 'COLON':
                return
            raise ValueError(f"Unexpected token: {self.current_token}")


        

    def assign_stmt(self):
        """
        Parses assignment statements.
        Example:
        x = 5 + 3
        """
        identifier=self.current_token
        self.advance()
        self.expect('EQUALS')
        expression=self.expression()
        return AST.Assignment(identifier, expression)

    def if_stmt(self):
        """
        Parses an if-statement, with an optional else block.
        Example:
        if condition:
            # statements
        else:
            # statements
        """
        condition=self.boolean_expression()
        self.advance()
        block=self.block()

        elseBlock = None # If else is not present the code will print the output without the else_branch
        if self.current_token[0] == 'ELSE':
            self.expect('ELSE')  # Move past 'ELSE'
            self.expect('COLON')  # Move past 'COLON'
            elseBlock = self.block()

        if elseBlock is None: # else_branch cases
            return AST.IfStatement(condition, block)
        else:
            return AST.IfStatement(condition, block, elseBlock)

    def while_stmt(self):
        """
        Parses a while-statement.
        Example:
        while condition:
            # statements
        TODO: Implement the logic to parse while loops with a condition and a block of statements.
        """
        
        condition=self.boolean_expression()
        self.advance()
        block=self.block()

        return AST.WhileStatement(condition, block)

    def block(self):
        """
        Parses a block of statements. A block is a collection of statements grouped by indentation.
        Example:
        if condition:
            # This is a block
            x = 5
            y = 10
        TODO: Implement logic to capture multiple statements as part of a block.
        """
        statements = []
        # write your code here
        while (self.current_token[0] not in ['EOF', 'ELSE', 'DEDENT']):
            if(self.current_token[0] != "COLON"):
                statements.append(self.statement())
            self.advance()
        return AST.Block(statements)

    def expression(self):
        """
        Parses an expression. Handles operators like +, -, etc.
        Example:
        x + y - 5
        """
        left = self.term()  # Parse the first term
        while self.peek() in ['PLUS', 'MINUS']:  # Handle + and -
            self.advance()
            op = self.current_token  # Capture the operator
            self.advance()  # Skip the operator
            right = self.term()  # Parse the next term
            left = AST.BinaryOperation(left, op, right)
        return left

    def boolean_expression(self):
        """
        Parses a boolean expression. These are comparisons like ==, !=, <, >.
        Example:
        x == 5
        """
        # write your code here, for reference check expression function
        left = self.expression()
        while self.peek() in ['EQ','NEQ','LESS','GREATER']:
            self.advance()
            op=self.current_token
            self.advance()
            right = self.expression()
            left=AST.BooleanExpression(left, op, right)
        return left

    def term(self):
        """
        Parses a term. A term consists of factors combined by * or /.
        Example:
        x * y / z
        """
        # write your code here, for reference check expression function
        left = self.factor()  # Parse the first term
        while self.peek() in ['MULTIPLY', 'DIVIDE']:  # Handle * and /
            self.advance()
            op = self.current_token  # Capture the operator
            self.advance()  # Skip the operator
            right = self.factor()  # Parse the next term
            left = AST.BinaryOperation(left, op, right)
        return left

    def factor(self):
        """
        Parses a factor. Factors are the basic building blocks of expressions.
        Example:
        - A number
        - An identifier (variable)
        - A parenthesized expression
        """
        if self.current_token[0] == 'NUMBER' or self.current_token[0] == 'IDENTIFIER':
            return self.current_token
        elif self.current_token[0] == 'LPAREN':
            ans = self.expression()
            self.expect('RPAREN')
            return ans
        else:
            raise ValueError(f"Unexpected token in factor: {self.current_token}")

    def function_call(self):
        """
        Parses a function call.
        Example:
        myFunction(arg1, arg2)
        TODO: Implement parsing for function calls with arguments.
        """
        func_name=self.current_token
        self.advance()
        self.expect("LPAREN")
        args=self.arg_list()
        #self.expect("RPAREN")
        
        return AST.FunctionCall(func_name, args)

    def arg_list(self):
        """
        Parses a list of arguments in a function call.
        Example:
        arg1, arg2, arg3
        TODO: Implement the logic to parse comma-separated arguments.
        """
        args = []
        if self.current_token[0] != "RPAREN":
            args.append(self.expression())
            while self.peek() == "COMMA":
                self.advance()
                self.advance()
                args.append(self.expression())
            self.advance()
        return args

    def expect(self, token_type):
       
        if self.current_token[0] == token_type:
            self.advance()  # Move to the next token
        else:
            raise ValueError(f"Expected {token_type} but got {self.current_token}")

    def peek(self):
        if self.tokens:
            return self.tokens[0][0]
        else:
            return None
