from py_ass_emul.assembler import assemble
from py_ass_emul.emulator import Emulator

# Dá se i načíst ze souboru (.asm)
code = """
segment code
..start
        MOV AX, stack
        MOV SS, AX
        MOV SP, top

        POP AX          ; F_1
        POP BX          ; F_0
        POP DX          ; n

        PUSH BX         ; vratim F_0
        CMP DX, 1
        JL end          ; pokud je n = 0, program skonci

        PUSH AX         ; vratim F_1

        CMP DX, 2
        JL end

loop:
        CALL func
        DEC DX
        CMP DX, 2
        JL end
        JNC loop

func:
        POP AX         ; F_n-1
        POP BX         ; F_n-2
        
        PUSH AX        ; F_n-1
        ADD AX, BX     ; F_n
        POP CX         ; vratim si F_n-1
        PUSH BX        ; vratim F_n-2
        PUSH CX        ; vratim f_n-1
        PUSH AX        ; ulozim F_n
        RET

end:
        HLT

segment stack
        resb 65530
top:    dw 1  ; F_1
        dw 0  ; F_0
        dw 3  ; n


"""


# Convert to bytecode
program, start, lines_info = assemble(code)

# Initialise emulator with the values
e = Emulator(program, start, lines_info)

# [optional] Set the input of console, edit limit of instructions, 
#   turning off debug mode (stops writing debug info to stdout)
e.console_input = "Hello\nWorld\n"
e.max_instructions = 100_000
# e.debugging_mode = False

# Start
e.run()

# Results can be seen in registers, console output, 
#   statistics of instructions or memmory
print(e.registers)
print("Console output:", e.console_output.replace("\n", "\\n"))
print(e.statistics)

print(e.program)
