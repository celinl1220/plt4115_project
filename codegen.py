import sys
import json

def convert_notes(original_notes, key_signature):
    """
    Convert notes from the original format to the desired format, ensuring they follow the key signature.

    Args:
        original_notes (list of str): List of notes in the format MN → [C|D|E|F|G|A|B|r][#|b|n]?[0-9]?
        key_signature (list of str): Key signature as an array of notes, e.g., ["C#", "D", "E", "F#", "G", "A", "B"]

    Returns:
        list of str: Converted notes in the format [C|D|E|F|G|A|B|r][#|b]?[0-9]
    """
    converted_notes = []
    default_octave = 4  # Default octave when not specified

    for note in original_notes:
        # Replace rests with null value
        if note == "r":
            converted_notes.append(None)
            continue

        # Extract the pitch, accidental, and octave using regex
        import re
        match = re.match(r"([A-Gr])([#b]?)?([0-9]?)", note)
        if not match:
            raise ValueError(f"Invalid note format: {note}")

        pitch, accidental, octave = match.groups()

        # Set default octave if none is provided
        if not octave:
            octave = str(default_octave)

        # Adjust the note to match the key signature
        target_note = pitch + accidental
        for ks_note in key_signature:
            if ks_note.startswith(pitch):
                target_note = ks_note
                break

        # Construct the final note
        final_note = target_note + octave
        converted_notes.append(final_note)

    return converted_notes

def keysig(ast):
    converted_ks = ast["value"];
    ks_key = converted_ks[0].upper();
    ks_majmin = converted_ks[1:];
    ks_arg = ks_key + " " + ks_majmin
    # print(ks_arg)
    return ks_arg

def ast_to_js(ast):
    if ast["type"] == "Program":
        # Convert the program to JavaScript
        js_code = []
        for child in ast["children"]:
            js_code.extend(ast_to_js(child))
        return js_code
    elif ast["type"] == "Assignment":
        js_code = []
        lhs = ast["children"][0];
        if lhs["value"] == "TimeSig":
            js_code = [f"Tone.Transport.timeSignature = %s;\n"];
        elif lhs["value"] == "Tempo":
            js_code = [f"Tone.Transport.bpm.value = %s;\n"];
        elif lhs["value"] == "KeySig":
            ks_id = lhs["children"][0]["value"]
            ks_arg = keysig(ast["children"][1])
            print(ks_id, ks_arg)
            js_code = [f"""const {ks_id} = Tonal.Scale.get({ks_arg}).notes;"""];
            print(js_code)
            return js_code
        if ast["children"][1]["type"] == "FunctionCall":
            # Function call assignment
            function_name = ast["children"][1]["value"]
            if (function_name == "time"):
                first_arg = ast["children"][1]["children"][0]
                second_arg = ast["children"][1]["children"][1]
                args = [first_arg["children"][0]["value"], second_arg["children"][0]["value"]]
                js_code[-1] = js_code[-1]%(f"[{args[0]}, {args[1]}]")
            elif function_name == "minorThird":
                args = [first_arg["children"][0]["value"]]
                js_code[-1] = js_code[-1]%(f"[{args[0]}]")
        elif ast["children"][1]["type"] == "NM":
            # Numeric value assignment
            js_code[-1] = js_code[-1]%(f"{ast['children'][1]['value']}")
        elif ast["children"][1]["type"] == "KW":
            # Keyword value assignment (like key signature)
            js_code[-1] = js_code[-1]%(f"{ast['children'][1]['value']}")
        print(js_code)
        return js_code
    # elif ast["type"] == "List":
    #     # List of bars (melody)
    #     melody_js = []
    #     for bar in ast["children"]:
    #         melody_js.extend(ast_to_js(bar))
    #     return melody_js
    # elif ast["type"] == "Bar":
    #     # Individual bar
    #     bar_js = []
    #     for mn in ast["children"]:
    #         bar_js.append(f"Tone.MusicNote('{mn['value']}');")
    #     return bar_js
    elif ast["type"] == "FunctionCall":
        # Play function call
        js_code = []
        function_name = ast["value"]
        if function_name == "add":
            first_arg = ast["children"][1]["children"][0]
            second_arg = ast["children"][1]["children"][1]
            args = [first_arg["children"][0]["value"], second_arg["children"][0]["value"]]
            js_code.append(f"{args[0]} += {args[1]};\n")
        return js_code

def main(ast_file):
    with open(ast_file, 'r') as f:
        ast = json.load(f)

    # Convert AST to JavaScript
    js_code = ast_to_js(ast)

    # Print JavaScript code
    for line in js_code:
        print(line)

    with open("output.js", 'w') as f:
        f.write(js_code)

    print("JavaScript code generated successfully.")

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: ./ast_converter.py <ast_file>")
        sys.exit(1)

    main(sys.argv[1])