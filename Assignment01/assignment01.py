from enum import Enum
import copy


def main():
    test_card()
    test_hand()


class Card:
    class CardSuit(Enum):
        SPADES = 1
        HEARTS = 2
        CLUBS = 3
        DIAMONDS = 4

        def __str__(self):
            ret_str = self.name[0].upper() + self.name[1:].lower()
            return ret_str

    class CardValue(Enum):
        ACE = 1
        TWO = 2
        THREE = 3
        FOUR = 4
        FIVE = 5
        SIX = 6
        SEVEN = 7
        EIGHT = 8
        NINE = 9
        TEN = 10
        JACK = 11
        QUEEN = 12
        KING = 13

        def __str__(self):
            ret_str = self.name[0].upper() + self.name[1:].lower()
            return ret_str

    DEFAULT_VAL = CardValue.ACE
    DEFAULT_SUIT = CardSuit.HEARTS

    val = 0
    suit = 0
    error_flag = False

    def __init__(self, val = DEFAULT_VAL, suit = DEFAULT_SUIT):
        self.set(val, suit)

    def __str__(self):
        if self.error_flag:
            return "[invalid]"
        return "{0} of {1}".format(self.val, self.suit)

    def set(self, val, suit):
        if self.valid_card(val, suit):
            self.val = val
            self.suit = suit
            self.error_flag = False
        else:
            self.error_flag = True

    def get_val(self):
        return self.val

    def get_suit(self):
        return self.suit

    def get_error_flag(self):
        return self.error_flag

    def equals(self, other_card):
        if (other_card.get_val() == self.val and
                other_card.get_suit() == self.suit and
                other_card.get_error_flag() == self.error_flag):
            return True
        return False

    @staticmethod
    def valid_card(value, suit):
        if value in Card.CardValue and suit in Card.CardSuit:
            return True
        return False


class Hand:
    MAX_CARDS_PER_HAND = 50

    my_cards = []
    num_cards = 0

    def __init__(self):
        def reset_hand():
            self.my_cards = []
            self.num_cards = 0

        reset_hand()

    def take_card(self, card):
        self.num_cards += 1
        if self.num_cards >= self.MAX_CARDS_PER_HAND:
            return False
        else:
            if not card.get_error_flag():
                self.my_cards.append(card)
                return True

    def play_card(self):
        self.num_cards -= 1
        if not self.my_cards or self.num_cards == 0:
            return None
        else:
            return self.my_cards.pop(0)

    def __str__(self):
        for x in range(len(self.my_cards)):
            card_string = "{0} of {1}". \
                format(self.my_cards[x].get_val(),
                       self.my_cards[x].get_suit())
            print(card_string)
        return ''

    def get_num_cards(self):
        return self.num_cards

    def inspect_card(self, k):
        temp = copy.deepcopy(self.my_cards)
        if k < 0 or k > 50:
            bad = Card()
            bad.set(1, 1)
            return bad
        else:
            return temp[k]


def test_card():
    card1 = Card()
    card2 = Card(Card.CardValue.JACK, Card.CardSuit.CLUBS)
    card3 = Card(0, 0)
    print("First display")
    print('{0} \n{1} \n{2}'.format(card1, card2, card3))
    card3.set(Card.CardValue.TWO, Card.CardSuit.DIAMONDS)
    card2.set(0, 0)
    print("Second display")
    print('{0} \n{1} \n{2}\n'.format(card1, card2, card3))


def test_hand():
    hand = Hand()
    card1 = Card(Card.CardValue.ACE, Card.CardSuit.SPADES)
    card2 = Card(Card.CardValue.TEN, Card.CardSuit.HEARTS)
    card3 = Card(Card.CardValue.KING, Card.CardSuit.DIAMONDS)
    card4 = Card(Card.CardValue.EIGHT, Card.CardSuit.CLUBS)
    card5 = Card(0, 0)
    cards = [card1, card2, card3, card4, card5]
    i = 0
    print("hand before deal")
    print("Hand = (  {0}  )".format(hand))
    print("num cards = {0}\n".format(hand.get_num_cards()))
    while hand.take_card(cards[i]):
        i += 1
        if i == 4:
            i = 0
    print("take_card() finished: filled to max with only valid cards and returned True\n\nHand full\n")
    print("Hand after deal")
    print(hand)
    print("num cards = {0}\n".format(hand.get_num_cards()))
    print("inspecting 5th card")
    print(hand.inspect_card(4))
    print("test bad input value")
    print(hand.inspect_card(100))
    print("test another bad input value")
    print(hand.inspect_card(-100))
    print("test equals() method")
    print(card1.equals(card1))
    print("test equals() method again")
    print(card1.equals(card2), "\n")
    print("Play cards")
    while hand.get_num_cards() > 1:
        print(hand.play_card())
    print("\nHand = (  {0}  )".format(hand))


if __name__ == "__main__":
    main()

""" ------------------ run of main client ---------------------------
DeprecationWarning: using non-Enums in containment checks will raise TypeError in Python 3.8
  if value in Card.CardValue and suit in Card.CardSuit:
First display
Ace of Hearts 
Jack of Clubs 
[invalid]
Second display
Ace of Hearts 
[invalid] 
Two of Diamonds

hand before deal
Hand = (    )
num cards = 0

take_card() finished: filled to max with only valid cards and returned True

Hand full

Hand after deal
Ace of Spades
Ten of Hearts
King of Diamonds
Eight of Clubs
Ace of Spades
Ten of Hearts
King of Diamonds
Eight of Clubs
Ace of Spades
Ten of Hearts
King of Diamonds
Eight of Clubs
Ace of Spades
Ten of Hearts
King of Diamonds
Eight of Clubs
Ace of Spades
Ten of Hearts
King of Diamonds
Eight of Clubs
Ace of Spades
Ten of Hearts
King of Diamonds
Eight of Clubs
Ace of Spades
Ten of Hearts
King of Diamonds
Eight of Clubs
Ace of Spades
Ten of Hearts
King of Diamonds
Eight of Clubs
Ace of Spades
Ten of Hearts
King of Diamonds
Eight of Clubs
Ace of Spades
Ten of Hearts
King of Diamonds
Eight of Clubs
Ace of Spades
Ten of Hearts
King of Diamonds
Eight of Clubs
Ace of Spades
Ten of Hearts
King of Diamonds
Eight of Clubs
Ace of Spades

num cards = 50

inspecting 5th card
Ace of Spades
test bad input value
[invalid]
test another bad input value
[invalid]
test equals() method
True
test equals() method again
False 

Play cards
Ace of Spades
Ten of Hearts
King of Diamonds
Eight of Clubs
Ace of Spades
Ten of Hearts
King of Diamonds
Eight of Clubs
Ace of Spades
Ten of Hearts
King of Diamonds
Eight of Clubs
Ace of Spades
Ten of Hearts
King of Diamonds
Eight of Clubs
Ace of Spades
Ten of Hearts
King of Diamonds
Eight of Clubs
Ace of Spades
Ten of Hearts
King of Diamonds
Eight of Clubs
Ace of Spades
Ten of Hearts
King of Diamonds
Eight of Clubs
Ace of Spades
Ten of Hearts
King of Diamonds
Eight of Clubs
Ace of Spades
Ten of Hearts
King of Diamonds
Eight of Clubs
Ace of Spades
Ten of Hearts
King of Diamonds
Eight of Clubs
Ace of Spades
Ten of Hearts
King of Diamonds
Eight of Clubs
Ace of Spades
Ten of Hearts
King of Diamonds
Eight of Clubs
Ace of Spades

Hand = (    )

------------------------------------------------------------------- """
