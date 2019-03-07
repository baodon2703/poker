import random

cardNum = 13;
rank = ["A", "K", "Q", "J", "T", "9", "8", "7", "6", "5", "4", "3", "2"]

weight = [[6, 4, 4, 4, 4, 4, 4],
          [6, 4, 4, 4, 4, 4, 4]]

def init():
    matrix = [[0 for x in range(cardNum)] for y in range(cardNum)]
    cardList = []
    for i in range(cardNum):
        for j in range(cardNum):
            if i < j:
                matrix[i][j] = rank[i] + rank[j] + "s"
            elif i > j:
                matrix[i][j] = rank[j] + rank[i] + "o"
            else:
                matrix[i][j] = rank[j] + rank[i]
            cardList.append(matrix[i][j])
    return matrix, cardList

def print_card_in_matrix(card, matrix):
    for i in range(cardNum):
        for j in range(cardNum):
            if card == matrix[i][j]:
                print "\033[1;31;40m" + card + "\033[0;37;40m",
            else:
                print matrix[i][j],
        print ""

def choose_random_hand(card_list):
    return random.choice(card_list)

def read_hand(filename):
    f = open(filename, "r")
    card_string = f.read()
    return [x.strip() for x in card_string.split(",")]

def isPair(cards):
    return cards[0] == cards[1]

def validate(cards):
    if isPair(cards) and len(cards) > 2:
        raise ValueError(cards + " pair cannot suit/offsuit")

    if not isPair(cards) and len(cards) == 2:
        raise ValueError(cards + " not pair card and must have suit/offsuit value")

def gen_connector(first_cards, last_cards):
    first_cards1 = rank.index(first_cards[0])
    first_cards2 = rank.index(first_cards[1])

    last_cards1 = rank.index(last_cards[0])
    last_cards2 = rank.index(last_cards[1])

    if (first_cards2 - first_cards1) != (last_cards2 - last_cards1):
        raise ValueError("gen_connector: not same connector " + first_cards + " " + last_cards)

    offsuit = ""
    if len(first_cards) > 2:
        if first_cards[2] != last_cards[2]:
            raise ValueError("gen_connector: offsuit not same for first and last card " + first_cards + " " + last_cards)
        offsuit = first_cards[2]

    result = []
    result.append(first_cards)
    while first_cards1 != last_cards1:
        first_cards1 -= 1
        first_cards2 -= 1
        result.append(rank[first_cards1] + rank[first_cards2] + offsuit)
    return result

def gen_flat(first_cards, last_cards):
    first_cards1 = rank.index(first_cards[0])
    first_cards2 = rank.index(first_cards[1])

    last_cards1 = rank.index(last_cards[0])
    last_cards2 = rank.index(last_cards[1])

    offsuit = ""
    if len(first_cards) > 2:
        if first_cards[2] != last_cards[2]:
            raise ValueError("gen_flat: offsuit not same for first and last card " + first_cards + " " + last_cards)
        offsuit = first_cards[2]

    result = []
    result.append(first_cards)
    while first_cards2 != last_cards2:
        first_cards2 -= 1
        if first_cards1 == first_cards2:
            break;
        else:
            result.append(rank[first_cards1] + rank[first_cards2] + offsuit)
    return result

def generate_range_card(card_string):
    result = []

    isSingleCard = card_string.find('-') == -1

    if isSingleCard:
        result.append(card_string)
        return result

    cards = [x.strip() for x in card_string.split('-')]
    first_card = cards[0]
    last_card = cards[1]

    validate(first_card)
    validate(last_card)

    if first_card[0] == last_card[0]:
        return gen_flat(cards[0], cards[1])
    else:
        return gen_connector(cards[0], cards[1])

def generate_range_list(card_list):
    append_list = []
    for card in card_list:
        append_list.append(generate_range_card(card))

    # SET
    # result = set()
    # for sublist in append_list:
    #     for item in sublist:
    #         result.add(item)

    # return list(result)

    result = []
    for sublist in append_list:
        for item in sublist:
            result.append(item)

    return result

matrix, all_card_list = init()
readResult = read_hand("openrange.txt")
learn_range_list = generate_range_list(readResult)

while True:
    random_hand = choose_random_hand(all_card_list)
    print "\n============"
    print "Should you open-raise? " + random_hand

    answer = raw_input("y/n?: ")
    if (answer == "y" and random_hand in learn_range_list) or (answer == "n" and random_hand not in learn_range_list):
        print "\033[1;31;40mCorrect \033[0;37;40m"
    else:
        print "\033[1;36;40mWell, learn again dude \033[0;37;40m"

    print_card_in_matrix(random_hand, matrix)
