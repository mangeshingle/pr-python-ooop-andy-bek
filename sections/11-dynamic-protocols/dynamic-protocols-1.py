import random


class PlayingCard:
    ALLOWED_SUITS = ("spades", "diamonds", "clubs", "hearts")
    ALLOWED_RANKS = (
        "ace",
        "2",
        "3",
        "4",
        "5",
        "6",
        "7",
        "8",
        "9",
        "10",
        "jack",
        "queen",
        "king",
    )

    def __new__(cls, suit, rank):
        instance = super().__new__(cls)
        if (
            suit is None
            or rank is None
            or str(suit).strip().lower() not in PlayingCard.ALLOWED_SUITS
            or str(rank).strip().lower() not in PlayingCard.ALLOWED_RANKS
        ):
            return None
        return instance

    def __init__(self, suit, rank):
        self.suit = suit
        self.rank = rank

    def __repr__(self):
        return f"{self.__class__.__name__}(suit='{self.suit}', rank='{self.rank}')"

    def __eq__(self, other):
        if type(other) is not PlayingCard:
            return False

        if (
            self.suit is None
            or self.rank is None
            or other.suit is None
            or other.rank is None
        ):
            return False

        if self.suit == other.suit and self.rank == other.rank:
            return True
        return False

    @property
    def suit(self):
        return self._suit

    @suit.setter
    def suit(self, value):
        if value is not None:
            standardized_suit = str(value).strip().lower()
            self._suit = (
                standardized_suit
                if standardized_suit in PlayingCard.ALLOWED_SUITS
                else None
            )
        if self._suit is None or value is None:
            raise ValueError(
                f"Wrong suit value is provided. Allowed suit values are : {PlayingCard.ALLOWED_SUITS}"
            )

    @property
    def rank(self):
        return self._rank

    @rank.setter
    def rank(self, value):
        if value is not None:
            standardized_rank = str(value).strip().lower()
            self._rank = (
                standardized_rank
                if standardized_rank in PlayingCard.ALLOWED_RANKS
                else None
            )
        if self._rank is None or value is None:
            raise ValueError(
                f"Wrong rank value is provided. Allowed rank values are : {PlayingCard.ALLOWED_RANKS}"
            )


class CardDeck(object):
    def __init__(self, cards=None):
        self.cards = cards
        self.idx = 0

    def _get_transient_instance(self):
        cls = type(self)
        transient_object = cls()
        transient_object._cards = []
        return transient_object

    def __repr__(self):
        return f"{self.__class__.__name__}(cards={self.cards})"

    def __add__(self, other):
        match other.__class__:
            case cls if cls is self.__class__:
                transient_card_deck = self._get_transient_instance()
                transient_card_deck._cards.extend(self._cards)
                transient_card_deck._cards.extend(other._cards)
                return transient_card_deck
            case cls if cls is PlayingCard:
                transient_card_deck = self._get_transient_instance()
                transient_card_deck._cards.extend(self._cards)
                transient_card_deck._cards.append(other)
                return transient_card_deck
            case _:
                return NotImplemented

    def __radd__(self, other):
        return self.__add__(other)

    def __mul__(self, other):
        match other:
            case cls if isinstance(cls, int):
                transient_card_deck = self._get_transient_instance()
                if other < 1:
                    raise ValueError(f"Multiplication by {other} is not allowed.")
                for playing_card in self._cards:
                    for _ in range(0, other):
                        duplicate_playing_card = PlayingCard(
                            suit=playing_card.suit, rank=playing_card.rank
                        )
                        transient_card_deck._cards.append(duplicate_playing_card)
                return transient_card_deck
            case _:
                return NotImplemented

    def __rmul__(self, other):
        return self.__mul__(other)

    def __len__(self):
        return len(self._cards)

    def __contains__(self, value):
        return value in self._cards

    def __getitem__(self, key):
        match key:
            case idx if type(idx) is int:
                return self._cards[key]
            case idx if type(idx) is slice:
                transient_card_deck = self._get_transient_instance()
                for playing_card in self._cards[idx]:
                    transient_card_deck._cards.append(playing_card)
                return transient_card_deck
            case _:
                raise NotImplementedError

    def __iter__(self):
        return self

    def __next__(self):
        try:
            self.idx += 1
            return self._cards[self.idx - 1]
        except IndexError:
            self.idx = 0
            raise StopIteration

    def draw(self, n):
        no_of_cards = len(self._cards)
        if type(n) is not int:
            raise ValueError("Please provide integer value.")

        if n > len(self._cards):
            raise ValueError(
                f"Not enough cards in the deck. Current card size is: {no_of_cards}"
            )

        if n == 1:
            random_index = random.choice(range(0, no_of_cards))
            playing_card = self._cards[random_index]
            del self._cards[random_index]
            return playing_card
        else:
            random_indices = random.sample(range(0, no_of_cards), n)
            transient_card_deck = self._get_transient_instance()
            for idx in random_indices:
                playing_card = self._cards[idx]
                transient_card_deck._cards.append(playing_card)
                del self._cards[idx]
            return transient_card_deck

    @property
    def cards(self):
        return self._cards

    @cards.setter
    def cards(self, value):
        self._cards: list[PlayingCard] = []
        match value:
            case x if x is None:
                self._cards = []
            case x if isinstance(x, list):
                for item in x:
                    if type(item) is PlayingCard:
                        self._cards.append(item)
            case _:
                self._cards = []

        if len(self._cards) == 0:
            for suit in PlayingCard.ALLOWED_SUITS:
                for rank in PlayingCard.ALLOWED_RANKS:
                    playing_card = PlayingCard(suit=suit, rank=rank)
                    self._cards.append(playing_card)
