from dataclasses import dataclass, field


@dataclass
class Card():
    """
    Represents a single card
    """
    name: str
    power: int
    suit: str
    
    def get_naming(self) -> str:
        return self.name + self.suit
    
    @staticmethod
    def get_power(card: str) -> int:
        lst = ["A", "2", "3", "4", "5", "6",
               "7", "8", "9", "10", "J", "Q", "K"]
        for i in range(len(lst)):
            if lst[i] == card:
                return i
        return -1


@dataclass
class CardDeck():
    """
    Represents a card deck with multiple cards
    """
    cards: list[Card]
    
    def add(self, card: Card) -> None:
        # add and keep order by power
        index = 0
        while index < len(self.cards) and self.cards[index].power < card.power:
            index += 1
        self.cards.insert(index, card)
    
    def remove(self, card: Card) -> None:
        self.cards.remove(card)

    def get_cards_to_beat(self, card: Card) -> list:
        ret = []
        for beat_opt in self.cards:
            if beat_opt.power >= card.power:
                ret.append(beat_opt)
        return ret

    def is_empty(self) -> bool:
        return len(self.cards) == 0

    def card_index(self, card) -> int:
        left = 0
        right = len(self.cards) - 1
        while left <= right:
            mid = (left + right) // 2

            if self.cards[mid] == card:
                return mid
            elif self.cards[mid] < card:
                left = mid + 1
            else:
                right = mid - 1
        return -1


@dataclass
class Player():
    """
    Represents a single player
    """
    card_deck: CardDeck

    def play(self, last_played: Card) -> list[Card]:
        if last_played == None:
            played_cards = self.card_deck.get_cards_to_beat(Card("", 0, ""))
        else:
            played_cards = self.card_deck.get_cards_to_beat(last_played)
        for card in played_cards:
            self.card_deck.remove(card)
        return played_cards

    def buy_cards(self, cards: list[Card]):
        for card in cards:
            self.card_deck.add(card)

    def doubt(self, played_cards) -> bool:
        for card in played_cards:
            if self.card_deck.card_index(card) == -1:
                return False
        return True

    def print_cards(self) -> None:
        print("Mão: " + " ".join([card.get_naming() for card in self.card_deck.cards]))


@dataclass
class Game():
    """
    Represents the main game
    """
    players: list[Player]
    doubt_interval: int
    stack: list[Card] = field(init=False)

    def play(self) -> list[Card]:
        self.stack = []
        num_of_plays = 0
        for i in range(len(self.players)):
            if self.someboy_won():
                break
            self.print_status()
            played_cards = self.players[i].play(None if len(self.stack) == 0 else self.stack[-1])
            print(f"[Jogador {i + 1}] {len(played_cards)} carta(s) {played_cards[0].name}")
            for card in played_cards:
                self.stack.append(card)
            if num_of_plays + 1 % self.doubt_interval == 0:
                if not self.player[i].doubt():
                    self.player[i].buy_cards(self.stack)
            if i == len(self.players) - 1:
                i = 0
            num_of_plays += 1

    def someboy_won(self):
        return any([player for player in self.players if player.card_deck.is_empty()])

    def print_status(self):
        for i in range(len(self.players)):
            print("Jogador " + str(i + 1))
            self.players[i].print_cards()
        print("Pilha: " + " ".join([card.get_naming() for card in self.stack]))


def main():
    J = int(input())
    players = []
    for _ in range(J):
        card_deck = CardDeck([])
        hand = input().split(", ")
        for card in hand:
            card_deck.add(Card(card[0], Card.get_power(card[0]), card[1]))
        players.append(
            Player(card_deck))
    N = int(input())
    Game(players, N).play()


if __name__ == "__main__":
    main()
