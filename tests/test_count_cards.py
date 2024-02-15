import pytest

CARD_VALUE = {
    '2': 2, '3': 3, '4': 4, '5': 5, '6': 6, '7': 7, '8': 8, '9': 9, '10': 10,
    'J': 10, 'Q': 10, 'K': 10, 'A': 11
}

def count_score(hand: list):
    score = 0
    num_aces = 0

    for card in hand:
        if card != 'A':
            score += CARD_VALUE[card]
        else:
            num_aces += 1

    
    for _ in range(num_aces):
        if score + 11 <= 21:
            score += 11
        else:
            score += 1

    while score > 21 and num_aces > 0:
        score -= 10
        num_aces -= 1

    return score

@pytest.mark.parametrize("hand, expected_score", [
    (['2', '3', '4'], 9),           # No Aces, simple sum
    (['2', '3', 'A'], 16),          # One Ace, treated as 11
    (['A', 'A'], 12),               # Two Aces, one treated as 11, other as 1
    (['A', 'A', '9'], 21),          # Two Aces, one treated as 11, other as 1, reaching 21
    (['10', 'A'], 21),              # Blackjack with Ace
    (['2', 'A', 'K'], 13),          # Blackjack with Ace counted as 11
    (['9', 'A', 'A'], 21),          # Aces considered as 1 and 11, reaching 21
    (['10', '10', 'A'], 21),        # Aces considered as 1 and 11, reaching 21
    (['10', '10', '10'], 30),       # Bust
    (['A', 'A', 'A', 'A'], 14),
    (['9', 'A', 'A', 'A', 'A'], 13),
    (['A', '7'], 18),
])

def test_count_score(hand, expected_score):
    assert count_score(hand) == expected_score