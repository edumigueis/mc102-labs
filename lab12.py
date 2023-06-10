from dataclasses import dataclass, field


@dataclass
class Card():
    """Represents a single card"""
    name: str
    power: int
    suit: str

    def get_naming(self) -> str:
        return self.name + self.suit

    def get_comparable(self) -> tuple:
        return (self.power, self.suit, self.name)

    @staticmethod
    def get_power(card: str) -> int:
        lst = ["A", "2", "3", "4", "5", "6",
               "7", "8", "9", "10", "J", "Q", "K"]
        for i in range(len(lst)):
            if lst[i] == card:
                return i
        return -1

    @staticmethod
    def get_suit_power(suit: str) -> int:
        lst = ["O", "E", "C", "P"]
        for i in range(len(lst)):
            if lst[i] == suit:
                return i
        return -1

    def compare_to(self, other) -> int:
        """
        Compares first by power than by suit
        Negative if smaller, positive if greater and zero if equal
        """
        if self.power != other.power:
            return self.power - other.power
        return Card.get_suit_power(self.suit) - Card.get_suit_power(other.suit)


@dataclass
class CardDeck():
    """Represents a card deck with multiple cards"""
    cards: list[Card]
    played_cards: list[Card] = field(default_factory=list)

    def add(self, card: Card) -> None:
        # add and keep order by power
        index = 0
        while (index < len(self.cards)
               and (self.cards[index].power > card.power
                    or (self.cards[index].power == card.power
                    and Card.get_suit_power(self.cards[index].suit)
                    > Card.get_suit_power(card.suit)))):
            index += 1
        self.cards.insert(index, card)

    def add_played_card(self, card: Card) -> None:
        self.played_cards.append(card)

    def sort_played_cards(self) -> None:
        n = len(self.played_cards)
        for i in range(n - 1):
            for j in range(0, n - i - 1):
                card = self.played_cards[j]
                next_card = self.played_cards[j + 1]
                is_greater = card.power > next_card.power
                has_same_power = card.power == next_card.power
                greater_suit = Card.get_suit_power(
                    card.suit) > Card.get_suit_power(next_card.suit)
                if is_greater or (has_same_power and greater_suit):
                    self.played_cards[j], self.played_cards[
                        j + 1] = next_card, card

    def remove(self, card: Card) -> None:
        self.cards.remove(card)

    def get_cards_to_beat(self, card: Card) -> tuple:
        """
        Gets the card that beats current pile top,
        and if not possible lies in game
        """
        counts: dict = {}
        for i in range(len(self.cards) - 1, -1, -1):
            counts.setdefault(self.cards[i].power, []).append(self.cards[i])

        for power, cards in counts.items():
            if power >= card.power:
                return (cards, cards)

        for power, cards in counts.items():
            if cards != []:
                return (cards, [Card(card.name, card.power, c.suit)
                                for c in cards])

        return ()

    def is_empty(self) -> bool:
        return len(self.cards) == 0

    def was_card_used(self, card: Card) -> bool:
        """Verifies if a card was used using binary search"""
        left = 0
        right = len(self.played_cards) - 1

        while left <= right:
            mid = (left + right) // 2
            comparison = self.played_cards[mid].compare_to(card)
            if comparison == 0:
                return True
            elif comparison < 0:
                left = mid + 1
            else:
                right = mid - 1

        return False


@dataclass
class Player():
    """Represents a single player"""
    card_deck: CardDeck

    def play(self, last_played: Card) -> tuple:
        if last_played is None:
            played_cards = self.card_deck.get_cards_to_beat(Card("", 0, ""))
        else:
            played_cards = self.card_deck.get_cards_to_beat(last_played)
        for card in played_cards[0]:
            self.card_deck.remove(card)
        for card in played_cards[0]:
            self.card_deck.add_played_card(card)
        return played_cards

    def buy_cards(self, cards: list[Card]) -> None:
        for card in cards:
            self.card_deck.add(card)

    def doubt(self, played_cards: list[Card]) -> bool:
        """
        Used to verify if the doubt raised by another player verifies or not
        Returns True if all cards match and False otherwise
        """
        self.card_deck.sort_played_cards()
        for card in played_cards:
            if not self.card_deck.was_card_used(card):
                return False
        return True

    def print_cards(self) -> None:
        print(
            f"Mão:{' ' if not self.card_deck.is_empty() else ''}{' '.join([card.get_naming() for card in self.card_deck.cards])}")


@dataclass
class Game():
    """Represents the main game"""
    players: list[Player]
    doubt_interval: int
    stack: list[Card] = field(init=False)

    def play(self) -> None:
        """Main loop(runs until someone wins)"""
        self.stack = []
        num_of_plays = 0
        print_players = True
        curr = 0

        while self.get_winner() == -1:
            self.print_status(players=print_players)
            print_players = False

            played_cards = self.players[curr].play(
                self.stack[-1][1] if self.stack else None)
            num_played_cards = len(played_cards[1])
            print(
                f"[Jogador {curr + 1}] {num_played_cards} carta(s) {played_cards[1][0].name}")
            self.stack.extend(zip(*played_cards))

            if (num_of_plays + 1) % self.doubt_interval == 0:
                self.print_status(players=False)
                next_player_index = curr + 2 if curr + \
                    2 <= len(self.players) else 1
                print(f"Jogador {next_player_index} duvidou.")
                if not self.players[curr].doubt(played_cards[1]):
                    player_to_buy = curr
                else:
                    player_to_buy = curr + \
                        1 if curr < len(self.players) - 1 else 0

                self.players[player_to_buy].buy_cards(
                    [card[0] for card in self.stack[:-num_played_cards]]
                    + played_cards[0])
                self.stack = []
                print_players = True

            curr = (curr + 1) % len(self.players)
            num_of_plays += 1

        self.print_status(players=print_players)
        winner = self.get_winner()
        print(f"Jogador {winner} é o vencedor!")

    def get_winner(self):
        """Winner has no cards left"""
        for i, player in enumerate(self.players, 1):
            if player.card_deck.is_empty():
                return i
        return -1

    def print_status(self, players=False):
        if players:
            for i, player in enumerate(self.players):
                print(f"Jogador {i + 1}")
                player.print_cards()

        stack_cards = [card[0].get_naming() for card in self.stack]
        print(f"Pilha:{' ' if self.stack else ''}{' '.join(stack_cards)}")


def main():
    players = []
    for _ in range(int(input())):
        card_deck = CardDeck([])
        hand = input().split(", ")
        for card in hand:
            if len(card) == 3:
                name, suit = card[0] + card[1], card[2]
            else:
                name, suit = card[0], card[1]
            card_deck.add(Card(name, Card.get_power(name), suit))
        players.append(
            Player(card_deck))
    Game(players, int(input())).play()


if __name__ == "__main__":
    main()
