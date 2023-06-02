from typing import Callable


def adapt_ASCII(index: int) -> str:
    if index >= 127:
        return chr(index - 95)  # starting again from 32
    else:
        if (index < 32):
            return chr(index + 32)
        else:
            return chr(index)


def decrypt(encrypted_string: str, key: int) -> str:
    ret = ""
    for char in encrypted_string:
        ret = ret + adapt_ASCII(ord(char)
                                + (key % 95))  # 95: number o readable chars
    return ret


def get_any_first_index(elements: list[str],
                        text: str,
                        out=False,
                        start=0) -> int:
    for i in range(start, len(text)):
        if out:
            if text[i] not in elements:
                return i
        else:
            if text[i] in elements:
                return i
    return -1  # not found


def get_index_by_operations(operator: str, text: str, start=0) -> int:
    nums = ["0", "1", "2", "3", "4", "5", "6", "7", "8", "9"]
    vowels = ["a", "e", "i", "o", "u", "A", "E", "I", "O", "U"]
    if operator == "vogal":
        return get_any_first_index(vowels, text, start=start)
    if operator == "consoante":
        return get_any_first_index(vowels, text, True, start=start)
    if operator == "numero":
        return get_any_first_index(nums, text, start=start)
    else:
        return get_any_first_index([operator], text, start=start)


def get_operation(operation: str) -> Callable:
    preset_ops = {'+': lambda x, y: x + y,
                  '-': lambda x, y: x - y,
                  '*': lambda x, y: x * y}
    return preset_ops[operation]


def get_key(operation: str,
            op1: str,
            op2: str,
            encrypted_lines: list[str]) -> int:
    concat_encrypted = "".join(encrypted_lines)
    index_op1 = get_index_by_operations(op1, concat_encrypted)
    index_op2 = get_index_by_operations(op2, concat_encrypted, index_op1)
    return get_operation(operation)(index_op1, index_op2)


def print_decrypted(key: int, decrypted_lines: list[str]) -> None:
    print(key)
    for decrypt in decrypted_lines:
        print(decrypt)


def main() -> None:
    operation = input()
    op1 = input()
    op2 = input()
    line_count = int(input())
    encrypted_lines = [input() for _ in range(line_count)]
    key = get_key(operation, op1, op2, encrypted_lines)
    decrypted_lines = [decrypt(encrypted, key)
                       for encrypted in encrypted_lines]
    print_decrypted(key, decrypted_lines)


main()
