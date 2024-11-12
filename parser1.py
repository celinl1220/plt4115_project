import re
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
        lhs = self.parse_LHS()
        if lhs and self.match(r'='):
            rhs = self.parse_RHS()
            if rhs:
                node = ASTNode("Assignment")
                node.add_child(lhs)
                node.add_child(rhs)
                return node
        return None
    
    def parse_LHS(self):
        # LHS → KW | KW ID
        if kw := self.parse_KW():
            lhs_node = ASTNode("LHS", kw[1])
            if id_node := self.parse_ID():
                lhs_node.add_child(ASTNode("ID", id_node[1]))
            return lhs_node
        return None
    
    def parse_RHS(self):
        # RHS → FNC | NM | KW | ID | [ BAR ]
        if fnc := self.parse_FNC():
            return fnc
        if nm := self.parse_NM():
            return ASTNode("NM", nm[1])
        if kw := self.parse_KW():
            return ASTNode("KW", kw[1])
        if id_node := self.parse_ID():
            return ASTNode("ID", id_node[1])
        if self.match(r'\['):
            list_node = ASTNode("List")
            while True:
                bar = self.parse_BAR()
                if bar:
                    list_node.add_child(bar)
                if not self.match(r','):
                    break
            if self.match(r'\]'):
                return list_node
        return None
    
    def parse_BAR(self):
        # BAR → [MN, MN, MN, MN], BAR | [MN, MN, MN, MN]
        if self.match(r'\['):
            bar_node = ASTNode("Bar")
            for _ in range(4):  # Expect exactly 4 music notes in a bar
                mn = self.parse_MN()
                if mn:
                    bar_node.add_child(ASTNode("MN", mn[1]))
                if not self.match(r',') and len(bar_node.children) < 4:
                    return None
            if self.match(r'\]'):
                return bar_node
        return None
    
    def parse_FNC(self):
        # FNC → KW ( ARG )
        if kw := self.parse_KW():
            fnc_node = ASTNode("FunctionCall", kw[1])
            if self.match(r'\('):
                arg_node = self.parse_ARG()
                if arg_node:
                    fnc_node.add_child(arg_node)
                if self.match(r'\)'):
                    return fnc_node
        return None
    
    def parse_ARG(self):
        # ARG → MN, ARG | NM, ARG | MN | NM | ε
        arg_node = ASTNode("Arguments")
        first_arg = self.parse_MN() or self.parse_NM()
        if first_arg:
            arg_node.add_child(ASTNode("Argument", first_arg[1]))
            while self.match(r','):
                next_arg = self.parse_MN() or self.parse_NM()
                if next_arg:
                    arg_node.add_child(ASTNode("Argument", next_arg[1]))
                else:
                    return None
            return arg_node
        return None
    
    def parse_LOOP(self):
        # LOOP → ‘repeat’ NM PN WS S
        if self.match(r'repeat'):
            loop_node = ASTNode("Loop", "repeat")
            if nm := self.parse_NM():
                loop_node.add_child(ASTNode("NM", nm[1]))
                return loop_node
        return None

    def parse_KW(self):
        return self.tokens[self.pos] if self.tokens[self.pos][0] == "KW" else None

    def parse_ID(self):
        return self.tokens[self.pos] if self.tokens[self.pos][0] == "ID" else None

    def parse_NM(self):
        return self.tokens[self.pos] if self.tokens[self.pos][0] == "NM" else None

    def parse_MN(self):
        return self.tokens[self.pos] if self.tokens[self.pos][0] == "MN" else None