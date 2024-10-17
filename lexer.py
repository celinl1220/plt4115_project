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
	return char in ['TimeSig', 'Tempo', 'KeySig', 'Tune', 'time', 'add', 'minorThird', 'minorFifth', 'repeat', 'play']

def is_music_note_accidental(char):
    return char in ['#', 'b', 'n']

def is_music_note_duration(char):
    return char in ['w', 'h', 'q', 'e', 's']

class LexicalError(Exception):
    pass

def scan(input_program):
    tokens = [] # list of tokens to output (token_type, token_value)
    current_state = "START" # keeps track of most recent state
    token_value = "" # token value to add to token list

    for char in input_program:
        if current_state == "START": # if at START state (starting new token)
            if is_letter(char): # if char is a letter
                token_value += char # add char to token value
                current_state = "ID_OR_KEYWORD" # update current state to ID_OR_KEYWORD
            elif is_digit(char): # if char is a number
                token_value += char # add char to token value
                current_state = "NUMBER" # update current state to NUMBER
            elif is_music_note_start(char):
                token_value += char
                current_state = "MUSIC_NOTE"
            elif is_punctuator(char): # if char is a punctuator
                tokens.append(("PN", char)) # append char to token list as PN
            elif is_whitespace(char): # if char is whitespace
                current_state = "WHITESPACE" # update current state to WHITESPACE (don't need to append to token list?)
            else:
                raise LexicalError(f"Unrecognized character: {char}")

        elif current_state == "ID_OR_KEYWORD": # if current state is ID_OR_KEYWORD
            if is_letter(char) or is_digit(char): # if char is letter or number
                token_value += char # add char to token value
            else: # else (id or keyword value is followed by non-letter/number -- whitespace, punctuation, unknown symbol)
                if is_keyword(token_value): # if token value is a keyword
                    tokens.append(("KW", token_value)) # append token value to token list as KW
                else: # if token value is not a keyword
                    tokens.append(("ID", token_value)) # append token value to token list as ID
                token_value = "" # reset token value and current state
                current_state = "START"

        elif current_state == "NUMBER": # if current state is NUMBER
            if is_digit(char): # if char is a number
                token_value += char # add char to token value
            else: # if char is not a number
                tokens.append(("NM", token_value)) # append token value to token list as NM
                token_value = "" # reset token value and current state
                current_state = "START"

        elif "MUSIC_NOTE" in current_state: # if current state has substring MUSIC_NOTE
            if current_state == "MUSIC_NOTE" and is_music_note_accidental(char): # if only first letter of music note and char is an accidental
                token_value += char # add char to token value
                current_state = "MUSIC_NOTE_ACC" # update current state to MUSIC_NOTE_ACC (music note with accidental)
            elif (current_state == "MUSIC_NOTE" or current_state == "MUSIC_NOTE_ACC") and is_digit(char): # if current state is either MUSIC_NOTE or MUSIC_NOTE_ACC and char is a number
                token_value += char # add char to token value
                current_state = "MUSIC_NOTE_OCT"
            elif is_music_note_duration(char): # if char is a music note duration
                token_value += char # add char to token value
                tokens.append(("MN", token_value)) # append token value to token list as MN
                token_value = "" # reset token value and current state
                current_state = "START"
            else:
                token_value += char
                raise LexicalError(f"Invalid MusicNote: {token_value}")
                
        elif current_state == "WHITESPACE": # if current state is WHITESPACE
            if not is_whitespace(char): # if char is not white space
                current_state = "START" # reset current state

    if token_value: # if input is fully scanned and there is remaining token value
        if current_state == "ID_OR_KEYWORD": # if current state is ID_OR_KEYWORD
            if is_keyword(token_value): # if token value is a keyword
                tokens.append(("KW", token_value)) # append token value to token list as KW
            else: # if token value is not a keyword
                tokens.append(("ID", token_value)) # append token value to token list as ID
        elif current_state == "NUMBER": # if current state is NUMBER
            tokens.append(("NM", token_value)) # append token value to token list as NM
        elif current_state == "MUSIC_NOTE": # if current state is MUSIC_NOTE
            tokens.append(("MN", token_value)) # append token value to token list as MN 

    return tokens