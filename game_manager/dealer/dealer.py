import random


from models import Game

CARD_VALUE = {
    '2': 2, '3': 3, '4': 4, '5': 5, '6': 6, '7': 7, '8': 8, '9': 9, '10': 10,
    'J': 10, 'Q': 10, 'K': 10, 'A': [1, 11]
}


def start_game(hand: list, game_cards:list):
    """
    adding 2 cards to the passed hand
    """
    first_card = random.choice(game_cards)
    hand.append(first_card)
    game_cards.remove(first_card)

    second_card = random.choice(game_cards)
    hand.append(second_card)
    game_cards.remove(second_card)

def hit(hand: list, game_cards: list):
    card = random.choice(game_cards)
    hand.append(card)
    game_cards.remove(card)


def count_score(hand: list):
    score = 0
    num_aces = 0
    for card in hand:
        if card != 'A':
            score += CARD_VALUE[card]
        else: 
            num_aces += 1
    
    # Add Aces to the score, treating them optimally as either 1 or 11
    if num_aces > 0:
        for _ in range(num_aces):
            # Add 11 if it won't bust the hand, otherwise add 1
            if score + 11 <= 21:
                score += 11
            else:
                score += 1
        
        while score > 21 and num_aces > 0:
            score -= 10
            num_aces -= 1

    return score


def play_dealer_hand(game: Game):
    dealer_score = count_score(game.dealer_hand)
    while dealer_score <= 16:
        hit(hand=game.dealer_hand, game_cards=game.get_deck())
        game.save()
        dealer_score = count_score(game.dealer_hand)


def check_if_burst(score: int) -> bool:
    """
    check the score after each hit
    """
    burst = False
    if score > 21:
        burst = True
    return burst

def evaluate(game: Game) ->int:
    """
    evaluate after stand 
    it returns [0, 1, 2]
    0 user lose
    1 user wins 
    2 tie
    """
    dealer_score = count_score(hand=game.dealer_hand)
    player_score = count_score(hand=game.player_hand)

    diff = dealer_score - player_score
    if player_score > 21:
        return 0
    elif player_score == dealer_score:
        return 2
    elif diff > 0 and dealer_score < 22:
        return 0
    else:
        return 1

