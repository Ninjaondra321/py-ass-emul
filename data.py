PREFIXES = ["CS:", "DS:", "ES:", "SS:"]
PREFIX_CODES = {
    "CS:": 0x2E,
    "DS:": 0x3E,
    "ES:": 0x26,
    "SS:": 0x36,
}

RM_8_REGS = ["AL", "CL", "DL", "BL", "AH", "CH", "DH", "BH"]
RM_16_REGS = ["AX", "CX", "DX", "BX", "SP", "BP", "SI", "DI"]

SEG_REGS = ["ES", "CS", "SS", "DS", "FS", "GS"]

# !! If mod=00, Místo BP je pouze displacement16!!
MOD_00_RM = ["BX+SI", "BX+DI", "BP+SI", "BP+DI", "SI", "DI", "BP", "BX"]

REGISTERS = set(RM_8_REGS + RM_16_REGS + SEG_REGS)
LOWERCASE_REGISTERS = [reg.lower() for reg in REGISTERS]

OPCODES = [
    # Parsed from http://www.mlsite.net/8086/#tbl_map1
    # 0x0_
    ('ADD', 'Eb Gb'), ('ADD', 'Ev Gv'), ('ADD', 'Gb Eb'), ('ADD',
                                                           'Gv Ev'), ('ADD', 'AL Ib'), ('ADD', 'AX Iv'), ('PUSH', 'ES'), ('POP', 'ES'),
    ('OR', 'Eb Gb'), ('OR', 'Ev Gv'), ('OR', 'Gb Eb'), ('OR',
                                                        'Gv Ev'), ('OR', 'AL Ib'), ('OR', 'AX Iv'), ('PUSH', 'CS'), ('', ''),

    # 0x1_
    ('ADC', 'Eb Gb'), ('ADC', 'Ev Gv'), ('ADC', 'Gb Eb'), ('ADC',
                                                           'Gv Ev'), ('ADC', 'AL Ib'), ('ADC', 'AX Iv'), ('PUSH', 'SS'), ('POP', 'SS'),
    ('SBB', 'Eb Gb'), ('SBB', 'Ev Gv'), ('SBB', 'Gb Eb'), ('SBB',
                                                           'Gv Ev'), ('SBB', 'AL Ib'), ('SBB', 'AX Iv'), ('PUSH', 'DS'), ('POP', 'DS'),

    # 0x2_
    ('AND', 'Eb Gb'), ('AND', 'Ev Gv'), ('AND', 'Gb Eb'), ('AND',
                                                           'Gv Ev'), ('AND', 'AL Ib'), ('AND', 'AX Iv'), ('ES:', 'prefix'), ('DAA', ''),
    ('SUB', 'Eb Gb'), ('SUB', 'Ev Gv'), ('SUB', 'Gb Eb'), ('SUB',
                                                           'Gv Ev'), ('SUB', 'AL Ib'), ('SUB', 'AX Iv'), ('CS:', 'prefix'), ('DAS', ''),

    # 0x3_
    ('XOR', 'Eb Gb'), ('XOR', 'Ev Gv'), ('XOR', 'Gb Eb'), ('XOR',
                                                           'Gv Ev'), ('XOR', 'AL Ib'), ('XOR', 'AX Iv'), ('SS:', 'prefix'), ('AAA', ''),
    ('CMP', 'Eb Gb'), ('CMP', 'Ev Gv'), ('CMP', 'Gb Eb'), ('CMP',
                                                           'Gv Ev'), ('CMP', 'AL Ib'), ('CMP', 'AX Iv'), ('DS:', 'prefix'), ('AAS', ''),

    # 0x4_
    ('INC', 'AX'), ('INC', 'CX'), ('INC', 'DX'), ('INC',
                                                  'BX'), ('INC', 'SP'), ('INC', 'BP'), ('INC', 'SI'), ('INC', 'DI'),
    ('DEC', 'AX'), ('DEC', 'CX'), ('DEC', 'DX'), ('DEC',
                                                  'BX'), ('DEC', 'SP'), ('DEC', 'BP'), ('DEC', 'SI'), ('DEC', 'DI'),

    # 0x5_
    ('PUSH', 'AX'), ('PUSH', 'CX'), ('PUSH', 'DX'), ('PUSH',
                                                     'BX'), ('PUSH', 'SP'), ('PUSH', 'BP'), ('PUSH', 'SI'), ('PUSH', 'DI'),
    ('POP', 'AX'), ('POP', 'CX'), ('POP', 'DX'), ('POP',
                                                  'BX'), ('POP', 'SP'), ('POP', 'BP'), ('POP', 'SI'), ('POP', 'DI'),

    # 0x6_  Not relevant for KSI emulator
    ('--', ''), ('--', ''), ('--', ''), ('--',
                                         ''), ('--', ''), ('--', ''), ('--', ''), ('--', ''),
    ('--', ''), ('--', ''), ('--', ''), ('--',
                                         ''), ('--', ''), ('--', ''), ('--', ''), ('--', ''),

    # 0x7_
    ('JO', 'Jb'), ('JNO', 'Jb'), ('JB', 'Jb'), ('JNB', 'Jb'), ('JZ',
                                                               'Jb'), ('JNZ', 'Jb'), ('JBE', 'Jb'), ('JA', 'Jb'),
    ('JS', 'Jb'), ('JNS', 'Jb'), ('JPE', 'Jb'), ('JPO',
                                                 'Jb'), ('JL', 'Jb'), ('JGE', 'Jb'), ('JLE', 'Jb'), ('JG', 'Jb'),

    # 0x8_
    ('GRP1', 'Eb Ib'), ('GRP1', 'Ev Iv'), ('GRP1', 'Eb Ib'), ('GRP1', 'Ev Ib'), ('TEST',
                                                                                 'Gb Eb'), ('TEST', 'Gv Ev'), ('XCHG', 'Gb Eb'), ('XCHG', 'Gv Ev'),
    ('MOV', 'Eb Gb'), ('MOV', 'Ev Gv'), ('MOV', 'Gb Eb'), ('MOV',
                                                           'Gv Ev'), ('MOV', 'Ew Sw'), ('LEA', 'Gv M'), ('MOV', 'Sw Ew'), ('POP', 'Ev'),

    # 0x9_
    ('NOP', ''), ('XCHG', 'CX AX'), ('XCHG', 'DX AX'), ('XCHG', 'BX AX'), ('XCHG',
                                                                           'SP AX'), ('XCHG', 'BP AX'), ('XCHG', 'SI AX'), ('XCHG', 'DI AX'),
    ('CBW', ''), ('CWD', ''), ('CALL', 'Ap'), ('WAIT',
                                               ''), ('PUSHF', ''), ('POPF', ''), ('SAHF', ''), ('LAHF', ''),

    # 0xA_
    ('MOV', 'AL Ob'), ('MOV', 'AX Ov'), ('MOV', 'Ob AL'), ('MOV',
                                                           'Ov AX'), ('MOVSB', ''), ('MOVSW', ''), ('CMPSB', ''), ('CMPSW', ''),
    ('TEST', 'AL Ib'), ('TEST', 'AX Iv'), ('STOSB', ''), ('STOSW',
                                                          ''), ('LODSB', ''), ('LODSW', ''), ('SCASB', ''), ('SCASW', ''),

    # 0xB_
    ('MOV', 'AL Ib'), ('MOV', 'CL Ib'), ('MOV', 'DL Ib'), ('MOV', 'BL Ib'), ('MOV',
                                                                             'AH Ib'), ('MOV', 'CH Ib'), ('MOV', 'DH Ib'), ('MOV', 'BH Ib'),
    ('MOV', 'AX Iv'), ('MOV', 'CX Iv'), ('MOV', 'DX Iv'), ('MOV', 'BX Iv'), ('MOV',
                                                                             'SP Iv'), ('MOV', 'BP Iv'), ('MOV', 'SI Iv'), ('MOV', 'DI Iv'),

    # 0xC_
    ('', ''), ('', ''), ('RET', 'Iw'), ('RET', ''), ('LES',
                                                     'Gv Mp'), ('LDS', 'Gv Mp'), ('MOV', 'Eb Ib'), ('MOV', 'Ev Iv'),
    ('', ''), ('', ''), ('RETF', 'Iw'), ('RETF', ''), ('INT',
                                                       '3'), ('INT', 'Ib'), ('INTO', ''), ('IRET', ''),

    # 0xD_
    ('GRP2', 'Eb 1'), ('GRP2', 'Ev 1'), ('GRP2', 'Eb CL'), ('GRP2',
                                                            'Ev CL'), ('AAM', 'I0'), ('AAD', 'I0'), ('', ''), ('XLAT', ''),
    ('CO-PROCESSOR INSTRUCTIONS', ''), ('--', ''), ('--',
                                                    ''), ('--', ''), ('--', ''), ('--', ''), ('--', ''), ('--', ''),

    # 0xE_
    ('LOOPNZ', 'Jb'), ('LOOPZ', 'Jb'), ('LOOP', 'Jb'), ('JCXZ', 'Jb'), ('IN',
                                                                        'AL Ib'), ('IN', 'AX Ib'), ('OUT', 'Ib AL'), ('OUT', 'Ib AX'),
    ('CALL', 'Jv'), ('JMP', 'Jv'), ('JMP', 'Ap'), ('JMP', 'Jb'), ('IN',
                                                                  'AL DX'), ('IN', 'AX DX'), ('OUT', 'DX AL'), ('OUT', 'DX AX'),

    # 0xF_
    ('LOCK', ''), ('', ''), ('REPNZ', ''), ('REPZ', ''), ('HLT',
                                                          ''), ('CMC', ''), ('GRP3a', 'Eb'), ('GRP3b', 'Ev'),
    ('CLC', ''), ('STC', ''), ('CLI', ''), ('STI', ''), ('CLD',
                                                         ''), ('STD', ''), ('GRP4', 'Eb'), ('GRP5', 'Ev'),
]

