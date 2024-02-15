import pytest

def evaluate(player_score: int, dealer_score: int):
    """
    Evaluate after each hit.
    Returns:
        0: User loses.
        1: User wins.
        2: Tie.
    """
    diff = dealer_score - player_score
    if player_score > 21:
        return 0
    elif player_score == dealer_score:
        return 2
    elif diff > 0 and dealer_score < 22:
        return 0
    else:
        return 1

# Define test cases
@pytest.mark.parametrize("player_score, dealer_score, expected_result", [
    (20, 18, 1),    # Player wins
    (20, 21, 0),    # Player loses, dealer has higher score
    (15, 15, 2),    # Tie
    (22, 20, 0),    # Player busts
    (18, 22, 1),    # Dealer busts, player wins
    (25, 25, 0),    # Both bust
    (18, 17, 1),    
])

def test_evaluate(player_score, dealer_score, expected_result):
    assert evaluate(player_score, dealer_score) == expected_result