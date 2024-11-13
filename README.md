# plt4115_project: Music Language

## Team Members: Celine Lee (cl4330) and Emma Li (eql2002)

### Demo of lexer and parser: https://youtu.be/ve0fZTbzl-4
### Google Doc of progress: https://docs.google.com/document/d/1IC8xrgoRSnulggQK8NDYVmRXlHIW1tGeOw0TDdbFREA/edit

### Context Free Grammar

S → ASN S | FNC S | LOOP S | ε

ASN → LHS = RHS

LHS → KW | KW ID

RHS → FNC | NM | KW | ID | [ BAR ]

BAR → [MN, MN, MN, MN], BAR | [MN, MN, MN, MN]

FNC → KW(ARG)

ARG → MN, ARG | NM, ARG | MN | NM | ε

LOOP → ‘loop’ NM PN WS S


### Token Types:
Keywords (KW): variable types (TimeSig, Tempo, KeySig, Tune), built-in methods (time(), add(), minorThird(), minorFifth()), loops (loop), TimeSig keywords (cmajor, gmajor)

Identifiers (ID): [ a-q s-z ] [ a-z | A-Z | 0-9 ]* (at least one lowercase letter followed by any number of letters or digits)

Numbers (NM): integers

Punctuators (PN)

MusicNote (MN): [ C | D | E | F | G | A | B | r ] [ # | b | n ]? [ 0-9 ]? [ w | h | q | e | s ]

Whitespace (WS): tabs (\t)


### Grammar Rules:
KW → ‘TimeSig’ | ‘Tempo’ | ‘KeySig’ | ‘Tune’ | ‘time’ | ‘add’ | ‘minorThird’ | ‘minorFifth’ | ‘loop’ | 

‘play’ | 'cmajor' | 'cminor' | 'dmajor' | 'dminor' | 'emajor' | 'eminor' | 'fmajor' | 'fminor' | 

'gmajor' | 'gminor' | 'amajor' | 'aminor' | 'bmajor' | 'bminor'

ID → [ a-q s-z ] [ a-z | A-Z | 0-9 ]*

NM → [ 0-9 ]+

PN → [ | ] | ( | ) | = | : | 

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
