class Number(int):
    def __new__(cls, value):
        return super().__new__(cls, value)

class Token:
    def __init__(self, kind, value=None):
        self.kind = kind
        self.value = value

    def __repr__(self):
        return f'Token {self.kind} {self.value}' if self.value else f'Token {self.kind}'

class TokenStream:
    def __init__(self, expr):
        self.input = list(expr)
        self.token = None

    # get a character from the input
    def __getch(self)->str:
        while self.input:
            ch = self.input.pop(0)
            if not ch.isspace():
                return ch
        return ''

    # put character back
    def __putch(self,ch: str):
        self.input.insert(0, ch)

    def getnum(self,ch)->Number:
        numstr = ''
        while ch.isdigit():
            numstr += ch
            ch = self.__getch()
        self.__putch(ch)
        return Number(numstr)

    def get(self)->Token:
        if self.token:
            token = self.token
            self.token = None
            return token
        ch = self.__getch()
        if ch in '()+-*/':
            return Token(ch)
        elif ch.isdigit():
            return Token('Number', self.getnum(ch))
        elif ch == '':
            return Token('End')
        else:
            raise ValueError(f'bad token {ch}')

    def put(self, token: Token):
        self.token = token

# factor : number | '(' expression ')'
def factor(ts: TokenStream)->Number:
    token = ts.get()
    if token.kind == '(':
        d = expression(ts)
        token = ts.get()
        if token.kind != ')':
            raise ValueError("')' expected")
        return d
    elif token.kind == 'Number':
        return token.value
    else:
        raise ValueError("factor expected")

# term : factor | term * factor | term / factor
def term(ts: TokenStream)->Number:
    left = factor(ts)
    token = ts.get()

    while True:
        if token.kind == '*':
            left *= factor(ts)
            token = ts.get()
        elif token.kind == '/':
            d = factor(ts)
            if d == 0:
                raise ValueError("divide by zero")
            left /= d
            token = ts.get()
        else:
            ts.put(token)
            return left

# expression : term | expression + term | expression - term
def expression(ts: TokenStream)->Number:
    left = term(ts)
    token = ts.get()

    while True:
        if token.kind == '+':
            left += term(ts)
            token = ts.get()
        elif token.kind == '-':
            left -= term(ts)
            token = ts.get()
        else:
            ts.put(token)
            return left

def calculate(expr: str)->Number:
    return expression(TokenStream(expr))

def main():
    try:
        expr = input('Enter expression: ')
        print(calculate(expr))
    except Exception as e:
        print(e)

if __name__ == "__main__":
    main()