# plt4115_project: Music Language

## Team Members: Celine Lee (cl4330) and Emma Li (eql2002)
### Google Doc of progress: https://docs.google.com/document/d/1IC8xrgoRSnulggQK8NDYVmRXlHIW1tGeOw0TDdbFREA/edit

### Context Free Grammar

S → ASN S | FNC S | LOOP S | ε

ASN → LHS = RHS

LHS → KW | KW ID

RHS → FNC | NM | KW | ID | [ BAR ]

BAR → [MN, MN, MN, MN], BAR | [MN, MN, MN, MN]

FNC → KW(ARG)

ARG → MN, ARG | NM, ARG | MN | NM | ε

LOOP → ‘repeat’ NM PN WS S


### Token Types:
Keywords (KW): variable types (TimeSig, Tempo, KeySig, Tune), built-in methods (time(), add(), minorThird(), minorFifth()), loops (repeat), TimeSig keywords (cmajor, gmajor)

Identifiers (ID): [ a-z ] [ a-z | A-Z | 0-9 ]* (at least one lowercase letter followed by any number of letters or digits)

Numbers (NM): integers

Punctuators (PN)

MusicNote (MN): [ C | D | E | F | G | A | B | r ] [ # | b | n ]? [ 0-9 ]? [ w | h | q | e | s ]

Whitespace (WS): tabs (\t)


### Grammar Rules:
KW → ‘TimeSig’ | ‘Tempo’ | ‘KeySig’ | ‘Tune’ | ‘time’ | ‘add’ | ‘minorThird’ | ‘minorFifth’ | ‘repeat’ | 

‘play’ | 'cmajor' | 'cminor' | 'dmajor' | 'dminor' | 'emajor' | 'eminor' | 'fmajor' | 'fminor' | 

'gmajor' | 'gminor' | 'amajor' | 'aminor' | 'bmajor' | 'bminor'

ID → [ a-z ] [ a-z | A-Z | 0-9 ]*

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
repeat 4:
<KW, repeat> <NM, 4> ‘:’
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
