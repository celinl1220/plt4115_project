import sys


def parse_ast_line(line):
    """
    Parse a single line of the AST to extract its type and value.
    """
    parts = line.strip().split(":")
    if len(parts) == 2:
        return parts[0].strip(), parts[1].strip()
    return parts[0].strip(), None


def generate_js(ast_lines):
    """
    Convert AST lines into JavaScript code using Tone.js and the provided general structure.
    """
    js_code = []
    js_code.append("// Generated JavaScript using Tone.js")
    js_code.append("import * as Tone from 'tone';\n")
    js_code.append("""
const durations_dict = {
    w: "1n",
    h: "2n",
    q: "4n",
    e: "8n",
    s: "16n"
};
""")

    time_signature = None
    tempo = None
    key_signature = None
    melody = []
    in_list = False
    current_bar = []

    for line in ast_lines:
        type_, value = parse_ast_line(line)

        if type_ == "LHS" and value == "TimeSig":
            time_signature = []  # Prepare to extract time signature
        elif type_ == "Argument" and time_signature is not None:
            time_signature.append(value)

        elif type_ == "LHS" and value == "Tempo":
            tempo = None  # Prepare to extract tempo
        elif type_ == "NM" and tempo is None:
            tempo = value

        elif type_ == "LHS" and value == "KeySig":
            key_signature = None  # Prepare to extract key signature
        elif type_ == "KW" and key_signature is None:
            key_signature = value

        elif type_ == "LHS" and value == "melody":
            melody = []  # Prepare to extract melody
        elif type_ == "List" and melody is not None:
            in_list = True
        elif type_ == "Bar" and in_list:
            current_bar = []  # Start a new bar
        elif type_ == "MN" and in_list:
            current_bar.append(value)
        elif type_ == "Bar" and current_bar:
            melody.append(current_bar)  # End of bar
            current_bar = []
        elif type_ == "List" and not current_bar:
            in_list = False

    # Generate JavaScript Code
    if time_signature:
        js_code.append(f"Tone.Transport.timeSignature = [{', '.join(time_signature)}];")
    if tempo:
        js_code.append(f"Tone.Transport.bpm.value = {tempo};")
    if key_signature:
        js_code.append(f'let original_ks = "{key_signature}";')
        js_code.append("let ks_key = original_ks.charAt(0).toUpperCase() + '4';")
        js_code.append("let ks_majmin = original_ks.slice(1);")
        js_code.append("const ks = Tonal.Scale.get(ks_key + ' ' + ks_majmin).notes;")

    if melody:
        js_code.append(f"let original_melody = {melody};")
        js_code.append("let melody = [];")
        js_code.append("let melody_durations = [];")
        js_code.append("""
for (var i = 0; i < original_melody.length; i++) {
    let original_melody_i = original_melody[i];
    let melody_i = [];
    let melody_durations_i = [];
    for (let j = 0; j < original_melody_i.length; j++) {
        let original_note = original_melody_i[j];
        let note = original_note.slice(0, -1); // Extract pitch
        let duration = original_note.slice(-1); // Extract duration
        if (!ks.includes(note)) {
            console.warn(`Note ${note} is not in the key signature ${original_ks}`);
        }
        melody_i.push(note);
        melody_durations_i.push(durations_dict[duration]);
    }
    melody.push(melody_i);
    melody_durations.push(melody_durations_i);
}
""")

    # Add play logic
    js_code.append("""
const synth = new Tone.Synth().toDestination();

async function playMelody() {
    await Tone.start();
    for (var i = 0; i < melody.length; i++) {
        var melody_i = melody[i];
        var melody_durations_i = melody_durations[i];
        for (var j = 0; j < melody_i.length; j++) {
            if (melody_i[j]) {
                synth.triggerAttackRelease(melody_i[j], melody_durations_i[j]);
            }
        }
    }
    Tone.Transport.start();
}

playMelody();
""")

    return "\n".join(js_code)


def main(ast_file):
    """
    Main function to process the AST file and generate JavaScript.
    """
    try:
        with open(ast_file, "r") as file:
            ast_lines = file.readlines()
    except Exception as e:
        print(f"Error reading AST file: {e}")
        sys.exit(1)

    js_code = generate_js(ast_lines)

    output_file = "output.js"
    try:
        with open(output_file, "w") as file:
            file.write(js_code)
        print(f"JavaScript code generated successfully as '{output_file}'.")
    except Exception as e:
        print(f"Error writing JavaScript file: {e}")
        sys.exit(1)


if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python3 codegen.py <ast_file>")
        sys.exit(1)

    main(sys.argv[1])