GRPs = {
    "GRP1": [('ADD', ''), ('OR', ''), ('ADC', ''), ('SBB', ''), ('AND', ''), ('SUB', ''), ('XOR', ''), ('CMP', '')],
    "GRP2": [('ROL', ''), ('ROR', ''), ('RCL', ''), ('RCR', ''), ('SHL', ''), ('SHR', ''), ('--', ''), ('SAR', '')],
    "GRP3a": [('TEST', 'Eb Ib'), ('--', ''), ('NOT', ''), ('NEG', ''), ('MUL', ''), ('IMUL', ''), ('DIV', ''), ('IDIV', '')],
    "GRP3b": [('TEST', 'Ev Iv'), ('--', ''), ('NOT', ''), ('NEG', ''), ('MUL', ''), ('IMUL', ''), ('DIV', ''), ('IDIV', '')],
    "GRP4": [('INC', ''), ('DEC', ''), ('--', ''), ('--', ''), ('--', ''), ('--', ''), ('--', ''), ('--', '')],
    "GRP5": [('INC', ''), ('DEC', ''), ('CALL', ''), ('CALL', 'Mp'), ('JMP', ''), ('JMP', 'Mp'), ('PUSH', ''), ('--', '')]
}

GRP2_INSTRUCTIONS = [instr[0] for instr in GRPs["GRP2"]]

