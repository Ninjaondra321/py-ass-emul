from assembler import assemble
from emulator import Emulator

# Dá se i načíst ze souboru (.asm)
code = """
segment code
        MOV BX, data
        MOV DS, BX
        MOV DL, [nums]
        MOV DI, 1
cycle   MOV BL, [nums+DI]
        CMP BL, 0
        JNZ nozero
        JMP end
nozero  CMP BL, DL
        JB bellow
        JMP else
bellow  INC BL
        JMP endif
else    JA above
        JMP endif
above   DEC BL
endif   MOV byte [nums+DI], BL
        ADD DI,1
        JMP cycle
end     HLT
segment data
nums    db 64
        db 66
        db 64
        db 9
        db 0

"""


# Převést na bajtkód
program, start, lines_info = assemble(code)

# Inicializovat tím emulátor
e = Emulator(program, start, lines_info)

# [volitelné] Nastavit vstup konzole, upravit maximální počet instrukcí, vypnutí debug módu (vypisování jednotlivých kroků)
e.console_input = "Hello\nWorld\n"
e.max_instructions = 100_000
# e.debugging_mode = False

# Supstit
e.run()

# Výsledek můžete pozorovat např. na registrech, výstupu konzole nebo na statistikách instrukcí
print(e.registers)
print("Console output:", e.console_output.replace("\n", "\\n"))
print(e.statistics)

print(e.program)
