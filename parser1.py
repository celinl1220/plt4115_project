import re
import sys
from lexer import scan

class ASTNode:
    def __init__(self, type, value=None):
        self.type = type
        self.value = value
        self.children = []

    def add_child(self, node):
        self.children.append(node)

    def __repr__(self, level=0):
        ret = "\t" * level + f"{self.type}: {self.value}\n"
        for child in self.children:
            ret += child.__repr__(level + 1)
        return ret
    
class Parser:
    def __init__(self, tokens): # input tokens is from Lexer
        self.tokens = tokens # list of tokens
        self.pos = 0 # current position
    
    def parse(self):
        root = self.parse_S()
        return root if self.pos == len(self.tokens) else None
    
    def match(self, pattern):
        if self.pos < len(self.tokens) and re.fullmatch(pattern, self.tokens[self.pos][1]):
            matched = self.tokens[self.pos]
            self.pos += 1
            return matched
        return None
    
    def parse_S(self):
	 # S → ASN S | FNC S | LOOP S | ε
        program_node = ASTNode("Program")
        while self.pos < len(self.tokens):
            statement = self.parse_ASN() or self.parse_FNC() or self.parse_LOOP()
            if statement:
                program_node.add_child(statement)
            else:
                break
        return program_node
    
    def parse_ASN(self):
        # ASN → LHS = RHS
        temp_pos = self.pos
        lhs = self.parse_LHS()
        if lhs and self.match(r'='):
            rhs = self.parse_RHS()
            if rhs:
                node = ASTNode("Assignment")
                node.add_child(lhs)
                node.add_child(rhs)
                return node
        self.pos = temp_pos
        return None
    
    def parse_LHS(self):
        # LHS → KW | KW ID
        if kw := self.parse_KW():
            lhs_node = ASTNode("LHS", kw[1])
            self.pos += 1
            if id_node := self.parse_ID():
                lhs_node.add_child(ASTNode("ID", id_node[1]))
                self.pos += 1
            return lhs_node
        return None
    
    def parse_RHS(self):
        # RHS → FNC | NM | KW | ID | [ BAR ]
        if fnc := self.parse_FNC():
            # self.pos += 1
            return fnc
        elif nm := self.parse_NM():
            self.pos += 1
            return ASTNode("NM", nm[1])
        elif kw := self.parse_KW():
            self.pos += 1
            return ASTNode("KW", kw[1])
        elif id_node := self.parse_ID():
            self.pos += 1
            return ASTNode("ID", id_node[1])
        elif self.match(r'\['):
            list_node = ASTNode("List")
            first_list = True
            while not self.match(r'\]'):
                bar = self.parse_BAR(first_list)
                if bar:
                    first_list = False
                    list_node.add_child(bar)
            return list_node
        return None
    
    def parse_BAR(self, first_list):
        # BAR → [MN, MN, MN, MN], BAR | [MN, MN, MN, MN]
        if first_list or (not first_list and self.match(r'\,')):
            if self.match(r'\['):
                bar_node = ASTNode("Bar")
                for i in range(4):  # Expect exactly 4 music notes in a bar
                    mn = self.parse_MN()
                    if mn:
                        bar_node.add_child(ASTNode("MN", mn[1]))
                        self.pos += 1
                    if not self.match(r',') and len(bar_node.children) < 4:
                        return None
                if self.match(r'\]'):
                    return bar_node
        return None
    
    def parse_FNC(self):
        # FNC → KW ( ARG )
        if kw := self.parse_KW():
            fnc_node = ASTNode("FunctionCall", kw[1])
            self.pos += 1
            if self.match(r'\('):
                while not self.match(r'\)'):
                    arg_node = self.parse_ARG()
                    if arg_node:
                        fnc_node.add_child(arg_node)
                        self.pos += 1
                return fnc_node
            else:
                self.pos -= 1
        return None
    
    def parse_ARG(self):
        # ARG → MN, ARG | NM, ARG | ID , ARG | MN | NM | ID | ε
        arg_node = ASTNode("Arguments")
        arg = self.parse_MN() or self.parse_NM() or self.parse_ID()
        if arg:
            arg_node.add_child(ASTNode("Argument", arg[1]))
            return arg_node
        return None
    
    def parse_LOOP(self):
        # LOOP → ‘repeat’ NM PN WS S
        if self.match(r'loop'):
            nm = self.parse_NM()
            if nm is not None:
                loop_node = ASTNode("Loop", nm[1])
                self.pos += 1
                # print(self.tokens[self.pos])
                while self.pos < len(self.tokens) and self.tokens[self.pos][0] == "TAB":
                    self.pos += 1
                    statement = self.parse_ASN() or self.parse_FNC() or self.parse_LOOP()
                    if statement:
                        loop_node.add_child(statement)
                    else:
                        break
                return loop_node
        return None

    def parse_KW(self):
        if self.tokens[self.pos][0] == "KW":
            toReturn = self.tokens[self.pos]
            return toReturn
        return None

    def parse_ID(self):
        if self.tokens[self.pos][0] == "ID":
            toReturn = self.tokens[self.pos]
            return toReturn
        return None

    def parse_NM(self):
        if self.tokens[self.pos][0] == "NM":
            toReturn = self.tokens[self.pos]
            return toReturn
        return None

    def parse_MN(self):
        if self.tokens[self.pos][0] == "MN":
            toReturn = self.tokens[self.pos]
            return toReturn
        return None
    

def main(token_file):
    with open(token_file, 'r') as f:
        tokens = eval(f.read())

    # Initialize the parser with tokens and parse
    parser = Parser(tokens)
    ast = parser.parse()

    # Print the AST if parsing was successful, or an error if not
    if ast:
        print(ast)
    else:
        print("Parsing failed due to syntax errors.")

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: ./parser.py <tokens_file>")
        sys.exit(1)
    
    main(sys.argv[1])