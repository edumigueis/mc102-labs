import typing


def normalize_arrays(a: list[typing.Any],
                     b: list[typing.Any],
                     fill: typing.Any) -> None:
    if len(a) < len(b):
        a[:] = a + [fill] * (len(b) - len(a))
    else:
        b[:] = b + [fill] * (len(a) - len(b))


def soma_vetores(a: list[int], b: list[int]) -> list[int]:
    normalize_arrays(a, b, 0)
    return [a[i] + b[i] for i in range(len(a))]


def subtrai_vetores(a: list[int], b: list[int]) -> list[int]:
    normalize_arrays(a, b, 0)
    return [a[i] - b[i] for i in range(len(a))]


def multiplica_vetores(a: list[int], b: list[int]) -> list[int]:
    normalize_arrays(a, b, 1)
    return [a[i] * b[i] for i in range(len(a))]


def divide_vetores(a: list[int], b: list[int]) -> list[int]:
    if len(a) <= len(b):
        normalize_arrays(a, b, 0)
    else:
        normalize_arrays(a, b, 1)
    return [a[i] // b[i] for i in range(len(a))]


def multiplicacao_escalar(arr: list[int], n: int) -> list[int]:
    return [n * i for i in arr]


def n_duplicacao(arr: list[int], n: int) -> list[int]:
    return arr * n


def soma_elementos(arr: list[int]) -> int:
    n = 0
    for i in arr:
        n += i
    return n


def produto_interno(a: list[int], b: list[int]) -> int:
    normalize_arrays(a, b, 1)
    n = 0
    for i in range(len(a)):
        n += a[i]*b[i]
    return n


def multiplica_todos(a: list[int], b: list[int]) -> list[int]:
    ret: list[int] = []
    for i in a:
        sum = 0
        for j in b:
            sum += i*j
        ret = ret + [sum]
    return ret


def correlacao_cruzada(arr: list[int], mask: list[int]) -> list[int]:
    ret: list[int] = []
    for i in range((len(arr) - len(mask)) + 1):
        sum = 0
        for m in range(len(mask)):
            sum += arr[i + m]*mask[m]
        ret = ret + [sum]
    return ret


def main() -> None:
    arr = [int(x) for x in input().split(",")]
    while True:
        try:
            func_name = input()
            match func_name:
                case "soma_elementos":
                    arr = [soma_elementos(arr)]
                case "produto_interno":
                    arr = [produto_interno(arr, [int(x)
                                           for x in input().split(",")])]
                case "n_duplicacao":
                    arr = n_duplicacao(arr, int(input()))
                case "multiplicacao_escalar":
                    arr = multiplicacao_escalar(arr, int(input()))
                case "fim":
                    break
                case _:
                    func = globals()[func_name]
                    arr_operation = [int(x) for x in input().split(",")]
                    arr = func(arr, arr_operation)
            print(arr)
        except KeyError:
            print("Opção indisponível.")


if __name__ == "__main__":
    main()