INSTRUCTIONS_WITHOUT_PARAMETER = {"DAA", "DAS", "AAA", "AAS", "NOP", "CBW", "CWD", "WAIT", "PUSHF", "POPF", "SAHF", "LAHF", "MOVSB", "MOVSW",
                                  "CMPSB", "CMPSW", "STOSB", "STOSW", "LODSB", "LODSW", "SCASB", "SCASW", "RET", "RETF", "INTO", "IRET", "XLAT",
                                  "LOCK", "REPNZ", "REPZ", "HLT", "CMC", "CLC", "STC", "CLI", "STI", "CLD", "STD"}

DATA_INSTRUCTIONS = {"DB", "DW", "DD", "RESB", "RESW", "RESD"}

STRING_QUOTES = ['"', "'"]

# Flags
Flag = int
CF, PF, ZF, SF, TF, IF, OF = 0, 2, 6, 7, 8, 9, 11

SIMPLE_CONDITION_JMPS = {
    'JE': [(ZF, 1)],
    'JZ': [(ZF, 1)],
    'JNE': [(ZF, 0)],
    'JNZ': [(ZF, 0)],
    'JP': [(PF, 1)],
    'JPE': [(PF, 1)],
    'JNP': [(PF, 0)],
    'JPO': [(PF, 0)],
    'JS': [(SF, 1)],
    'JNS': [(SF, 0)],
    'JC': [(CF, 1)],
    'JNC': [(CF, 0)],
    'JO': [(OF, 1)],
    'JNO': [(OF, 0)],
    'JB': [(CF, 1)],
    'JNAE': [(CF, 1)],
    'JA': [(CF, 0), (ZF, 0)],
    'JNBE': [(CF, 0), (ZF, 0)],
    'JBE': [(CF, 1), (ZF, 1)],
    'JNA': [(CF, 1), (ZF, 1)],
    'JAE': [(CF, 0)],
    'JNB': [(CF, 0)],
    # Ještě chybí JL, JNGE, JG, JNLE, JLE, JNG, JGE, JNL
    # ty se ale nedají definovat jednoduchou podmínkou
}

# For filling the instructions dictionary
MISSING_CONDITION_JMPS = ['JL', 'JNGE',
                          'JG', 'JNLE', 'JLE', 'JNG', 'JGE', 'JNL']

INSTRUCTION_ALIASES = {
    "JE": "JZ",
    "JNE": "JNZ",
    "JP": "JPE",
    "JNP": "JPO",

    "JNAE": "JB",
    "JNGE": "JL",
    "JNBE": "JA",
    "JNLE": "JG",
    "JNA": "JBE",
    "JNG": "JLE",
    "JAE": "JNB",
    "JNL": "JGE",
    "JC": "JB",
    "JNC": "JNB",

    "SAL": "SHL",
}

EXPLICITLY_NOT_SUPPORTED_INSTRUCTIONS = ["LEA"]

