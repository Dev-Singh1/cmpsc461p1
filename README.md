### Updated README for Python Parser Project

# CMPSC-461: Parser for a Custom Programming Language

This project implements a **lexer** and **parser** for a simple custom programming language as part of the coursework for CMPSC-461, Fall 2024. The language supports fundamental constructs like arithmetic expressions, boolean expressions, variable assignments, control flow structures (if-else, while loops), and function calls. The primary objective is to understand and apply parsing techniques and abstract syntax tree (AST) generation.

---

## Project Outline

### 1. Lexer
The lexer tokenizes the input code into meaningful tokens:
- Handles keywords (`if`, `else`, `while`), operators (`+`, `-`, `*`, `/`, `==`, `!=`, `<`, `>`), and delimiters (`(`, `)`, `,`, `:`).
- Recognizes identifiers and numeric literals.
- Skips irrelevant whitespaces.

### 2. Parser
The parser processes the tokenized input and constructs an AST:
- **Recursive Descent Parsing**: Implements grammar rules for:
  - Assignments (`x = 10`)
  - Binary operations (`x + y`)
  - Boolean expressions (`x == y`)
  - Control flow (`if`, `else`, `while`)
  - Function calls (`foo(x + 20)`)
- Adheres to the provided grammar and constructs nodes for valid statements and expressions.

### 3. AST Representation
- Uses predefined **ASTNodeDefs** to build ASTs for all supported constructs.
- Outputs ASTs in the expected format (verified using `verify.py`).

---

## Grammar

The custom language is defined by the following grammar rules:

```
program        ::= statement*
statement      ::= assign_stmt | if_stmt | while_stmt | expr_stmt | function_call
assign_stmt    ::= IDENTIFIER '=' expression
if_stmt        ::= 'if' boolean_expression ':' block ('else' ':' block)?
while_stmt     ::= 'while' boolean_expression ':' block
block          ::= statement*
expr_stmt      ::= expression
function_call  ::= IDENTIFIER '(' arg_list? ')'
arg_list       ::= expression (',' expression)*
boolean_expr   ::= term (( '==' | '!=' | '>' | '<' ) term)*
expression     ::= term (( '+' | '-' ) term)*
term           ::= factor (( '*' | '/' ) factor)*
factor         ::= NUMBER | IDENTIFIER | '(' expression ')'
IDENTIFIER     ::= [a-zA-Z_][a-zA-Z0-9_]*
NUMBER         ::= [0-9]+
```

---

## Example Code and Derivation

### Input Code:
```python
x = 10
if x > 10:
    foo(x + 20)
```

### Derivation for `x = 10`:
```
statement     ::= assign_stmt
assign_stmt   ::= IDENTIFIER '=' expression
IDENTIFIER    ::= x
expression    ::= term
term          ::= factor
factor        ::= NUMBER
NUMBER        ::= 10
```

### Derivation for `if x > 10: foo(x + 20)`:
```
statement     ::= if_stmt
if_stmt       ::= 'if' boolean_expression ':' block
boolean_expr  ::= term '>' term
term          ::= factor
factor        ::= IDENTIFIER
IDENTIFIER    ::= x
term          ::= factor
factor        ::= NUMBER
NUMBER        ::= 10
block         ::= statement
statement     ::= function_call
function_call ::= IDENTIFIER '(' arg_list ')'
IDENTIFIER    ::= foo
arg_list      ::= expression
expression    ::= term '+' term
term          ::= factor
factor        ::= IDENTIFIER
IDENTIFIER    ::= x
term          ::= factor
factor        ::= NUMBER
NUMBER        ::= 20
```

---

## Example ASTs

### Test Case 1:
```python
x = 5
y = y + x
```

**AST Representation**:
```python
[Assignment(('IDENTIFIER', 'x'), ('NUMBER', 5)),
 Assignment(('IDENTIFIER', 'y'), 
   BinaryOperation(('IDENTIFIER', 'y'), ('PLUS', '+'), ('IDENTIFIER', 'x')))]
```

### Test Case 2:
```python
if x != y:
    z = 100
```

**AST Representation**:
```python
[IfStatement(BooleanExpression(('IDENTIFIER', 'x'), ('NEQ', '!='), ('IDENTIFIER', 'y')),
 Block([Assignment(('IDENTIFIER', 'z'), ('NUMBER', 100))]),
 None)]
```

---




## Academic Integrity

Strict adherence to the university's academic integrity policies is expected. 

---
