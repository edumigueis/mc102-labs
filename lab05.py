gene = ""


def reverse(i, j):
    return gene[0:i] + gene[i:j+1][::-1] + gene[j+1::]


def transp(i, j, k):
    return gene[0:i] + gene[j+1:k+1] + gene[i:j+1] + gene[k+1::]


def combine(g, i):
    return gene[0:i] + g + gene[i::]


def concat(g):
    return gene + g


def remove(i, j):
    return gene[0:i] + gene[j + 1::]


def transp_rev(i, j, k):
    global gene
    gene = transp(i, j, k)
    return reverse(i, k)


def search(g):
    print(gene.count(g))


def search_bi(g):
    print(gene.count(g) + reverse(0, len(gene)).count(g))


def show():
    print(gene)


def main():
    global gene
    gene = input()
    while True:
        inp = input().split(" ")
        func = inp[0]
        params = inp[1:]
        match func:
            case "reverter":
                gene = reverse(int(params[0]), int(params[1]))
            case "transpor":
                gene = transp(int(params[0]), int(params[1]), int(params[2]))
            case "combinar":
                gene = combine(params[0], int(params[1]))
            case "concatenar":
                gene = concat(params[0])
            case "remover":
                gene = remove(int(params[0]), int(params[1]))
            case "transpor_e_reverter":
                gene = transp_rev(int(params[0]), int(
                    params[1]), int(params[2]))
            case "buscar":
                search(params[0])
            case "buscar_bidirecional":
                search_bi(params[0])
            case "mostrar":
                show()
            case "sair":
                break
            case _:
                print("Opção indisponível.")


if __name__ == "__main__":
    main()
