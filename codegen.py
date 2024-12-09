import re
import sys
from lexer import scan

class CodeGen:
    def __init__(self, ast):
        self.ast = ast
        self.temp_counter = 0
        self.instructions = []
    
    def generate(self):
        self.instructions = []
        self.traverse_ast(self.ast)
        return "\n".join(self.instructions)

    def traverse_ast(self, node):
        if node is None:
            return
        
        if node.type == "Program":
            for child in node.children:
                self.traverse_ast(child)
        
        elif node.type == "Assignment":
            lhs_reg = self.generate_mips_for(lhs=node.children[0])
            rhs_reg = self.generate_mips_for(rhs=node.children[1])
            self.instructions.append(f"sw {rhs_reg}, 0({lhs_reg})")
        
        elif node.type == "LHS":
            if node.value == "id":
                return f"t{self.get_temp_reg()}"
            else:
                return f"${node.value}"
        
        elif node.type == "RHS":
            if node.value == "id":
                return f"${node.value}"
            elif node.type == "NM":
                return f"li ${self.get_temp_reg()}, {node.value}"
            elif node.type == "KW":
                return f"${node.value}"
            elif node.type == "List":
                bar_address = self.handle_list(node)
                return f"{bar_address}"
        
        elif node.type == "FunctionCall":
            function_name = node.value
            arg_regs = []
            for arg in node.children:
                arg_regs.append(self.generate_mips_for(rhs=arg))
            self.instructions.append(f"{function_name}({', '.join(arg_regs)})")
        
        elif node.type == "Arguments":
            arg_regs = []
            for arg in node.children:
                arg_regs.append(self.generate_mips_for(rhs=arg))
            return f"({', '.join(arg_regs)})"
        
        elif node.type == "Loop":
            loop_count = self.generate_mips_for(rhs=node.children[0])
            self.instructions.append(f"loop_start:")
            self.traverse_ast(node.children[1])
            self.instructions.append(f"bnez t0, loop_start")
        
        elif node.type == "Bar":
            bar_address = self.handle_list(node)
            return bar_address
        
        else:
            raise ValueError(f"Unknown AST node type: {node.type}")
    
    def generate_mips_for(self, lhs=None, rhs=None):
        if lhs:
            if lhs.type == "id":
                return f"t{self.get_temp_reg()}"
            elif lhs.type == "KW":
                return f"${lhs.value}"
        
        if rhs:
            if rhs.type == "NM": 
                return f"li ${self.get_temp_reg()}, {rhs.value}"
            elif rhs.type == "KW": 
                return f"${rhs.value}" 
            elif rhs.type == "ID": 
                return f"${rhs.value}"
    
    def get_temp_reg(self):
        self.temp_counter += 1
        return self.temp_counter
    
    def handle_list(self, node):
        base_address = self.get_temp_reg()
        self.instructions.append(f"la t{base_address}, list")
        for i, child in enumerate(node.children):
            mn_reg = self.generate_mips_for(rhs=child)
            self.instructions.append(f"sw {mn_reg}, {i * 4}(t{base_address})")
        return f"t{base_address}"

def main(ast_file):
    with open(ast_file, 'r') as f:
        ast = eval(f.read())

    codegen = CodeGen(ast)
    mips_code = codegen.generate()

    with open("output.mips", 'w') as f:
        f.write(mips_code)

    print("MIPS code generated successfully.")

if __name__ == "__main__":
    import sys

    if len(sys.argv) != 2:
        print("Usage: ./codegen.py <ast_file>")
        sys.exit(1)
    
    main(sys.argv[1])