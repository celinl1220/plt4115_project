# plt4115_project: Music Language

## Team Members: Celine Lee (cl4330) and Emma Li (eql2002)

### Demo of lexer and parser: https://youtu.be/ve0fZTbzl-4
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
```
(1) Playing a Melody:
TimeSig ts = time(4, 4)
Tempo t = 144
KeySig ks = cmajor
Tune melody = [[C4q, Cq, Gq, Gq]]
play(melody, ts, ks, t)

main:
    move $fp $sp		# Set frame pointer to stack pointer
    sw $ra 0($sp)		# Save return address
    addiu $sp $sp -4		# Adjust stack pointer

    # Assignment: TimeSig ts = time(4, 4)
    li $t0 4			# Load second number 4 into $t0
    sw $t0 0($sp)		# Push numerator onto stack
    addiu $sp $sp -4		# Adjust stack pointer

    li $t0 4			# Load first number 4 into $t0
    sw $t0 0($sp)		# Push denominator onto stack
    addiu $sp $sp -4		# Adjust stack pointer

    jal time			# Call time function
    la $a0 ts			# Load address of ts
    sw $v0 0($a0)		# Store returned value from time(4,4) in ts

    # Assignment: Tempo t = 144
    li $t0 144			# Load number 144 into $t0
    la $a0 t			# Load address of t
    sw $t0 0($a0)		# Store tempo in t

    # Assignment: KeySig ks = cmajor
    la $a0 ks			# Load address of ks
    la $t0 "cmajor"		# Load address of the keyword "cmajor"
    sw $t0 0($a0)		# Store KeySig value in ks

    # Assignment: Tune melody = [[C4q, Cq, Gq, Gq]]
    lw $t0 “C4q”			# Load “C4q” into $t0
    sw $t0 0($sp)		# Push “C4q” onto stack
    addiu $sp $sp -4		# Adjust stack pointer
    jal get_musicnote		# Call get_musicnote function
    sw $a0 0($sp)		# Store the pointer to note in melody
    addiu $sp $sp -4		# Adjust stack pointer

    lw $t0 “Cq”			# Load “Cq” into $t0
    sw $t0 0($sp)		# Push “Cq” onto stack
    addiu $sp $sp -4		# Adjust stack pointer
    jal get_musicnote		# Call get_musicnote function
    sw $a0 0($sp)		# Store the pointer to note in melody
    addiu $sp $sp -4		# Adjust stack pointer

    lw $t0 “Gq”			# Load “Gq” into $t0
    sw $t0 0($sp)		# Push “Gq” onto stack
    addiu $sp $sp -4		# Adjust stack pointer
    jal get_musicnote		# Call get_musicnote function
    sw $a0 0($sp)		# Store the pointer to note in melody	
    addiu $sp $sp -4		# Adjust stack pointer

    lw $t0 “Gq”			# Load “Gq” into $t0
    sw $t0 0($sp)		# Push “Gq” onto stack
    addiu $sp $sp -4		# Adjust stack pointer
    jal get_musicnote		# Call get_musicnote function
    sw $a0 0($sp)		# Store the pointer to note in melody	
    addiu $sp $sp -4		# Adjust stack pointer

    la $t0 melody		# Load address of melody to $t0
    sw 

    # FunctionCall: play(melody, ts, ks, t)
    la $t0 melody		# Load melody address
    sw $t0 0($sp)		# Push melody onto stack
    addiu $sp $sp -4		# Adjust stack pointer

    la $t0 ts			# Load TimeSig address
    sw $t0 0($sp)		# Push ts onto stack
    addiu $sp $sp -4		# Adjust stack pointer

    la $t0 ks			# Load KeySig address
    sw $t0 0($sp)		# Push ks onto stack
    addiu $sp $sp -4		# Adjust stack pointer

    lw $t0 t			# Load Tempo value
    sw $t0 0($sp)		# Push t onto stack
    addiu $sp $sp -4		# Adjust stack pointer

    jal play			# Call play function

    lw $ra 4($sp)		# Restore return address
    addiu $sp $sp 4		# Adjust stack pointer
    lw $fp 0($sp)		# Reset frame pointer
    jr $ra			# Exit program

# Function: time
time:
    move $fp $sp		# Set frame pointer
    sw $ra 0($sp)		# Save return address
    addiu $sp $sp -4		# Adjust stack pointer

    # Load arguments from stack
    lw $a0 4($fp)		# Load first argument
    sw $a0 0($fp)		# Store first argument to stack
    addiu $sp $sp -4		# Adjust stack pointer

    lw $a1 8($fp)		# Load second argument
    sw $a0 0($fp)		# Store first argument to stack
    addiu $sp $sp -4		# Adjust stack pointer

    # Return language-specified notation of time signature (implementation omitted)

    lw $ra 4($sp)		# Restore return address
    addiu $sp $sp 16		# Adjust stack pointer
    lw $fp 0($sp)		# fp = old_fp
    jr $ra			# Return to caller

# Function: play
play:
    move $fp $sp		# Set frame pointer to current stack pointer
    sw $ra 0($sp)		# Save return address
    addiu $sp $sp -4		# Adjust stack pointer

    # Load arguments
    lw $a0 16($fp)		# Load melody (first argument)
    sw $a0 0($fp)		# Store first argument to stack
    addiu $sp $sp -4		# Adjust stack pointer

    lw $a0 12($fp)		# Load TimeSig (second argument)
    sw $a0 0($fp)		# Store first argument to stack
    addiu $sp $sp -4		# Adjust stack pointer

    lw $a0 8($fp)		# Load KeySig (third argument)
    sw $a0 0($fp)		# Store first argument to stack
    addiu $sp $sp -4		# Adjust stack pointer

    lw $a0 4($fp)		# Load Tempo (fourth argument)
    sw $a0 0($fp)		# Store first argument to stack
    addiu $sp $sp -4		# Adjust stack pointer

    # Simulate play logic (implementation omitted)

    lw $ra 4($sp)		# Restore return address
    addiu $sp $sp 24		# Flush out
    lw $fp 0($sp)		# fp = old_fp
    jr $ra			# Return to caller

# Function: get_musicnote
get_musicnote:
    move $fp $sp		# Set frame pointer to current stack pointer
    sw $ra 0($sp)		# Save return address
    addiu $sp $sp -4		# Adjust stack pointer

    # Load argument
    lw $a0 4($fp)		# Load argument
    sw $a0 0($fp)		# Store argument to stack
    addiu $sp $sp -4		# Adjust stack pointer

    # Simulate logic to get music note address and store in $a0 (implementation omitted)

    lw $ra 4($sp)		# Restore return address
    addiu $sp $sp 12		# Flush out
    lw $fp 0($sp)		# fp = old_fp
    jr $ra			# Return to caller


(2) Call Function for Harmony
TimeSig ts = time(4, 4)
Tempo t = 144
KeySig ks = cmajor
Tune melody = [[Aq, Aq, Gq, Gq]]
Tune harmony = minorThird(melody)
play(harmony, ts, ks, t)

main:
    move $fp, $sp		# Set frame pointer to stack pointer
    sw $ra, 0($sp)		# Save return address
    addiu $sp, $sp, -4		# Adjust stack pointer

    # Assignment: TimeSig ts = time(4, 4)
    li $t0, 4			# Load first number 4 into $t0
    sw $t0, 0($sp)		# Push numerator onto stack
    addiu $sp, $sp, -4		# Adjust stack pointer

    li $t0, 4			# Load second number 4 into $t0
    sw $t0, 0($sp)		# Push denominator onto stack
    addiu $sp, $sp, -4		# Adjust stack pointer

    jal time			# Call time function
    la $a0, ts			# Load address of ts
    sw $v0, 0($a0)		# Store returned value in ts

    # Assignment: Tempo t = 144
    li $t0, 144			# Load number 144 into $t0
    la $a0, t			# Load address of t
    sw $t0, 0($a0)		# Store tempo in t

    # Assignment: KeySig ks = cmajor
    la $a0, ks			# Load address of ks
    la $t0, "cmajor"		# Load address of the keyword "cmajor"
    sw $t0, 0($a0)		# Store KeySig value in ks

    # Assignment: Tune melody = [[Aq, Aq, Gq, Gq]]
    la $a0, melody		# Load address of melody
    li $t0, 0xA			# Aq
    sw $t0, 0($a0)
    sw $t0, 4($a0)
    li $t0, 0xG            # Gq
    sw $t0, 8($a0)
    sw $t0, 12($a0)

    # Assignment: Tune harmony = minorThird(melody)
    la $t0, melody         # Load melody address
    sw $t0, 0($sp)         # Push melody onto stack
    addiu $sp, $sp, -4     # Adjust stack pointer

    jal minorThird         # Call minorThird function
    la $a0, harmony        # Load address of harmony
    sw $v0, 0($a0)         # Store returned value in harmony

    # FunctionCall: play(harmony, ts, ks, t)
    la $t0, harmony        # Load harmony address
    sw $t0, 0($sp)         # Push harmony onto stack
    addiu $sp, $sp, -4     # Adjust stack pointer

    la $t0, ts             # Load TimeSig address
    sw $t0, 0($sp)         # Push ts onto stack
    addiu $sp, $sp, -4     # Adjust stack pointer

    la $t0, ks             # Load KeySig address
    sw $t0, 0($

(3) Loops
TimeSig ts = time(4, 4)
Tempo t = 144
KeySig ks = cmajor
Tune melody = [[Aq, Aq, Gq, Gq]]
Tune tune = [[Aq, rq, Bq, rq]]
loop 4:
	add(melody, tune)

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

.data
ts: .word 0             # TimeSig variable
t: .word 0              # Tempo variable
ks: .asciiz "cmajor"    # KeySig variable
melody: .space 16       # Memory for melody notes (4 notes)
tune: .space 16         # Memory for tune notes (4 notes)

.text
main:
    # Prologue
    move $fp, $sp          # Set frame pointer to stack pointer
    sw $ra, 0($sp)         # Save return address
    addiu $sp, $sp, -4     # Adjust stack pointer

    # Assignment: TimeSig ts = time(4, 4)
    li $t0, 4              # Load first number 4 into $t0
    sw $t0, 0($sp)         # Push numerator onto stack
    addiu $sp, $sp, -4     # Adjust stack pointer

    li $t0, 4              # Load second number 4 into $t0
    sw $t0, 0($sp)         # Push denominator onto stack
    addiu $sp, $sp, -4     # Adjust stack pointer

    jal time               # Call time function
    la $a0, ts             # Load address of ts
    sw $v0, 0($a0)         # Store returned value in ts

    # Assignment: Tempo t = 144
    li $t0, 144            # Load number 144 into $t0
    la $a0, t              # Load address of t
    sw $t0, 0($a0)         # Store tempo in t

    # Assignment: KeySig ks = cmajor
    la $a0, ks             # Load address of ks
    la $t0, "cmajor"       # Load address of the keyword "cmajor"
    sw $t0, 0($a0)         # Store KeySig value in ks

    # Assignment: Tune melody = [[Aq, Aq, Gq, Gq]]
    la $a0, melody         # Load address of melody
    li $t0, 0xA            # Aq
    sw $t0, 0($a0)
    sw $t0, 4($a0)
    li $t0, 0xG            # Gq
    sw $t0, 8($a0)
    sw $t0, 12($a0)

    # Assignment: Tune tune = [[Aq, rq, Bq, rq]]
    la $a0, tune           # Load address of tune
    li $t0, 0xA            # Aq
    sw $t0, 0($a0)
    li $t0, 0x0            # rq (rest)
    sw $t0, 4($a0)
    li $t0, 0xB            # Bq
    sw $t0, 8($a0)
    li $t0, 0x0            # rq (rest)
    sw $t0, 12($a0)

    # Loop: loop 4 times to add melody and tune
    li $t4, 4              # Loop counter
loop_start:
    beqz $t4, loop_end     # Exit loop if counter is 0

    # FunctionCall: add(melody, tune)
    la $t0, melody         # Load melody address
    sw $t0, 0($sp)         # Push melody onto stack
    addiu $sp, $sp, -4     # Adjust stack pointer

    la $t0, tune           # Load tune address
    sw $t0, 0($sp)         # Push tune onto stack
    addiu $sp, $sp, -4     # Adjust stack pointer

    jal add                # Call add function

    sub $t4, $t4, 1        # Decrement loop counter
    j loop_start           # Jump back to loop_start
loop_end:

    # Epilogue
    lw $ra, 0($sp)         # Restore return address
    addiu $sp, $sp, 4      # Adjust stack pointer
    lw $fp, 0($sp)         # Reset frame pointer
    jr $ra                 # Exit program

# Function: time
time:
    move $fp, $sp          # Set frame pointer
    sw $ra, 0($sp)         # Save return address
    addiu $sp, $sp, -4     # Adjust stack pointer

    # Load arguments from stack
    lw $a0, 8($fp)         # Load first argument
    lw $a1, 4($fp)         # Load second argument

    # Implementation of time omitted

    lw $ra, 0($sp)         # Restore return address
    addiu $sp, $sp, 8      # Adjust stack pointer
    jr $ra                 # Return to caller

# Function: add
add:
    move $fp, $sp          # Set frame pointer
    sw $ra, 0($sp)         # Save return address
    addiu $sp, $sp, -4     # Adjust stack pointer

    # Load arguments
    lw $a0, 8($fp)         # Load melody (first argument)
    lw $a1, 4($fp)         # Load tune (second argument)

    # Simulate adding tune to melody
    lw $t0, 0($a1)         # Load first note from tune
    sw $t0, 0($a0)         # Add it to melody
    lw $t0, 4($a1)
    sw $t0, 4($a0)
    lw $t0, 8($a1)
    sw $t0, 8($a0)
    lw $t0, 12($a1)
    sw $t0, 12($a0)

    lw $ra, 0($sp)         # Restore return address
    addiu $sp, $sp, 4      # Adjust stack pointer
    jr $ra                 # Return to caller

(4) Loops with Multiple Lines
Tempo t = 144
KeySig ks = cmajor
Tune melody = [[C4q, Cq, Gq, Gq]]
Tune tune1 = [[A4q, Aq, Gq, Gq]]
Tune tune2 = [[B4q, Bq, Gq, Gq]]
loop 2:
	add(melody, tune1)
            add(melody, tune2)

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

.data
t: .word 0          # Tempo variable
ks: .asciiz "cmajor" # KeySig variable
melody: .space 16   # Memory for melody (4 words for 1 bar)
tune1: .space 16    # Memory for tune1 (4 words for 1 bar)
tune2: .space 16    # Memory for tune2 (4 words for 1 bar)

.text
main:
    # Assign Tempo t = 144
    li $t0, 144          # Load constant 144 into $t0
    la $t1, t            # Load address of t into $t1
    sw $t0, 0($t1)       # Store 144 into t

    # Assign KeySig ks = "cmajor"
    la $a0, ks           # Load address of ks into $a0
    li $v0, 4            # Syscall to print string
    syscall              # Print "cmajor"

    # Assign Tune melody = [[C4q, Cq, Gq, Gq]]
    la $t2, melody       # Load address of melody into $t2
    li $t3, 0xC4         # C4q
    sw $t3, 0($t2)
    li $t3, 0xC          # Cq
    sw $t3, 4($t2)
    li $t3, 0xG          # Gq
    sw $t3, 8($t2)
    sw $t3, 12($t2)

    # Assign Tune tune1 = [[A4q, Aq, Gq, Gq]]
    la $t2, tune1        # Load address of tune1 into $t2
    li $t3, 0xA4         # A4q
    sw $t3, 0($t2)
    li $t3, 0xA          # Aq
    sw $t3, 4($t2)
    li $t3, 0xG          # Gq
    sw $t3, 8($t2)
    sw $t3, 12($t2)

    # Assign Tune tune2 = [[B4q, Bq, Gq, Gq]]
    la $t2, tune2        # Load address of tune2 into $t2
    li $t3, 0xB4         # B4q
    sw $t3, 0($t2)
    li $t3, 0xB          # Bq
    sw $t3, 4($t2)
    li $t3, 0xG          # Gq
    sw $t3, 8($t2)
    sw $t3, 12($t2)

    # Loop 2 times
    li $t4, 2            # Loop counter
loop_start:
    beqz $t4, loop_end   # Exit loop if counter is 0

    # FunctionCall add(melody, tune1)
    la $a0, melody       # Argument 1: melody
    la $a1, tune1        # Argument 2: tune1
    jal add              # Call add function

    # FunctionCall add(melody, tune2)
    la $a0, melody       # Argument 1: melody
    la $a1, tune2        # Argument 2: tune2
    jal add              # Call add function

    sub $t4, $t4, 1      # Decrement loop counter
    j loop_start         # Jump back to loop_start
loop_end:

    li $v0, 10           # Exit program
    syscall

# Function: add
# Adds tune data to melody
add:
    lw $t0, 0($a1)       # Load word from tune
    sw $t0, 0($a0)       # Store word to melody
    lw $t0, 4($a1)       # Repeat for next word
    sw $t0, 4($a0)
    lw $t0, 8($a1)
    sw $t0, 8($a0)
    lw $t0, 12($a1)
    sw $t0, 12($a0)
    jr $ra               # Return from function


(5) Multiple Bars
Tune melody = [[C4q, 2q, Gq, Gq], [Aq, Aq, Gq, Gq], [Fq, Fq, Eq, Eq], [Dq, Dq, Cq, Cq]]

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

    # Allocate memory for melody
    la $t0, melody           # Base address for melody array
    li $t1, 4                # Size of each Bar in words (4 notes per bar)
    li $t2, 4                # Number of Bars

    # Bar 1: [C4q, 2q, Gq, Gq]
    la $t3, bar1             # Base address for Bar 1
    li $t4, C4q              # Load first note (C4q)
    sw $t4, 0($t3)           # Store first note in Bar 1
    li $t4, 2q               # Load second note (2q)
    sw $t4, 4($t3)           # Store second note
    li $t4, Gq               # Load third note (Gq)
    sw $t4, 8($t3)           # Store third note
    li $t4, Gq               # Load fourth note (Gq)
    sw $t4, 12($t3)          # Store fourth note
    sw $t3, 0($t0)           # Store base address of Bar 1 in melody array

    # Bar 2: [Aq, Aq, Gq, Gq]
    la $t3, bar2             # Base address for Bar 2
    li $t4, Aq               # Load first note (Aq)
    sw $t4, 0($t3)           # Store first note in Bar 2
    li $t4, Aq               # Load second note (Aq)
    sw $t4, 4($t3)           # Store second note
    li $t4, Gq               # Load third note (Gq)
    sw $t4, 8($t3)           # Store third note
    li $t4, Gq               # Load fourth note (Gq)
    sw $t4, 12($t3)          # Store fourth note
    sw $t3, 4($t0)           # Store base address of Bar 2 in melody array

    # Bar 3: [Fq, Fq, Eq, Eq]
    la $t3, bar3             # Base address for Bar 3
    li $t4, Fq               # Load first note (Fq)
    sw $t4, 0($t3)           # Store first note in Bar 3
    li $t4, Fq               # Load second note (Fq)
    sw $t4, 4($t3)           # Store second note
    li $t4, Eq               # Load third note (Eq)
    sw $t4, 8($t3)           # Store third note
    li $t4, Eq               # Load fourth note (Eq)
    sw $t4, 12($t3)          # Store fourth note
    sw $t3, 8($t0)           # Store base address of Bar 3 in melody array

    # Bar 4: [Dq, Dq, Cq, Cq]
    la $t3, bar4             # Base address for Bar 4
    li $t4, Dq               # Load first note (Dq)
    sw $t4, 0($t3)           # Store first note in Bar 4
    li $t4, Dq               # Load second note (Dq)
    sw $t4, 4($t3)           # Store second note
    li $t4, Cq               # Load third note (Cq)
    sw $t4, 8($t3)           # Store third note
    li $t4, Cq               # Load fourth note (Cq)
    sw $t4, 12($t3)          # Store fourth note
    sw $t3, 12($t0)          # Store base address of Bar 4 in melody array

    # Done
    jr $ra                   # Return to caller
'''
