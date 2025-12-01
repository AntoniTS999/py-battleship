from typing import Tuple, Dict, List, Optional


class Deck:
    def __init__(self, row: int, column: int, is_alive: bool = True) -> None:
        self.row: int = row
        self.column: int = column
        self.is_alive: bool = is_alive


class Ship:
    def __init__(self,
                 start: Tuple[int, int],
                 end: Tuple[int, int],
                 is_drowned: bool = False) -> None:
        self.is_drowned: bool = is_drowned
        self.decks: List[Deck] = []

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

    def get_deck(self, row: int, column: int) -> Optional[Deck]:
        for deck in self.decks:
            if deck.row == row and deck.column == column:
                return deck
        return None

    def fire(self, row: int, column: int) -> str:
        deck: Optional[Deck] = self.get_deck(row, column)
        if deck is None:
            return "Miss!"

        if not deck.is_alive:
            if self.is_drowned:
                return "Sunk!"
            return "Hit!"

        deck.is_alive = False

        if all(not d.is_alive for d in self.decks):
            self.is_drowned = True
            return "Sunk!"

        return "Hit!"


class Battleship:
    def __init__(self,
                 ships: List[Tuple[Tuple[int, int], Tuple[int, int]]]) \
            -> None:
        self.field: Dict[Tuple[int, int], Ship] = {}
        self.ships: List[Ship] = []

        for start, end in ships:
            ship: Ship = Ship(start, end)
            self.ships.append(ship)
            for deck in ship.decks:
                self.field[(deck.row, deck.column)] = ship

        self._validate_field()

    def fire(self, location: Tuple[int, int]) -> str:
        r, c = location
        if (r, c) not in self.field:
            return "Miss!"
        ship: Ship = self.field[(r, c)]
        return ship.fire(r, c)

    # ------------------- brakujące metody -------------------

    def print_field(self) -> None:
        size: int = 10
        for ra in range(size):
            row_str: List[str] = []
            for co in range(size):
                cell: Optional[Ship] = self.field.get((ra, co))
                if cell is None:
                    row_str.append("~")
                else:
                    deck = cell.get_deck(ra, co)
                    if deck is None:
                        row_str.append("~")
                    elif deck.is_alive:
                        row_str.append("□")
                    elif not deck.is_alive and not cell.is_drowned:
                        row_str.append("*")
                    else:
                        row_str.append("x")
            print(" ".join(row_str))
        print()

    def _validate_field(self) -> None:
        # Sprawdzenie liczby statków
        if len(self.ships) != 10:
            raise ValueError("Field must contain exactly 10 ships.")

        # Sprawdzenie liczby statków wg wielkości
        sizes: List[int] = [len(ship.decks) for ship in self.ships]
        if sizes.count(1) != 4:
            raise ValueError("There must be 4 single-deck ships.")
        if sizes.count(2) != 3:
            raise ValueError("There must be 3 double-deck ships.")
        if sizes.count(3) != 2:
            raise ValueError("There must be 2 triple-deck ships.")
        if sizes.count(4) != 1:
            raise ValueError("There must be 1 four-deck ship.")

        # Sprawdzenie, czy statki się nie stykają
        occupied: set[Tuple[int, int]] = set()
        for ship in self.ships:
            for deck in ship.decks:
                r, c = deck.row, deck.column
                for dr in [-1, 0, 1]:
                    for dc in [-1, 0, 1]:
                        nr, nc = r + dr, c + dc
                        if (nr, nc) in occupied:
                            raise ValueError("Ships cannot touch each other, "
                                             "even diagonally.")
                occupied.add((r, c))
