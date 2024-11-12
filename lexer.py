import sys

def is_letter(char): 
    return char.isalpha()

def is_digit(char): 
    return char.isdigit() 

def is_punctuator(char): 
    return char in ["=", "(", ")", "[", "]", "|", ":", ",", ";"] 

def is_whitespace(char): 
    return char in [' ', '\t', '\n']

def is_music_note_start(char):
	return char in ['C', 'D', 'E', 'F', 'G', 'A', 'B', 'r']

def is_keyword(char):
	return char in ['TimeSig', 'Tempo', 'KeySig', 'Tune', 'time', 'add', 'minorThird', 'minorFifth', 'repeat', 'play', 'cmajor', 'cminor', 'dmajor', 'dminor', 'emajor', 'eminor', 'fmajor', 'fminor', 'gmajor', 'gminor', 'amajor', 'aminor', 'bmajor', 'bminor']

def is_music_note_accidental(char):
    return char in ['#', 'b', 'n']

def is_music_note_duration(char):
    return char in ['w', 'h', 'q', 'e', 's']

class LexicalError(Exception):
    pass

def scan(input_program):
    tokens = []  # List of tokens to output (token_type, token_value)
    current_state = "START"  # Keeps track of the most recent state
    token_value = ""  # Token value to add to token list

    for char in input_program:
        if current_state == "START":  # If at START state (starting new token)
            if is_music_note_start(char):
                token_value += char
                current_state = "MUSIC_NOTE"
            elif is_letter(char):  # If char is a letter
                token_value += char  # Add char to token value
                current_state = "ID_OR_KEYWORD"  # Update current state to ID_OR_KEYWORD
            elif is_digit(char):  # If char is a number
                token_value += char  # Add char to token value
                current_state = "NUMBER"  # Update current state to NUMBER
            elif is_punctuator(char):  # If char is a punctuator
                tokens.append(("PN", char))  # Append char to token list as PN
            elif char == '\t': # If char is a tab character 
                tokens.append(("TAB", "\\t"))
            elif char in [' ', '\n']:
                continue
            else:
                raise LexicalError(f"Unrecognized character: {char}")

        elif current_state == "ID_OR_KEYWORD":  # If current state is ID_OR_KEYWORD
            if is_letter(char) or is_digit(char):  # If char is letter or number
                token_value += char  # Add char to token value
            else:  # Else (id or keyword value is followed by non-letter/number -- whitespace, punctuation, unknown symbol)
                if is_keyword(token_value):  # If token value is a keyword
                    tokens.append(("KW", token_value))  # Append token value to token list as KW
                else:  # If token value is not a keyword
                    tokens.append(("ID", token_value))  # Append token value to token list as ID
                token_value = ""  # Reset token value and current state
                current_state = "START"

        elif current_state == "NUMBER":  # If current state is NUMBER
            if is_digit(char):  # If char is a number
                token_value += char  # Add char to token value
            else:  # If char is not a number
                tokens.append(("NM", token_value))  # Append token value to token list as NM
                token_value = ""  # Reset token value and current state
                current_state = "START"

        elif "MUSIC_NOTE" in current_state:  # If current state has substring MUSIC_NOTE
            if current_state == "MUSIC_NOTE" and is_music_note_accidental(char):  # If only first letter of music note and char is an accidental
                token_value += char  # Add char to token value
                current_state = "MUSIC_NOTE_ACC"  # Update current state to MUSIC_NOTE_ACC (music note with accidental)
            elif (current_state == "MUSIC_NOTE" or current_state == "MUSIC_NOTE_ACC") and is_digit(char):  # If current state is either MUSIC_NOTE or MUSIC_NOTE_ACC and char is a number
                token_value += char  # Add char to token value
                current_state = "MUSIC_NOTE_OCT"
            elif is_music_note_duration(char):  # If char is a music note duration
                token_value += char  # Add char to token value
                tokens.append(("MN", token_value))  # Append token value to token list as MN
                token_value = ""  # Reset token value and current state
                current_state = "START"
            else:
                raise LexicalError(f"Invalid MusicNote: {token_value}")
        elif current_state == "WHITESPACE":
            if is_whitespace(char):
                token_value += char
            else:
                tokens.append(("WS", token_value)) # Append token value to token list as WS

    # After loop ends, process any remaining token value
    if token_value:
        if current_state == "ID_OR_KEYWORD":
            if is_keyword(token_value):
                tokens.append(("KW", token_value))
            else:
                tokens.append(("ID", token_value))
        elif current_state == "NUMBER":
            tokens.append(("NM", token_value))
        elif current_state == "MUSIC_NOTE":
            tokens.append(("MN", token_value))

    return tokens

def main(program_file):
    # Read the input program from the specified file
    with open(program_file, 'r') as f:
        program_text = f.read()

    # Tokenize the program
    tokens = scan(program_text)

    # Print tokens to stdout in a format that can be read by the parser
    print(tokens)

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: ./lexer.py <program_file>")
        sys.exit(1)
    
    main(sys.argv[1])