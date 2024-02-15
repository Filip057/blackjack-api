from django.shortcuts import get_object_or_404
from django.core.exceptions import ValidationError

from rest_framework.response import Response

from ..models import Session, Game
from ..serializers import GameSerializer
from game_manager.dealer import dealer

def get_session_and_game_ids(request):
    session_id = request.headers.get('sid')
    game_id = request.headers.get('gid')
    return session_id, game_id


def get_session_and_game(session_id, game_id):
    session = get_object_or_404(Session, session_id=session_id)
    game = get_object_or_404(Game, id=game_id, session=session)
    return session, game

def place_bet_and_start_game(game: Game, bet_amount):
    if game.bet_placed:
        raise ValidationError("Bet has already been placed for this game")
    game.bet = bet_amount
    game.bet_placed = True
    # Assuming dealer.start_game() initializes the game
    dealer.start_game(hand=game.player_hand, game_cards=game.get_deck())
    dealer.start_game(hand=game.dealer_hand, game_cards=game.get_deck())
    game.save()

def generate_bet_response(game):
    game_serializer = GameSerializer(game)
    return Response({'message': 'Bet successfully placed', 'current_game': game_serializer.data})