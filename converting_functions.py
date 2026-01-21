
def get_bit(number: int, position: int):
    return (number // 2**position) % 2


def from_twos_complement(num: int, bits: int) -> int:
    if num >= 2 ** (bits - 1):
        num -= 2 ** bits
    return num


def to_twos_complement(num: int, bits: int) -> int:
    if num < 0:
        num += 2 ** bits
    return num
