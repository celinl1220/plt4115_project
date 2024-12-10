# plt4115_project: Music Language

## Team Members: Celine Lee (cl4330) and Emma Li (eql2002)

### Demo of lexer and parser: https://youtu.be/ve0fZTbzl-4
### Demo of code gen: https://youtu.be/8OKVa2ogRg8
### Google Doc of PA 1: https://docs.google.com/document/d/1IC8xrgoRSnulggQK8NDYVmRXlHIW1tGeOw0TDdbFREA/edit
### Google Doc of PA 2: [https://docs.google.com/document/d/1IC8xrgoRSnulggQK8NDYVmRXlHIW1tGeOw0TDdbFREA/edit](https://docs.google.com/document/d/1ZMe8Ih4Nr3aRxr5IcuGaK-74HFXwYsAZcHyCRY3h31w/edit?usp=sharing)
### Google Doc of PA 3: [https://docs.google.com/document/d/1IC8xrgoRSnulggQK8NDYVmRXlHIW1tGeOw0TDdbFREA/edit
](https://docs.google.com/document/d/1i4IBiJI4VnU23_-e0JkF2EkrfKXXYdSvCbE1JReYWas/edit?usp=sharing)

### Context Free Grammar

S → ASN S | FNC S | LOOP S | ε

ASN → LHS = RHS

LHS → KW | KW ID

RHS → FNC | NM | KW | ID | [ BAR ]

BAR → [MN, MN, MN, MN], BAR | [MN, MN, MN, MN]

FNC → KW(ARG)

ARG → MN ARG | NM ARG | ID ARG | ID | MN | NM | ε

LOOP → ‘loop’ NM PN WS S

### Token Types:
Keywords (KW): variable types (TimeSig, Tempo, KeySig, Tune), built-in methods (time(), add(), minorThird(), minorFifth()), loops (loop), TimeSig keywords (cmajor, gmajor)

Identifiers (ID): [ a-q s-z ] [ a-z | A-Z | 0-9 ]* (at least one lowercase letter followed by any number of letters or digits)

Numbers (NM): integers

Punctuators (PN)

MusicNote (MN): [ C | D | E | F | G | A | B | r ] [ # | b | n ]? [ 0-9 ]? [ w | h | q | e | s ]

Whitespace (WS): tabs (\t)


### Grammar Rules:

KW → ‘TimeSig’ | ‘Tempo’ | ‘KeySig’ | ‘Tune’ | ‘time’ | ‘add’ | ‘minorThird’ | ‘minorFifth’ | ‘play’ | 'cmajor' | 'cminor' | 'dmajor' | 'dminor' | 'emajor' | 'eminor' | 'fmajor' | 'fminor' | 'gmajor' | 'gminor' | 'amajor' | 'aminor' | 'bmajor' | 'bminor'

ID → [ a-q s-z ] [ a-z | A-Z | 0-9 ]*

NM → [ 0-9 ]+

PN → [ | ] | ( | ) | = | : 

MN → [ C | D | E | F | G | A | B | r ] [ # | b | n ]? [ 0-9 ]? [ w | h | q | e | s ]

WS → ‘\t’


### Example Programs and Outputs

Below are example programs and their corresponding token outputs as processed by the lexer:

```
(1) Creating a melody:
TimeSig ts = time(4, 4)
<KW, TimeSig> <ID, ts> ‘=’ <KW, time> ‘(‘ <NM, 4> ‘,’ <NM, 4> ‘)’
Tempo t = 144
<KW, Tempo> <ID, t> ‘=’ <NM, 144>
KeySig ks = cmajor
<KW, KeySig> <ID, ks> ‘=’ <KW, cmajor>
Tune melody = [[C4q, Cq, Gq, Gq], [Aq, Aq, Gh], [Fq, Fq, Eq, Eq], [Dq, Dq, Ch]]
<KW, Tune> <ID, melody> ‘=’ ‘[‘ ‘[‘ <MN, C4q> ‘,’ <MN, Cq> ‘,’ <MN, Gq> ‘,’ <MN, Gq> ‘]’ ‘,’ ‘[‘ <MN, Aq> ‘,’ <MN, Aq> ‘,’ <MN, Gh> ‘]’ ‘,’  ‘[‘ <MN, Fq> ‘,’ <MN, Fq> ‘,’ <MN, Eq> ‘,’ <MN, Eq> ‘]’ ‘,’ ‘[‘ <MN, Dq> ‘,’ <MN, Dq> ‘,’ <MN, Ch> ‘]’ ‘]’
play(melody, ts, ks, t)
<KW, play> ‘(‘ <ID, melody> ‘,’ <ID, ts> ‘,’ <ID, ks> ‘,’ <ID, t> ‘)’

(2) Call Function for Harmony
TimeSig ts = time(4, 4)
<KW, TimeSig> <ID, ts> ‘=’ <KW, time> ‘(‘ <NM, 4> ‘,’ <NM, 4> ‘)’
Tempo t = 144
<KW, Tempo> <ID, t> ‘=’ <NM, 144>
KeySig ks = cmajor
<KW, KeySig> <ID, ks> ‘=’ <KW, cmajor>
Tune melody = [[Aq, Aq, Gh]]
<KW, Tune> <ID, melody> ‘=’ ‘[‘ ‘[‘ <MN, Aq> ‘,’ <MN, Aq> ‘,’ <MN, Gh> ‘]’ ‘]’
Tune harmony = minorThird(melody)
<KW, Tune> <ID, harmony> ‘=’ <KW, minorThird> ‘(‘ <ID, melody> ‘)’
play([melody, harmony], ts, ks, t)
<KW, play> ‘(‘ ‘[‘ <ID, melody> <ID, harmony> ‘]’ ‘,’ <ID, ts> ‘,’ <ID, ks> ‘,’ <ID, t> ‘)’

(3) Loops
TimeSig ts = time(4, 4)
<KW, TimeSig> <ID, ts> ‘=’ <KW, time> ‘(‘ <NM, 4> ‘,’ <NM, 4> ‘)’
Tempo t = 144
<KW, Tempo> <ID, t> ‘=’ <NM, 144>
KeySig ks = cmajor
<KW, KeySig> <ID, ks> ‘=’ <KW, cmajor>
Tune melody = [[Aq, Aq, Gh]]
<KW, Tune> <ID, melody> ‘=’ ‘[‘ ‘[‘ <MN, Aq> ‘,’ <MN, Aq> ‘,’ <MN, Gh> ‘]’ ‘]’
Tune tune = [[Aq, rq, Bq, rq]]
<KW, Tune> <ID, tune> ‘=’ ‘[‘ ‘[‘ <MN, Aq> ‘,’ <MN, rq> ‘,’ <MN, Bq> ‘,’ <MN, rq> ‘]’ ‘]’
loop 4:
<KW, loop> <NM, 4> ‘:’
	melody.add(tune)
	<WS, ‘\t’> <ID, melody> ’.’ <KW, add> ‘(‘ <ID, tune> ‘)’

(4) ERROR: Missing parameter in built-in function
Tempo t = 144
<KW, Tempo> <ID, t> ‘=’ <NM, 144>
KeySig ks = cmajor
<KW, KeySig> <ID, ks> ‘=’ <KW, cmajor>
Tune melody = [[C4q, Cq, Gq, Gq]]
<KW, Tune> <ID, melody> ‘=’ ‘[‘ ‘[‘ <MN, C4q> ‘,’ <MN, Cq> ‘,’ <MN, Gq> ‘,’ <MN, Gq> ‘]’ ‘]’
play(melody, ks, t)
<KW, play> ‘(‘ <ID, melody> ‘,’ <ID, ks> ‘,’ <ID, t> ‘)’
ERROR: Missing TimeSig in play function

(5) Invalid note
Tune melody = [[C4q, 2q, Gq, Gq]]
<KW, Tune> <ID, melody> ‘=’ ‘[‘ ‘[‘ <MN, C4q> ‘,’ <MN, 2q> ‘,’ <MN, Gq> ‘,’ <MN, Gq> ‘]’ ‘]’
ERROR: Invalid MusicNote ‘2q’
```
Below are example programs and their corresponding token outputs as processed by the parser:
```
(1) Playing a Melody:
TimeSig ts = time(4, 4)
<KW, TimeSig> <ID, ts> ‘=’ <KW, time> ‘(‘ <NM, 4> ‘,’ <NM, 4> ‘)’
Tempo t = 144
<KW, Tempo> <ID, t> ‘=’ <NM, 144>
KeySig ks = cmajor
<KW, KeySig> <ID, ks> ‘=’ <KW, cmajor>
Tune melody = [[C4q, Cq, Gq, Gq]]
<KW, Tune> <ID, melody> ‘=’ ‘[‘ ‘[‘ <MN, C4q> ‘,’ <MN, Cq> ‘,’ <MN, Gq> ‘,’ <MN, Gq> ‘]’ ‘]’
play(melody, ts, ks, t)
<KW, play> ‘(‘ <ID, melody> ‘,’ <ID, ts> ‘,’ <ID, ks> ‘,’ <ID, t> ‘)’

Parsed AST:
Program
    Assignment
        LHS(TimeSig)
            ID(ts)
        FunctionCall(time)
            Argument(4)
            Argument(4)
    Assignment
        LHS(Tempo)
            ID(t)
        NM(144)
    Assignment
        LHS(KeySig)
            ID(ks)
        KW(cmajor)
    Assignment
        LHS(Tune)
            ID(melody)
        List
            Bar
                MN(C4q)
                MN(Cq)
                MN(Gq)
                MN(Gq)
    FunctionCall(play)
        Argument(melody)
        Argument(ts)
        Argument(ks)
        Argument(t)

(2) Call Function for Harmony
TimeSig ts = time(4, 4)
<KW, TimeSig> <ID, ts> ‘=’ <KW, time> ‘(‘ <NM, 4> ‘,’ <NM, 4> ‘)’
Tempo t = 144
<KW, Tempo> <ID, t> ‘=’ <NM, 144>
KeySig ks = cmajor
<KW, KeySig> <ID, ks> ‘=’ <KW, cmajor>
Tune melody = [[Aq, Aq, Gq, Gq]]
<KW, Tune> <ID, melody> ‘=’ ‘[‘ ‘[‘ <MN, Aq> ‘,’ <MN, Aq> ‘,’ <MN, Gq> ‘,’ <MN, Gq> ‘]’ ‘]’
Tune harmony = minorThird(melody)
<KW, Tune> <ID, harmony> ‘=’ <KW, minorThird> ‘(‘ <ID, melody> ‘)’
play(harmony, ts, ks, t)
<KW, play> ‘(‘ <ID, harmony> ‘,’ <ID, ts> ‘,’ <ID, ks> ‘,’ <ID, t> ‘)’

Program
    Assignment
        LHS(TimeSig)
            ID(ts)
        FunctionCall(time)
            Argument(4)
            Argument(4)
    Assignment
        LHS(Tempo)
            ID(t)
        NM(144)
    Assignment
        LHS(KeySig)
            ID(ks)
        KW(cmajor)
    Assignment
        LHS(Tune)
            ID(melody)
        List
            Bar
                MN(Aq)
                MN(Aq)
                MN(Gq)
                MN(Gq)
    Assignment
        LHS(Tune)
            ID(harmony)
        FunctionCall(minorThird)
            Argument(melody)
    FunctionCall(play)
        Argument(harmony)
        Argument(ts)
        Argument(ks)
        Argument(t)

(3) Loops
TimeSig ts = time(4, 4)
<KW, TimeSig> <ID, ts> ‘=’ <KW, time> ‘(‘ <NM, 4> ‘,’ <NM, 4> ‘)’
Tempo t = 144
<KW, Tempo> <ID, t> ‘=’ <NM, 144>
KeySig ks = cmajor
<KW, KeySig> <ID, ks> ‘=’ <KW, cmajor>
Tune melody = [[Aq, Aq, Gq, Gq]]
<KW, Tune> <ID, melody> ‘=’ ‘[‘ ‘[‘ <MN, Aq> ‘,’ <MN, Aq> ‘,’ <MN, Gq> ‘,’ <MN, Gq> ‘]’ ‘]’
Tune tune = [[Aq, rq, Bq, rq]]
<KW, Tune> <ID, tune> ‘=’ ‘[‘ ‘[‘ <MN, Aq> ‘,’ <MN, rq> ‘,’ <MN, Bq> ‘,’ <MN, rq> ‘]’ ‘]’
loop 4:
<KW, loop> <NM, 4> ‘:’
	add(melody, tune)
	<KW, add> ‘(‘ <ID, melody> ‘,’ <ID, tune> ‘)’

Program
    Assignment
            LHS(TimeSig)
                ID(ts)
        FunctionCall(time)
            Argument(4)
            Argument(4)
    Assignment
        LHS(Tempo)
            ID(t)
        NM(144)
    Assignment
        LHS(KeySig)
            ID(ks)
        KW(cmajor)
    Assignment
        LHS(Tune)
            ID(melody)
        List
            Bar
                MusicNote(Aq)
                MusicNote(Aq)
                MusicNote(Gq)
                MusicNote(Gq)
    Assignment
        LHS(Tune)
            ID(harmony)
        List
            Bar
                MusicNote(Aq)
                MusicNote(rq)
                MusicNote(Bq)
                MusicNote(rq)
    Loop(4)
        Program
            FunctionCall(add)
                Argument(melody)
                Argument(tune)

(4) Loops with Multiple Lines
Tempo t = 144
<KW, Tempo> <ID, t> ‘=’ <NM, 144>
KeySig ks = cmajor
<KW, KeySig> <ID, ks> ‘=’ <KW, cmajor>
Tune melody = [[C4q, Cq, Gq, Gq]]
<KW, Tune> <ID, melody> ‘=’ ‘[‘ ‘[‘ <MN, C4q> ‘,’ <MN, Cq> ‘,’ <MN, Gq> ‘,’ <MN, Gq> ‘]’ ‘]’
Tune tune1 = [[A4q, Aq, Gq, Gq]]
<KW, Tune> <ID, tune1> ‘=’ ‘[‘ ‘[‘ <MN, A4q> ‘,’ <MN, Aq> ‘,’ <MN, Gq> ‘,’ <MN, Gq> ‘]’ ‘]’
Tune tune2 = [[B4q, Bq, Gq, Gq]]
<KW, Tune> <ID, tune1> ‘=’ ‘[‘ ‘[‘ <MN, B4q> ‘,’ <MN, Bq> ‘,’ <MN, Gq> ‘,’ <MN, Gq> ‘]’ ‘]’
loop 2:
<KW, loop> <NM, 2> ‘:’
	add(melody, tune1)
	<KW, add> ‘(‘ <ID, melody> ‘,’ <ID, tune1> ‘)’
            add(melody, tune2)
	<KW, add> ‘(‘ <ID, melody> ‘,’ <ID, tune2> ‘)’

Program
    Assignment
        LHS(Tempo)
            ID(t)
        NM(144)
    Assignment
        LHS(KeySig)
            ID(ks)
        KW(cmajor)
    Assignment
        LHS(Tune)
            ID(melody)
        List
            Bar
                MN(C4q)
                MN(Cq)
                MN(Gq)
                MN(Gq)
    Assignment
        LHS(Tune)
            ID(tune1)
        List
            Bar
                MN(A4q)
                MN(Aq)
                MN(Gq)
                MN(Gq)
    Assignment
        LHS(Tune)
            ID(tune2)
        List
            Bar
                MN(B4q)
                MN(Bq)
                MN(Gq)
                MN(Gq)
    Loop(2)
        Program
            FunctionCall(add)
                Argument(melody)
                Argument(tune1)
        Program
            FunctionCall(add)
                Argument(melody)
                Argument(tune2)

(5) Multiple Bars
Tune melody = [[C4q, 2q, Gq, Gq], [Aq, Aq, Gq, Gq], [Fq, Fq, Eq, Eq], [Dq, Dq, Cq, Cq]]
<KW, Tune> <ID, melody> ‘=’ ‘[‘ ‘[‘ <MN, C4q> ‘,’ <MN, 2q> ‘,’ <MN, Gq> ‘,’ <MN, Gq> ‘]’ ‘,’ ‘[‘ <MN, Aq> ‘,’ <MN, Aq> ‘,’ <MN, Gq> ‘,’ <MN, Gq> ‘]’ ‘,’  ‘[‘ <MN, Fq> ‘,’ <MN, Fq> ‘,’ <MN, Eq> ‘,’ <MN, Eq> ‘]’ ‘,’ ‘[‘ <MN, Dq> ‘,’ <MN, Dq> ‘,’ <MN, Cq> ‘,’ <MN, Cq> ‘]’ ‘]’

Program
    Assignment
        LHS(Tune)
            ID(melody)
        List
            Bar
                MN(C4q)
                MN(2q)
                MN(Gq)
                MN(Gq)
            Bar
                MN(Aq)
                MN(Aq)
                MN(Gq)
                MN(Gq)
            Bar
                MN(Fq)
                MN(Fq)
                MN(Eq)
                MN(Eq)
            Bar
                MN(Dq)
                MN(Dq)
                MN(Cq)
                MN(Cq)
```

Below are example programs and their corresponding code gen outputs as processed by the codegen.py:
(1) Playing a Melody:
TimeSig ts = time ( 4, 4 )
Tempo t = 144
KeySig ks = cmajor
Tune melody = [[C4q, Cq, Gq, Gq]]
play ( melody, ts, ks, t )

Javascript (tone):

Tone.Transport.timeSignature = [4, 4];
Tone.Transport.bpm.value = 144;
let original_ks = "cmajor";
let ks_key = original_ks.charAt(0).toUpperCase() + "4"; // "C4"
let ks_majmin = original_ks.slice(1); // "major"
const ks = Tonal.Scale.get(ks_key + " " + ks_majmin).notes;

let original_melody = [["C4q", "Cq", "Gq", "Gq"]];
let melody = [];
let melody_durations = [];
for (var i = 0; i < original_melody.length; i++) {
    let original_melody_i = original_melody[i];
    let melody_i = [];
    let melody_durations_i = [];
    for (let j = 0; j < original_melody_i.length; j++) {
        let original_note = original_melody_i[j];
        let note = original_note.slice(0,-1);
        if (note
        if (not note in ks) {
            
        }
        let duration = original_note.slice(-1);
        melody_i.push(note);
        melody_durations_i.push(durations_dict[duration]);
    }
    melody.push(melody_i);
    melody_durations.push(melody_durations_i);
}

for (var i = 0; i < melody.length; i++) {
    var melody_i = melody[i];
    var melody_durations_i = melody_durations[i];
    for (var j = 0; j < melody_i.length; j++) {
        synth.triggerAttackRelease(melody_i[j], melody_durations_i[j]+"n");
    }
}


(2) Call Function for Harmony
TimeSig ts = time ( 4, 4 )
Tempo t = 144
KeySig ks = cmajor
Tune melody = [[Aq, Aq, Gq, Gq]]
Tune harmony = minorThird ( melody )
play ( harmony, ts, ks, t )


// Import Tone.js (include this script tag in HTML or import it in your project)
// <script src="https://cdn.jsdelivr.net/npm/tone"></script>

// Define time signature
const timeSig = [4, 4]; // TimeSig ts = time(4, 4)

// Define tempo
const tempo = 144; // Tempo t = 144
Tone.Transport.bpm.value = tempo;

// Define key signature
const keySig = "C Major"; // KeySig ks = cmajor

// Define melody
const melody = [
  { note: "A4", duration: "4n" }, // Aq
  { note: "A4", duration: "4n" }, // Aq
  { note: "G4", duration: "4n" }, // Gq
  { note: "G4", duration: "4n" }, // Gq
];

// Generate harmony (minor third below melody)
function minorThird(melody) {
  return melody.map((note) => {
    if (note.note) {
      const transposed = Tone.Frequency(note.note).transpose(-3).toNote();
      return { note: transposed, duration: note.duration };
    }
    return note; // For rests or invalid notes
  });
}

// Create harmony
const harmony = minorThird(melody);

// Play function
async function play(harmony, timeSig, keySig, tempo) {
  // Create a synthesizer
  const synth = new Tone.Synth().toDestination();

  // Schedule harmony notes
  const now = Tone.now();
  harmony.forEach((note, index) => {
    if (note.note) {
      synth.triggerAttackRelease(note.note, note.duration, now + index * Tone.Time(note.duration).toSeconds());
    }
  });

  // Start the Transport
  Tone.Transport.start();
}

// Play the harmony
play(harmony, timeSig, keySig, tempo);



(3) Loops
TimeSig ts = time( 4, 4 )
Tempo t = 144
KeySig ks = cmajor
Tune melody = [[Aq, Aq, Gq, Gq]]
Tune tune = [[Aq, rq, Bq, rq]]
loop 4:
	add( melody, tune )

Program
    Assignment
            LHS(TimeSig)
                ID(ts)
        FunctionCall(time)
            Argument(4)
            Argument(4)
    Assignment
        LHS(Tempo)
            ID(t)
        NM(144)
    Assignment
        LHS(KeySig)
            ID(ks)
        KW(cmajor)
    Assignment
        LHS(Tune)
            ID(melody)
        List
            Bar
                MusicNote(Aq)
                MusicNote(Aq)
                MusicNote(Gq)
                MusicNote(Gq)
    Assignment
        LHS(Tune)
            ID(harmony)
        List
            Bar
                MusicNote(Aq)
                MusicNote(rq)
                MusicNote(Bq)
                MusicNote(rq)
    Loop(4)
        Program
            FunctionCall(add)
                Argument(melody)
                Argument(tune)


// Import Tone.js (include this script tag in HTML or import it in your project)
// <script src="https://cdn.jsdelivr.net/npm/tone"></script>

// Define time signature
const timeSig = [4, 4]; // TimeSig ts = time(4, 4)

// Define tempo
const tempo = 144; // Tempo t = 144
Tone.Transport.bpm.value = tempo;

// Define key signature
const keySig = "C Major"; // KeySig ks = cmajor

// Define melody
let melody = [
  { note: "A4", duration: "4n" }, // Aq
  { note: "A4", duration: "4n" }, // Aq
  { note: "G4", duration: "4n" }, // Gq
  { note: "G4", duration: "4n" }, // Gq
];

// Define tune
const tune = [
  { note: "A4", duration: "4n" }, // Aq
  { note: null, duration: "4n" }, // rq (rest)
  { note: "B4", duration: "4n" }, // Bq
  { note: null, duration: "4n" }, // rq (rest)
];

// Add function: Adds the notes of tune to melody
function add(melody, tune) {
  return melody.concat(tune); // Concatenate melody and tune
}

// Play function: Play a sequence of notes
async function play(melody) {
  // Create a synthesizer
  const synth = new Tone.Synth().toDestination();

  // Schedule melody notes
  const now = Tone.now();
  melody.forEach((note, index) => {
    if (note.note) {
      synth.triggerAttackRelease(note.note, note.duration, now + index * Tone.Time(note.duration).toSeconds());
    }
  });

  // Start the Transport (optional if using sequences or Parts)
  Tone.Transport.start();
}

// Loop logic: Perform the add operation 4 times
for (let i = 0; i < 4; i++) {
  melody = add(melody, tune); // Add tune to melody
}

// Play the resulting melody
play(melody);


(4) Loops with Multiple Lines
Tempo t = 144
KeySig ks = cmajor
Tune melody = [[C4q, Cq, Gq, Gq]]
Tune tune1 = [[A4q, Aq, Gq, Gq]]
Tune tune2 = [[B4q, Bq, Gq, Gq]]
loop 2:
	add( melody, tune1 )
            add( melody, tune2 )

Program
    Assignment
        LHS(Tempo)
            ID(t)
        NM(144)
    Assignment
        LHS(KeySig)
            ID(ks)
        KW(cmajor)
    Assignment
        LHS(Tune)
            ID(melody)
        List
            Bar
                MN(C4q)
                MN(Cq)
                MN(Gq)
                MN(Gq)
    Assignment
        LHS(Tune)
            ID(tune1)
        List
            Bar
                MN(A4q)
                MN(Aq)
                MN(Gq)
                MN(Gq)
    Assignment
        LHS(Tune)
            ID(tune2)
        List
            Bar
                MN(B4q)
                MN(Bq)
                MN(Gq)
                MN(Gq)
    Loop(2)
        Program
            FunctionCall(add)
                Argument(melody)
                Argument(tune1)
        Program
            FunctionCall(add)
                Argument(melody)
                Argument(tune2)


// Import Tone.js (include this script tag in HTML or import it in your project)
// <script src="https://cdn.jsdelivr.net/npm/tone"></script>

// Define tempo
const tempo = 144; // Tempo t = 144
Tone.Transport.bpm.value = tempo;

// Define key signature
const keySig = "C Major"; // KeySig ks = cmajor

// Define melody
let melody = [
  { note: "C4", duration: "4n" }, // C4q
  { note: "C4", duration: "4n" }, // Cq
  { note: "G4", duration: "4n" }, // Gq
  { note: "G4", duration: "4n" }, // Gq
];

// Define tune1
const tune1 = [
  { note: "A4", duration: "4n" }, // A4q
  { note: "A4", duration: "4n" }, // Aq
  { note: "G4", duration: "4n" }, // Gq
  { note: "G4", duration: "4n" }, // Gq
];

// Define tune2
const tune2 = [
  { note: "B4", duration: "4n" }, // B4q
  { note: "B4", duration: "4n" }, // Bq
  { note: "G4", duration: "4n" }, // Gq
  { note: "G4", duration: "4n" }, // Gq
];

// Add function: Appends the notes of tune to melody
function add(melody, tune) {
  return melody.concat(tune);
}

// Play function: Plays a sequence of notes
async function play(melody) {
  // Create a synthesizer
  const synth = new Tone.Synth().toDestination();

  // Schedule melody notes
  const now = Tone.now();
  melody.forEach((note, index) => {
    if (note.note) {
      synth.triggerAttackRelease(note.note, note.duration, now + index * Tone.Time(note.duration).toSeconds());
    }
  });

  // Start the Transport
  Tone.Transport.start();
}

// Loop logic: Perform the add operations 2 times
for (let i = 0; i < 2; i++) {
  melody = add(melody, tune1); // Add tune1 to melody
  melody = add(melody, tune2); // Add tune2 to melody
}

// Play the resulting melody
play(melody);




(5) Multiple Bars
Tune melody = [[C4q, 2q, Gq, Gq], [Aq, Aq, Gq, Gq], [Fq, Fq, Eq, Eq], [Dq, Dq, Cq, Cq]]


// Import Tone.js (include this script tag in HTML or import it in your project)
// <script src="https://cdn.jsdelivr.net/npm/tone"></script>

// Define melody as multiple bars
const melody = [
  // Bar 1
  [
    { note: "C4", duration: "4n" }, // C4q
    { note: null, duration: "4n" }, // 2q (rest)
    { note: "G4", duration: "4n" }, // Gq
    { note: "G4", duration: "4n" }, // Gq
  ],
  // Bar 2
  [
    { note: "A4", duration: "4n" }, // Aq
    { note: "A4", duration: "4n" }, // Aq
    { note: "G4", duration: "4n" }, // Gq
    { note: "G4", duration: "4n" }, // Gq
  ],
  // Bar 3
  [
    { note: "F4", duration: "4n" }, // Fq
    { note: "F4", duration: "4n" }, // Fq
    { note: "E4", duration: "4n" }, // Eq
    { note: "E4", duration: "4n" }, // Eq
  ],
  // Bar 4
  [
    { note: "D4", duration: "4n" }, // Dq
    { note: "D4", duration: "4n" }, // Dq
    { note: "C4", duration: "4n" }, // Cq
    { note: "C4", duration: "4n" }, // Cq
  ],
];

// Play function: Plays a sequence of bars
async function playBars(melody) {
  // Create a synthesizer
  const synth = new Tone.Synth().toDestination();

  // Schedule melody bars
  let time = Tone.now(); // Start time
  melody.forEach((bar) => {
    bar.forEach((note) => {
      if (note.note) {
        synth.triggerAttackRelease(note.note, note.duration, time);
      }
      time += Tone.Time(note.duration).toSeconds();
    });
  });

  // Start the Transport (optional if using sequences or Parts)
  Tone.Transport.start();
}

// Play the melody
playBars(melody);
