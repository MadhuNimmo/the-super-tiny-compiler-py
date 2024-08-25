from the_super_tiny_compiler import tokenizer, parser, transformer, code_generator, compiler

def test_compiler():
    input_str = '(add 2 (subtract 4 2))'
    expected_output = 'add(2, subtract(4, 2));'

    expected_tokens = [
        {'type': 'paren', 'value': '('},
        {'type': 'name', 'value': 'add'},
        {'type': 'number', 'value': '2'},
        {'type': 'paren', 'value': '('},
        {'type': 'name', 'value': 'subtract'},
        {'type': 'number', 'value': '4'},
        {'type': 'number', 'value': '2'},
        {'type': 'paren', 'value': ')'},
        {'type': 'paren', 'value': ')'}
    ]

    expected_ast = {
        'type': 'Program',
        'body': [{
            'type': 'CallExpression',
            'name': 'add',
            'params': [{
                'type': 'NumberLiteral',
                'value': '2'
            }, {
                'type': 'CallExpression',
                'name': 'subtract',
                'params': [{
                    'type': 'NumberLiteral',
                    'value': '4'
                }, {
                    'type': 'NumberLiteral',
                    'value': '2'
                }]
            }]
        }]
    }

    expected_new_ast = {
        'type': 'Program',
        'body': [{
            'type': 'ExpressionStatement',
            'expression': {
                'type': 'CallExpression',
                'callee': {
                    'type': 'Identifier',
                    'name': 'add'
                },
                'arguments': [{
                    'type': 'NumberLiteral',
                    'value': '2'
                }, {
                    'type': 'CallExpression',
                    'callee': {
                        'type': 'Identifier',
                        'name': 'subtract'
                    },
                    'arguments': [{
                        'type': 'NumberLiteral',
                        'value': '4'
                    }, {
                        'type': 'NumberLiteral',
                        'value': '2'
                    }]
                }]
            }
        }]
    }

    # Run the tests
    assert tokenizer(input_str) == expected_tokens, 'Tokenizer should turn `input_str` string into `expected_tokens` array'
    assert parser(expected_tokens) == expected_ast, 'Parser should turn `expected_tokens` array into `expected_ast`'
    assert transformer(expected_ast) == expected_new_ast, 'Transformer should turn `expected_ast` into `expected_new_ast`'
    assert code_generator(expected_new_ast) == expected_output, 'Code Generator should turn `expected_new_ast` into `expected_output`'
    assert compiler(input_str) == expected_output, 'Compiler should turn `input_str` into `expected_output`'

    print('All Passed!')

# Run the tests
test_compiler()
