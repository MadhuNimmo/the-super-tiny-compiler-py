import re

def tokenizer(input_str):
    current = 0
    tokens = []

    while current < len(input_str):
        char = input_str[current]

        if char == '(':
            tokens.append({'type': 'paren', 'value': '('})
            current += 1
            continue

        if char == ')':
            tokens.append({'type': 'paren', 'value': ')'})
            current += 1
            continue

        if re.match(r'\s', char):
            current += 1
            continue

        if re.match(r'[0-9]', char):
            value = ''
            while re.match(r'[0-9]', char):
                value += char
                current += 1
                if current < len(input_str):
                    char = input_str[current]
            tokens.append({'type': 'number', 'value': value})
            continue

        if char == '"':
            value = ''
            current += 1
            if current < len(input_str):
                char = input_str[current]
            while char != '"':
                value += char
                current += 1
                if current < len(input_str):
                    char = input_str[current]
            current += 1
            tokens.append({'type': 'string', 'value': value})
            continue

        if re.match(r'[a-zA-Z]', char):
            value = ''
            while re.match(r'[a-zA-Z]', char):
                value += char
                current += 1
                if current < len(input_str):
                    char = input_str[current]
            tokens.append({'type': 'name', 'value': value})
            continue

        raise TypeError(f'I don\'t know what this character is: {char}')

    return tokens

def parser(tokens):
    current = 0

    def walk():
        nonlocal current
        token = tokens[current]

        if token['type'] == 'number':
            current += 1
            return {'type': 'NumberLiteral', 'value': token['value']}

        if token['type'] == 'string':
            current += 1
            return {'type': 'StringLiteral', 'value': token['value']}

        if token['type'] == 'paren' and token['value'] == '(':
            current += 1
            token = tokens[current]
            node = {'type': 'CallExpression', 'name': token['value'], 'params': []}
            current += 1
            token = tokens[current]

            while not (token['type'] == 'paren' and token['value'] == ')'):
                node['params'].append(walk())
                token = tokens[current]

            current += 1
            return node

        raise TypeError(token['type'])

    ast = {'type': 'Program', 'body': []}
    while current < len(tokens):
        ast['body'].append(walk())

    return ast

def traverser(ast, visitor):
    def traverseArray(array, parent):
        for child in array:
            traverseNode(child, parent)

    def traverseNode(node, parent):
        
        methods = visitor.get(node['type'])
        
        if methods and 'enter' in methods:
            methods['enter'](node, parent)

        if node['type'] == 'Program':
            traverseArray(node['body'], node)
        elif node['type'] == 'CallExpression':
            traverseArray(node['params'], node)
        elif node['type'] in ['NumberLiteral', 'StringLiteral']:
            pass
        else:
            raise TypeError(node['type'])

        if methods and 'exit' in methods:
            methods['exit'](node, parent)

    traverseNode(ast, None)

def transformer(ast):
    new_ast = {'type': 'Program', 'body': []}
    ast['_context'] = new_ast['body']

    def call_expression_visitor(node, parent):
        expression = {
            'type': 'CallExpression',
            'callee': {
                'type': 'Identifier',
                'name': node['name']
            },
            'arguments': []
        }

        node['_context'] = expression['arguments']

        if parent['type'] != 'CallExpression':
            expression = {
                'type': 'ExpressionStatement',
                'expression': expression
            }

        parent['_context'].append(expression)

    visitor = {
        'NumberLiteral': {
            'enter': lambda node, parent: parent['_context'].append({
                'type': 'NumberLiteral',
                'value': node['value']
            })
        },
        'StringLiteral': {
            'enter': lambda node, parent: parent['_context'].append({
                'type': 'StringLiteral',
                'value': node['value']
            })
        },
        'CallExpression': {
            'enter': lambda node, parent: call_expression_visitor(node, parent)
        }
    } 

    traverser(ast, visitor)
    return new_ast
def code_generator(ast):
    # Code Generator implementation
    def generate_node(node):
        if node['type'] == 'Program':
            return ''.join(generate_node(statement) for statement in node['body'])

        if node['type'] == 'ExpressionStatement':
            return generate_node(node['expression'])+";"

        if node['type'] == 'CallExpression':
            callee = generate_node(node['callee'])
            args = ', '.join(generate_node(arg) for arg in node['arguments'])
            return f'{callee}({args})'

        if node['type'] == 'Identifier':
            return node['name']

        if node['type'] == 'NumberLiteral':
            return node['value']

        if node['type'] == 'StringLiteral':
            return f'"{node['value']}"'

        raise TypeError(f'Unknown node type: {node["type"]}')

    return generate_node(ast)

def compiler(input):
  tokens = tokenizer(input)
  ast    = parser(tokens)
  newAst = transformer(ast)
  output = code_generator(newAst)

  return output

# Example usage
input_str = "(add 2 (subtract 4 2))"
tokens = tokenizer(input_str)
ast = parser(tokens)
new_ast = transformer(ast)
output = code_generator(new_ast)

print("Tokens:", tokens)
print("AST:", ast)
print("Transformed AST:", new_ast)
print("Generated Code:", output)
