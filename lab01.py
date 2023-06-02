class RoundPick:
    def __init__(self, name, index, beats):
        self.name = name
        self.index = index
        self.beats = beats


possible_plays = [
    RoundPick("TESOURA", 0, [3, 1]),
    RoundPick("PAPEL", 1, [4, 2]),
    RoundPick("PEDRA", 2, [3, 0]),
    RoundPick("LAGARTO", 3, [4, 1]),
    RoundPick("SPOCK", 4, [0, 2])
]


def get_play(play_name):
    for play in possible_plays:
        if play.name == play_name:
            return play


sheila_pick = get_play(input().upper())
reginaldo_pick = get_play(input().upper())

if reginaldo_pick.index in sheila_pick.beats and sheila_pick.index not in reginaldo_pick.beats:
    print("Interestelar")
elif sheila_pick.index in reginaldo_pick.beats and reginaldo_pick.index not in sheila_pick.beats:
    print("Jornada nas Estrelas")
else:
    print("empate")
