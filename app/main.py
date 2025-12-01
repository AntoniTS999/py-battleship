class Deck:
    def __init__(self, row: int, column: int, is_alive: bool = True) -> None:
        self.row = row
        self.column = column
        self.is_alive = is_alive


class Ship:
    def __init__(self,
                 start: tuple[int],
                 end: tuple[int],
                 is_drowned: bool = False) -> None:
        self.start = start
        self.end = end
        self.is_drowned = is_drowned
        self.decks = []

        r1, c1 = start
        r2, c2 = end

        if r1 == r2:
            for col in range(min(c1, c2), max(c1, c2) + 1):
                self.decks.append(Deck(r1, col))
        elif c1 == c2:
            for row in range(min(r1, r2), max(r1, r2) + 1):
                self.decks.append(Deck(row, c1))
        else:
            raise ValueError("Ships must be horizontal or vertical")

    def get_deck(self, row: int, column: int) -> Deck | None:
        for deck in self.decks:
            if deck.row == row and deck.column == column:
                return deck
        return None

    def fire(self, row: int, column: int) -> bool:
        deck = self.get_deck(row, column)
        if deck is None:
            return "Miss!"

        if not deck.is_alive:
            if self.is_drowned:
                return "Sunk!"
            else:
                return "Hit!"

        deck.is_alive = False

        if all(not d.is_alive for d in self.decks):
            self.is_drowned = True
            return "Sunk!"
        else:
            return "Hit!"


class Battleship:
    def __init__(self, ships: list) -> None:
        self.ships = [Ship(start, end) for start, end in ships]
        self.field = {}
        for ship in self.ships:
            for deck in ship.decks:
                self.field[(deck.row, deck.column)] = ship

    def fire(self, location: tuple) -> tuple:
        r, c = location

        if (r, c) not in self.field:
            return "Miss!"

        ship = self.field[(r, c)]
        return ship.fire(r, c)
