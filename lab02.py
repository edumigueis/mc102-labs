class Tree:
    def __init__(self, info, children=[]):
        self.children = children
        self.info = info


def initOptionTree():
    return Tree("Seu SO anterior era Linux?", [
                Tree("Seu SO anterior era um MacOS?", [
                    Tree("Ubuntu Mate, Ubuntu Mint, Kubuntu, Manjaro."),
                    Tree("ElementaryOS, ApricityOS.")
                ]), Tree("É programador/ desenvolvedor ou de áreas semelhantes?", [
                    Tree("Ubuntu Mint, Fedora."), Tree(
                        "Gostaria de algo pronto para uso ao invés de ficar configurando o SO?", [
                            Tree("Já utilizou Arch Linux?", [
                                Tree("Antergos, Arch Linux."), Tree(
                                    "Gentoo, CentOS, Slackware.")
                            ]), Tree(
                                "Já utilizou Debian ou Ubuntu?", [
                                    Tree("OpenSuse, Ubuntu Mint, Ubuntu Mate, Ubuntu."), Tree(
                                        "Manjaro, ApricityOS.")
                                ])
                        ]),
                    Tree("Kali Linux, Black Arch."),
                ])])


root = initOptionTree()


def displayNextOption(option, node):
    if len(node.children) > 0:
        node = node.children[option]
        return node
    return None


def buildOptString(questionOrAnswer, options):
    formattedOptions = ""
    for x in range(0, len(options)):
        formattedOptions += "(" + str(x) + ") " + \
            options[x] + ("\n" if x != len(options) - 1 else "")

    return "%s\n%s" % (questionOrAnswer, formattedOptions)


def definePath(selecteOptions):
    if (selecteOptions[0] == 0):
        return "Você passará pelo caminho daqueles que decidiram abandonar sua zona de conforto, as distribuições recomendadas são: "  # motivação
    if (selecteOptions[0] == selecteOptions[len(selecteOptions) - 1]):
        return "Suas escolhas te levaram a um caminho repleto de desafios, para você recomendamos as distribuições: "  # desafio
    if (selecteOptions[0] == 1 and (selecteOptions[len(selecteOptions) - 1] == 0 or selecteOptions[len(selecteOptions) - 1] == 2)):
        return "Ao trilhar esse caminho, um novo guru do Linux irá surgir, as distribuições que servirão de base para seu aprendizado são: "  # aprendizado


def main():
    print("Este é um sistema que irá te ajudar a escolher a sua próxima Distribuição Linux. Responda a algumas poucas perguntas para ter uma recomendação.")
    current = root
    selecteOptions = []
    while current != None:
        print(buildOptString((definePath(selecteOptions) + current.info if len(current.children) == 0 else current.info), (["Não", "Sim"] if len(current.children) != 0 else []) + ([
            "Sim, realizo testes e invasão de sistemas"] if len(current.children) == 3 else [])))
        if len(current.children) != 0:
            try:
                currentOption = int(input())
                if currentOption >= len(current.children):
                    raise Exception
            except:
                print("Opção inválida, recomece o questionário.")
                break
            selecteOptions += [currentOption]
        current = displayNextOption(currentOption, current)


main()
