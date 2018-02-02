from collections import deque
import sys
import math


VALID_START_SYMBOLS = set(
    "abcdefghijklmnopqrstuvwxyz"
    "ABCDEFGHIJKLMNOPQRSTUVWXYZ_")

_symbol_table = {
    "pi": math.pi,
    "e": math.exp(1)
}


def _lookup(sym):
    try:
        sym = float(sym)
    except Exception:
        res = _symbol_table.get(sym)
        if res is None:
            raise ValueError("Unbound symbol: {}".format(sym))
        return res

    return sym


def _is_valid_variable_name(name):
    if name in _OPERATORS:
        return False

    if isinstance(name, str):
        return name[0] in VALID_START_SYMBOLS

    return False


def _assignment(target, value):
    if not target:
        raise ValueError("Bad target")

    if not _is_valid_variable_name(target):
        raise ValueError("Illegal variable name: {}"
                         .format(target))

    val = _lookup(value)

    _symbol_table[target] = _lookup(val)

    return val


def _cond(predicate, iftrue, otherwise):
    return (_lookup(iftrue) if bool(_lookup(predicate)) else _lookup(otherwise))


_OPERATORS = {
    '*': {
        'num_args': 2,
        'apply': lambda x, y: _lookup(x) * _lookup(y)
    },
    '/': {
        'num_args': 2,
        'apply': lambda x, y: _lookup(x) / _lookup(y)
    },
    '+': {
        'num_args': 2,
        'apply': lambda x, y: _lookup(x) + _lookup(y)
    },
    '-': {
        'num_args': 2,
        'apply': lambda x, y: _lookup(x) - _lookup(y)
    },
    'sin': {
        'num_args': 1,
        'apply': lambda x: math.sin(_lookup(x))
    },
    'cos': {
        'num_args': 1,
        'apply': lambda x: math.cos(_lookup(x))
    },
    'exp': {
        'num_args': 1,
        'apply': lambda x: math.exp(_lookup(x))
    },
    'tan': {
        'num_args': 1,
        'apply': lambda x: math.tan(_lookup(x))
    },
    '=': {
        'num_args': 2,
        'apply': _assignment
    },
    '?': {
        'num_args': 3,
        'apply': _cond
    },
    'log': {
        'num_args': 1,
        'apply': lambda x: math.log(_lookup(x))
    }
}


def _eval(tokens):
    stack = []

    while tokens:
        tok = tokens.popleft()

        if tok not in _OPERATORS:
            stack.append(tok)
            continue

        # apply operator

        op = _OPERATORS[tok]
        num_args = op['num_args']
        args = deque()
        for i in range(num_args):
            if stack:
                arg = stack.pop()
                args.appendleft(arg)
            else:
                raise ValueError("Invalid number of args to {}"
                                 .format(tok))

        res = op['apply'](*args)
        stack.append(res)

    res = _lookup(stack.pop())

    if len(stack) > 0:
        raise ValueError("Invalid expression")

    return res


def _tokenize(expr):
    result = deque()
    tokens = expr.split(' ')
    for t in tokens:
        if t in _OPERATORS:
            result.append(t)
            continue

        try:
            val = float(t)
        except Exception:
            result.append(t)
        else:
            result.append(val)

    return result


def _run_tests():
    tests = [
        ("3 5 * 2 + 7 -", 10),
        ("3 5 10 + *", 45),
        ("1 3.14 sin +", 1),
        ("1", 1),
        ("2 pi *", 6.28),
        ("x 3 =", 3),
        ("x", 3)
    ]

    for test in tests:
        expr = test[0]
        expected = test[1]
        tokens = _tokenize(expr)
        result = _eval(tokens)
        print('Test "{}", expected: {}, actual: {}'
              .format(expr, expected, result))


def eval_expr(expr):
    return _eval(_tokenize(expr))


def main(args):
    while True:
        expr = input("> ")
        expr = expr.strip()
        if not expr:
            continue

        try:
            res = eval_expr(expr)
            print(res)
        except Exception as e:
            print(e)


if __name__ == "__main__":
    main(sys.argv)