INSTRUCTIONS_v2 = {
    "ADD8": [
        ("Eb Gb", {"opcode": 0, "expected_length": 4}),
        ("Gb Eb", {"opcode": 2, "expected_length": 4}),
        ("AL Ib", {"opcode": 4, "expected_length": 2}),
        ("Eb Ib", {"opcode": 128, "modrm": 0, "expected_length": 5}),
        ("Eb Ib", {"opcode": 130, "modrm": 0, "expected_length": 5}),
        ("Ev Ib", {"opcode": 131, "modrm": 0, "expected_length": 5}),
    ],
    "ADD16": [
        ("Ev Gv", {"opcode": 1, "expected_length": 4}),
        ("Gv Ev", {"opcode": 3, "expected_length": 4}),
        ("AX Iv", {"opcode": 5, "expected_length": 3}),
        ("Ev Iv", {"opcode": 129, "modrm": 0, "expected_length": 6}),
    ],
    "PUSH16": [
        ("ES", {"opcode": 6, "expected_length": 1}),
        ("CS", {"opcode": 14, "expected_length": 1}),
        ("SS", {"opcode": 22, "expected_length": 1}),
        ("DS", {"opcode": 30, "expected_length": 1}),
        ("AX", {"opcode": 80, "expected_length": 1}),
        ("CX", {"opcode": 81, "expected_length": 1}),
        ("DX", {"opcode": 82, "expected_length": 1}),
        ("BX", {"opcode": 83, "expected_length": 1}),
        ("SP", {"opcode": 84, "expected_length": 1}),
        ("BP", {"opcode": 85, "expected_length": 1}),
        ("SI", {"opcode": 86, "expected_length": 1}),
        ("DI", {"opcode": 87, "expected_length": 1}),
    ],
    "PUSH32": [("Ev", {"opcode": 255, "modrm": 48, "expected_length": 6})],
    "POP16": [
        ("ES", {"opcode": 7, "expected_length": 1}),
        ("SS", {"opcode": 23, "expected_length": 1}),
        ("DS", {"opcode": 31, "expected_length": 1}),
        ("AX", {"opcode": 88, "expected_length": 1}),
        ("CX", {"opcode": 89, "expected_length": 1}),
        ("DX", {"opcode": 90, "expected_length": 1}),
        ("BX", {"opcode": 91, "expected_length": 1}),
        ("SP", {"opcode": 92, "expected_length": 1}),
        ("BP", {"opcode": 93, "expected_length": 1}),
        ("SI", {"opcode": 94, "expected_length": 1}),
        ("DI", {"opcode": 95, "expected_length": 1}),
        ("Ev", {"opcode": 143, "expected_length": 4}),
    ],
    "OR8": [
        ("Eb Gb", {"opcode": 8, "expected_length": 4}),
        ("Gb Eb", {"opcode": 10, "expected_length": 4}),
        ("AL Ib", {"opcode": 12, "expected_length": 2}),
        ("Eb Ib", {"opcode": 128, "modrm": 8, "expected_length": 5}),
        ("Eb Ib", {"opcode": 130, "modrm": 8, "expected_length": 5}),
        ("Ev Ib", {"opcode": 131, "modrm": 8, "expected_length": 5}),
    ],
    "OR16": [
        ("Ev Gv", {"opcode": 9, "expected_length": 4}),
        ("Gv Ev", {"opcode": 11, "expected_length": 4}),
        ("AX Iv", {"opcode": 13, "expected_length": 3}),
        ("Ev Iv", {"opcode": 129, "modrm": 8, "expected_length": 6}),
    ],
    "ADC8": [
        ("Eb Gb", {"opcode": 16, "expected_length": 4}),
        ("Gb Eb", {"opcode": 18, "expected_length": 4}),
        ("AL Ib", {"opcode": 20, "expected_length": 2}),
        ("Eb Ib", {"opcode": 128, "modrm": 16, "expected_length": 5}),
        ("Eb Ib", {"opcode": 130, "modrm": 16, "expected_length": 5}),
        ("Ev Ib", {"opcode": 131, "modrm": 16, "expected_length": 5}),
    ],
    "ADC16": [
        ("Ev Gv", {"opcode": 17, "expected_length": 4}),
        ("Gv Ev", {"opcode": 19, "expected_length": 4}),
        ("AX Iv", {"opcode": 21, "expected_length": 3}),
        ("Ev Iv", {"opcode": 129, "modrm": 16, "expected_length": 6}),
    ],
    "SBB8": [
        ("Eb Gb", {"opcode": 24, "expected_length": 4}),
        ("Gb Eb", {"opcode": 26, "expected_length": 4}),
        ("AL Ib", {"opcode": 28, "expected_length": 2}),
        ("Eb Ib", {"opcode": 128, "modrm": 24, "expected_length": 5}),
        ("Eb Ib", {"opcode": 130, "modrm": 24, "expected_length": 5}),
        ("Ev Ib", {"opcode": 131, "modrm": 24, "expected_length": 5}),
    ],
    "SBB16": [
        ("Ev Gv", {"opcode": 25, "expected_length": 4}),
        ("Gv Ev", {"opcode": 27, "expected_length": 4}),
        ("AX Iv", {"opcode": 29, "expected_length": 3}),
        ("Ev Iv", {"opcode": 129, "modrm": 24, "expected_length": 6}),
    ],
    "AND8": [
        ("Eb Gb", {"opcode": 32, "expected_length": 4}),
        ("Gb Eb", {"opcode": 34, "expected_length": 4}),
        ("AL Ib", {"opcode": 36, "expected_length": 2}),
        ("Eb Ib", {"opcode": 128, "modrm": 32, "expected_length": 5}),
        ("Eb Ib", {"opcode": 130, "modrm": 32, "expected_length": 5}),
        ("Ev Ib", {"opcode": 131, "modrm": 32, "expected_length": 5}),
    ],
    "AND16": [
        ("Ev Gv", {"opcode": 33, "expected_length": 4}),
        ("Gv Ev", {"opcode": 35, "expected_length": 4}),
        ("AX Iv", {"opcode": 37, "expected_length": 3}),
        ("Ev Iv", {"opcode": 129, "modrm": 32, "expected_length": 6}),
    ],
    "DAA0": [("", {"opcode": 39, "expected_length": 1})],
    "SUB8": [
        ("Eb Gb", {"opcode": 40, "expected_length": 4}),
        ("Gb Eb", {"opcode": 42, "expected_length": 4}),
        ("AL Ib", {"opcode": 44, "expected_length": 2}),
        ("Eb Ib", {"opcode": 128, "modrm": 40, "expected_length": 5}),
        ("Eb Ib", {"opcode": 130, "modrm": 40, "expected_length": 5}),
        ("Ev Ib", {"opcode": 131, "modrm": 40, "expected_length": 5}),
    ],
    "SUB16": [
        ("Ev Gv", {"opcode": 41, "expected_length": 4}),
        ("Gv Ev", {"opcode": 43, "expected_length": 4}),
        ("AX Iv", {"opcode": 45, "expected_length": 3}),
        ("Ev Iv", {"opcode": 129, "modrm": 40, "expected_length": 6}),
    ],
    "DAS0": [("", {"opcode": 47, "expected_length": 1})],
    "XOR8": [
        ("Eb Gb", {"opcode": 48, "expected_length": 4}),
        ("Gb Eb", {"opcode": 50, "expected_length": 4}),
        ("AL Ib", {"opcode": 52, "expected_length": 2}),
        ("Eb Ib", {"opcode": 128, "modrm": 48, "expected_length": 5}),
        ("Eb Ib", {"opcode": 130, "modrm": 48, "expected_length": 5}),
        ("Ev Ib", {"opcode": 131, "modrm": 48, "expected_length": 5}),
    ],
    "XOR16": [
        ("Ev Gv", {"opcode": 49, "expected_length": 4}),
        ("Gv Ev", {"opcode": 51, "expected_length": 4}),
        ("AX Iv", {"opcode": 53, "expected_length": 3}),
        ("Ev Iv", {"opcode": 129, "modrm": 48, "expected_length": 6}),
    ],
    "AAA0": [("", {"opcode": 55, "expected_length": 1})],
    "CMP8": [
        ("Eb Gb", {"opcode": 56, "expected_length": 4}),
        ("Gb Eb", {"opcode": 58, "expected_length": 4}),
        ("AL Ib", {"opcode": 60, "expected_length": 2}),
        ("Eb Ib", {"opcode": 128, "modrm": 56, "expected_length": 5}),
        ("Eb Ib", {"opcode": 130, "modrm": 56, "expected_length": 5}),
        ("Ev Ib", {"opcode": 131, "modrm": 56, "expected_length": 5}),
    ],
    "CMP16": [
        ("Ev Gv", {"opcode": 57, "expected_length": 4}),
        ("Gv Ev", {"opcode": 59, "expected_length": 4}),
        ("AX Iv", {"opcode": 61, "expected_length": 3}),
        ("Ev Iv", {"opcode": 129, "modrm": 56, "expected_length": 6}),
    ],
    "AAS0": [("", {"opcode": 63, "expected_length": 1})],
    "INC16": [
        ("AX", {"opcode": 64, "expected_length": 1}),
        ("CX", {"opcode": 65, "expected_length": 1}),
        ("DX", {"opcode": 66, "expected_length": 1}),
        ("BX", {"opcode": 67, "expected_length": 1}),
        ("SP", {"opcode": 68, "expected_length": 1}),
        ("BP", {"opcode": 69, "expected_length": 1}),
        ("SI", {"opcode": 70, "expected_length": 1}),
        ("DI", {"opcode": 71, "expected_length": 1}),
        ("Ev", {"opcode": 255, "modrm": 0, "expected_length": 4}),
    ],
    "INC8": [("Eb", {"opcode": 254, "modrm": 0, "expected_length": 4})],
    "DEC16": [
        ("AX", {"opcode": 72, "expected_length": 1}),
        ("CX", {"opcode": 73, "expected_length": 1}),
        ("DX", {"opcode": 74, "expected_length": 1}),
        ("BX", {"opcode": 75, "expected_length": 1}),
        ("SP", {"opcode": 76, "expected_length": 1}),
        ("BP", {"opcode": 77, "expected_length": 1}),
        ("SI", {"opcode": 78, "expected_length": 1}),
        ("DI", {"opcode": 79, "expected_length": 1}),
        ("Ev", {"opcode": 255, "modrm": 8, "expected_length": 4}),
    ],
    "DEC8": [("Eb", {"opcode": 254, "modrm": 8, "expected_length": 4})],
    "JO8": [("Jb", {"opcode": 112, "expected_length": 2})],
    "JNO8": [("Jb", {"opcode": 113, "expected_length": 2})],
    "JB8": [("Jb", {"opcode": 114, "expected_length": 2})],
    "JNB8": [("Jb", {"opcode": 115, "expected_length": 2})],
    "JZ8": [("Jb", {"opcode": 116, "expected_length": 2})],
    "JNZ8": [("Jb", {"opcode": 117, "expected_length": 2})],
    "JBE8": [("Jb", {"opcode": 118, "expected_length": 2})],
    "JA8": [("Jb", {"opcode": 119, "expected_length": 2})],
    "JS8": [("Jb", {"opcode": 120, "expected_length": 2})],
    "JNS8": [("Jb", {"opcode": 121, "expected_length": 2})],
    "JPE8": [("Jb", {"opcode": 122, "expected_length": 2})],
    "JPO8": [("Jb", {"opcode": 123, "expected_length": 2})],
    "JL8": [("Jb", {"opcode": 124, "expected_length": 2})],
    "JGE8": [("Jb", {"opcode": 125, "expected_length": 2})],
    "JLE8": [("Jb", {"opcode": 126, "expected_length": 2})],
    "JG8": [("Jb", {"opcode": 127, "expected_length": 2})],
    "TEST8": [
        ("Gb Eb", {"opcode": 132, "expected_length": 4}),
        ("AL Ib", {"opcode": 168, "expected_length": 2}),
        ("Eb Ib", {"opcode": 246, "modrm": 0, "expected_length": 5}),
    ],
    "TEST16": [
        ("Gv Ev", {"opcode": 133, "expected_length": 4}),
        ("AX Iv", {"opcode": 169, "expected_length": 3}),
        ("Ev Iv", {"opcode": 247, "modrm": 0, "expected_length": 6}),
    ],
    "XCHG8": [("Gb Eb", {"opcode": 134, "expected_length": 4})],
    "XCHG16": [
        ("Gv Ev", {"opcode": 135, "expected_length": 4}),
        ("CX AX", {"opcode": 145, "expected_length": 1}),
        ("DX AX", {"opcode": 146, "expected_length": 1}),
        ("BX AX", {"opcode": 147, "expected_length": 1}),
        ("SP AX", {"opcode": 148, "expected_length": 1}),
        ("BP AX", {"opcode": 149, "expected_length": 1}),
        ("SI AX", {"opcode": 150, "expected_length": 1}),
        ("DI AX", {"opcode": 151, "expected_length": 1}),
    ],
    "MOV8": [
        ("Eb Gb", {"opcode": 136, "expected_length": 4}),
        ("Gb Eb", {"opcode": 138, "expected_length": 4}),
        ("AL Ob", {"opcode": 160, "expected_length": 3}),
        ("Ob AL", {"opcode": 162, "expected_length": 3}),
        ("AL Ib", {"opcode": 176, "expected_length": 2}),
        ("CL Ib", {"opcode": 177, "expected_length": 2}),
        ("DL Ib", {"opcode": 178, "expected_length": 2}),
        ("BL Ib", {"opcode": 179, "expected_length": 2}),
        ("AH Ib", {"opcode": 180, "expected_length": 2}),
        ("CH Ib", {"opcode": 181, "expected_length": 2}),
        ("DH Ib", {"opcode": 182, "expected_length": 2}),
        ("BH Ib", {"opcode": 183, "expected_length": 2}),
        ("Eb Ib", {"opcode": 198, "expected_length": 5}),
    ],
    "MOV16": [
        ("Ev Gv", {"opcode": 137, "expected_length": 4}),
        ("Gv Ev", {"opcode": 139, "expected_length": 4}),
        ("Ew Sw", {"opcode": 140, "expected_length": 4}),
        ("Sw Ew", {"opcode": 142, "expected_length": 4}),
        ("AX Ov", {"opcode": 161, "expected_length": 3}),
        ("Ov AX", {"opcode": 163, "expected_length": 3}),
        ("AX Iv", {"opcode": 184, "expected_length": 3}),
        ("CX Iv", {"opcode": 185, "expected_length": 3}),
        ("DX Iv", {"opcode": 186, "expected_length": 3}),
        ("BX Iv", {"opcode": 187, "expected_length": 3}),
        ("SP Iv", {"opcode": 188, "expected_length": 3}),
        ("BP Iv", {"opcode": 189, "expected_length": 3}),
        ("SI Iv", {"opcode": 190, "expected_length": 3}),
        ("DI Iv", {"opcode": 191, "expected_length": 3}),
        ("Ev Iv", {"opcode": 199, "expected_length": 6}),
    ],
    "LEA16": [("Gv M", {"opcode": 141, "expected_length": 2})],
    "NOP0": [("", {"opcode": 144, "expected_length": 1})],
    "CBW0": [("", {"opcode": 152, "expected_length": 1})],
    "CWD0": [("", {"opcode": 153, "expected_length": 1})],
    "CALL32": [
        ("Ap", {"opcode": 154, "expected_length": 5}),
        ("Ev", {"opcode": 255, "modrm": 24, "expected_length": 6}),
    ],
    "CALL16": [
        ("Jv", {"opcode": 232, "expected_length": 3}),
        ("Ev", {"opcode": 255, "modrm": 16, "expected_length": 4}),
    ],
    "WAIT0": [("", {"opcode": 155, "expected_length": 1})],
    "PUSHF0": [("", {"opcode": 156, "expected_length": 1})],
    "POPF0": [("", {"opcode": 157, "expected_length": 1})],
    "SAHF0": [("", {"opcode": 158, "expected_length": 1})],
    "LAHF0": [("", {"opcode": 159, "expected_length": 1})],
    "MOVSB0": [("", {"opcode": 164, "expected_length": 1})],
    "MOVSW0": [("", {"opcode": 165, "expected_length": 1})],
    "CMPSB0": [("", {"opcode": 166, "expected_length": 1})],
    "CMPSW0": [("", {"opcode": 167, "expected_length": 1})],
    "STOSB0": [("", {"opcode": 170, "expected_length": 1})],
    "STOSW0": [("", {"opcode": 171, "expected_length": 1})],
    "LODSB0": [("", {"opcode": 172, "expected_length": 1})],
    "LODSW0": [("", {"opcode": 173, "expected_length": 1})],
    "SCASB0": [("", {"opcode": 174, "expected_length": 1})],
    "SCASW0": [("", {"opcode": 175, "expected_length": 1})],
    "RET16": [("Iw", {"opcode": 194, "expected_length": 3})],
    "RET0": [("", {"opcode": 195, "expected_length": 1})],
    "LES16": [("Gv Mp", {"opcode": 196, "expected_length": 6})],
    "LDS16": [("Gv Mp", {"opcode": 197, "expected_length": 6})],
    "RETF16": [("Iw", {"opcode": 202, "expected_length": 3})],
    "RETF0": [("", {"opcode": 203, "expected_length": 1})],
    "INT0": [("3", {"opcode": 204, "expected_length": 1})],
    "INT8": [("Ib", {"opcode": 205, "expected_length": 2})],
    "INTO0": [("", {"opcode": 206, "expected_length": 1})],
    "IRET0": [("", {"opcode": 207, "expected_length": 1})],
    "AAM0": [("I0", {"opcode": 212, "expected_length": 3})],
    "AAD0": [("I0", {"opcode": 213, "expected_length": 3})],
    "XLAT0": [("", {"opcode": 215, "expected_length": 1})],
    "CO-PROCESSOR INSTRUCTIONS0": [("", {"opcode": 216, "expected_length": 1})],
    "LOOPNZ8": [("Jb", {"opcode": 224, "expected_length": 2})],
    "LOOPZ8": [("Jb", {"opcode": 225, "expected_length": 2})],
    "LOOP8": [("Jb", {"opcode": 226, "expected_length": 2})],
    "JCXZ8": [("Jb", {"opcode": 227, "expected_length": 2})],
    "IN8": [
        ("AL Ib", {"opcode": 228, "expected_length": 2}),
        ("AX Ib", {"opcode": 229, "expected_length": 2}),
        ("AL DX", {"opcode": 236, "expected_length": 1}),
    ],
    "IN16": [("AX DX", {"opcode": 237, "expected_length": 1})],
    "OUT8": [
        ("Ib AL", {"opcode": 230, "expected_length": 2}),
        ("Ib AX", {"opcode": 231, "expected_length": 2}),
    ],
    "OUT16": [
        ("DX AL", {"opcode": 238, "expected_length": 1}),
        ("DX AX", {"opcode": 239, "expected_length": 1}),
    ],
    "JMP16": [("Jv", {"opcode": 233, "expected_length": 3})],
    "JMP32": [
        ("Ap", {"opcode": 234, "expected_length": 5}),
        ("Ev", {"opcode": 255, "modrm": 32, "expected_length": 6}),
        ("Ev", {"opcode": 255, "modrm": 40, "expected_length": 6}),
    ],
    "JMP8": [("Jb", {"opcode": 235, "expected_length": 2})],
    "LOCK0": [("", {"opcode": 240, "expected_length": 1})],
    "REPNZ0": [("", {"opcode": 242, "expected_length": 1})],
    "REPZ0": [("", {"opcode": 243, "expected_length": 1})],
    "HLT0": [("", {"opcode": 244, "expected_length": 1})],
    "CMC0": [("", {"opcode": 245, "expected_length": 1})],
    "CLC0": [("", {"opcode": 248, "expected_length": 1})],
    "STC0": [("", {"opcode": 249, "expected_length": 1})],
    "CLI0": [("", {"opcode": 250, "expected_length": 1})],
    "STI0": [("", {"opcode": 251, "expected_length": 1})],
    "CLD0": [("", {"opcode": 252, "expected_length": 1})],
    "STD0": [("", {"opcode": 253, "expected_length": 1})],
    "ROL8": [
        ("Eb 1", {"opcode": 208, "modrm": 0, "expected_length": 4}),
        ("Eb 1", {"opcode": 208, "modrm": 0, "expected_length": 4}),
        ("Eb 1", {"opcode": 208, "modrm": 0, "expected_length": 2}),
        ("Eb CL", {"opcode": 210, "modrm": 0, "expected_length": 2}),
        ("Eb 1", {"opcode": 208, "modrm": 0, "expected_length": 2}),
        ("Eb CL", {"opcode": 210, "modrm": 0, "expected_length": 2}),
    ],
    "ROL16": [
        ("Ev 1", {"opcode": 209, "modrm": 0, "expected_length": 4}),
        ("Ev 1", {"opcode": 209, "modrm": 0, "expected_length": 4}),
        ("Ev 1", {"opcode": 209, "modrm": 0, "expected_length": 2}),
        ("Ev CL", {"opcode": 211, "modrm": 0, "expected_length": 2}),
    ],
    "ROR8": [
        ("Eb 1", {"opcode": 208, "modrm": 8, "expected_length": 4}),
        ("Eb 1", {"opcode": 208, "modrm": 8, "expected_length": 4}),
        ("Eb 1", {"opcode": 208, "modrm": 8, "expected_length": 2}),
        ("Eb CL", {"opcode": 210, "modrm": 8, "expected_length": 2}),
        ("Eb 1", {"opcode": 208, "modrm": 8, "expected_length": 2}),
        ("Eb CL", {"opcode": 210, "modrm": 8, "expected_length": 2}),
    ],
    "ROR16": [
        ("Ev 1", {"opcode": 209, "modrm": 8, "expected_length": 4}),
        ("Ev 1", {"opcode": 209, "modrm": 8, "expected_length": 4}),
        ("Ev 1", {"opcode": 209, "modrm": 8, "expected_length": 2}),
        ("Ev CL", {"opcode": 211, "modrm": 8, "expected_length": 2}),
    ],
    "RCL8": [
        ("Eb 1", {"opcode": 208, "modrm": 16, "expected_length": 4}),
        ("Eb 1", {"opcode": 208, "modrm": 16, "expected_length": 4}),
        ("Eb 1", {"opcode": 208, "modrm": 16, "expected_length": 2}),
        ("Eb CL", {"opcode": 210, "modrm": 16, "expected_length": 2}),
        ("Eb 1", {"opcode": 208, "modrm": 16, "expected_length": 2}),
        ("Eb CL", {"opcode": 210, "modrm": 16, "expected_length": 2}),
    ],
    "RCL16": [
        ("Ev 1", {"opcode": 209, "modrm": 16, "expected_length": 4}),
        ("Ev 1", {"opcode": 209, "modrm": 16, "expected_length": 4}),
        ("Ev 1", {"opcode": 209, "modrm": 16, "expected_length": 2}),
        ("Ev CL", {"opcode": 211, "modrm": 16, "expected_length": 2}),
    ],
    "RCR8": [
        ("Eb 1", {"opcode": 208, "modrm": 24, "expected_length": 4}),
        ("Eb 1", {"opcode": 208, "modrm": 24, "expected_length": 4}),
        ("Eb 1", {"opcode": 208, "modrm": 24, "expected_length": 2}),
        ("Eb CL", {"opcode": 210, "modrm": 24, "expected_length": 2}),
        ("Eb 1", {"opcode": 208, "modrm": 24, "expected_length": 2}),
        ("Eb CL", {"opcode": 210, "modrm": 24, "expected_length": 2}),
    ],
    "RCR16": [
        ("Ev 1", {"opcode": 209, "modrm": 24, "expected_length": 4}),
        ("Ev 1", {"opcode": 209, "modrm": 24, "expected_length": 4}),
        ("Ev 1", {"opcode": 209, "modrm": 24, "expected_length": 2}),
        ("Ev CL", {"opcode": 211, "modrm": 24, "expected_length": 2}),
    ],
    "SHL8": [
        ("Eb 1", {"opcode": 208, "modrm": 32, "expected_length": 4}),
        ("Eb 1", {"opcode": 208, "modrm": 32, "expected_length": 4}),
        ("Eb 1", {"opcode": 208, "modrm": 32, "expected_length": 2}),
        ("Eb CL", {"opcode": 210, "modrm": 32, "expected_length": 2}),
        ("Eb 1", {"opcode": 208, "modrm": 32, "expected_length": 2}),
        ("Eb CL", {"opcode": 210, "modrm": 32, "expected_length": 2}),
    ],
    "SHL16": [
        ("Ev 1", {"opcode": 209, "modrm": 32, "expected_length": 4}),
        ("Ev 1", {"opcode": 209, "modrm": 32, "expected_length": 4}),
        ("Ev 1", {"opcode": 209, "modrm": 32, "expected_length": 2}),
        ("Ev CL", {"opcode": 211, "modrm": 32, "expected_length": 2}),
    ],
    "SHR8": [
        ("Eb 1", {"opcode": 208, "modrm": 40, "expected_length": 4}),
        ("Eb 1", {"opcode": 208, "modrm": 40, "expected_length": 4}),
        ("Eb 1", {"opcode": 208, "modrm": 40, "expected_length": 2}),
        ("Eb CL", {"opcode": 210, "modrm": 40, "expected_length": 2}),
        ("Eb 1", {"opcode": 208, "modrm": 40, "expected_length": 2}),
        ("Eb CL", {"opcode": 210, "modrm": 40, "expected_length": 2}),
    ],
    "SHR16": [
        ("Ev 1", {"opcode": 209, "modrm": 40, "expected_length": 4}),
        ("Ev 1", {"opcode": 209, "modrm": 40, "expected_length": 4}),
        ("Ev 1", {"opcode": 209, "modrm": 40, "expected_length": 2}),
        ("Ev CL", {"opcode": 211, "modrm": 40, "expected_length": 2}),
    ],
    "SAR8": [
        ("Eb 1", {"opcode": 208, "modrm": 56, "expected_length": 4}),
        ("Eb 1", {"opcode": 208, "modrm": 56, "expected_length": 4}),
        ("Eb 1", {"opcode": 208, "modrm": 56, "expected_length": 2}),
        ("Eb CL", {"opcode": 210, "modrm": 56, "expected_length": 2}),
        ("Eb 1", {"opcode": 208, "modrm": 56, "expected_length": 2}),
        ("Eb CL", {"opcode": 210, "modrm": 56, "expected_length": 2}),
    ],
    "SAR16": [
        ("Ev 1", {"opcode": 209, "modrm": 56, "expected_length": 4}),
        ("Ev 1", {"opcode": 209, "modrm": 56, "expected_length": 4}),
        ("Ev 1", {"opcode": 209, "modrm": 56, "expected_length": 2}),
        ("Ev CL", {"opcode": 211, "modrm": 56, "expected_length": 2}),
    ],
    "NOT8": [("Eb", {"opcode": 246, "modrm": 16, "expected_length": 5})],
    "NOT16": [("Ev", {"opcode": 247, "modrm": 16, "expected_length": 6})],
    "NEG8": [("Eb", {"opcode": 246, "modrm": 24, "expected_length": 5})],
    "NEG16": [("Ev", {"opcode": 247, "modrm": 24, "expected_length": 6})],
    "MUL8": [("Eb", {"opcode": 246, "modrm": 32, "expected_length": 5})],
    "MUL16": [("Ev", {"opcode": 247, "modrm": 32, "expected_length": 6})],
    "IMUL8": [("Eb", {"opcode": 246, "modrm": 40, "expected_length": 5})],
    "IMUL16": [("Ev", {"opcode": 247, "modrm": 40, "expected_length": 6})],
    "DIV8": [("Eb", {"opcode": 246, "modrm": 48, "expected_length": 5})],
    "DIV16": [("Ev", {"opcode": 247, "modrm": 48, "expected_length": 6})],
    "IDIV8": [("Eb", {"opcode": 246, "modrm": 56, "expected_length": 5})],
    "IDIV16": [("Ev", {"opcode": 247, "modrm": 56, "expected_length": 6})],
}
