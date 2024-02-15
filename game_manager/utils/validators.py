from django.core.exceptions import ValidationError

# Assuming this is your modified validate_bet function that expects an integer
def validate_bet(value):
    allowed_bets = {10, 25, 50, 75, 100}  # Set of allowed bet values
    if value not in allowed_bets:
        raise ValidationError(f"{value} is not a valid bet amount. Allowed values are {sorted(allowed_bets)}.")

def validate_user_bank(session, bet_amount):
    if session.bank < bet_amount:
        raise ValidationError(f"Not enough funds in bank. Remaining: {session.bank}")