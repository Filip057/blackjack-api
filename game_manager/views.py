from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response


from django.http import HttpRequest
from django.shortcuts import get_object_or_404
from django.db import transaction

from .models import Session, Game
from .serializers import SessionSerializer, GameSerializer

from game_manager.dealer import dealer

import uuid

# Create your views here.

@api_view(['POST'])
def create_session(request):
    if request.method == 'POST':
        username = request.data.get('username', None)
        if username is None:
            return Response({'error': 'Username is required'}, status=status.HTTP_400_BAD_REQUEST)
        
        # Create a new session with the provided username and session id
        session_id = uuid.uuid4()
        session = Session.objects.create(username=username, session_id = session_id)
        serializer = SessionSerializer(session)
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    
@api_view(['GET'])
def start_new_game(request: HttpRequest):
    # Retrieve the session_id from URL request headers
    
    session_id = request.headers.get('sid') # If session_id is in request headers

    if session_id is None:
        return Response({'error': 'Session ID is required'}, status=status.HTTP_400_BAD_REQUEST)
    
    # Check if the session exists
    try:
        session = Session.objects.get(session_id=session_id)
    except Session.DoesNotExist:
        return Response({'error': 'Session does not exist'}, status=status.HTTP_404_NOT_FOUND)

    # Check if there is an active game for the session
    active_games = Game.objects.filter(session=session, is_over=False)
    if active_games.exists():
        # If there is an active game, return its ID
        active_game_id = active_games.first().id
        return Response({'message': 'Active game found', 'active_game_id': active_game_id}, status=status.HTTP_200_OK)

    # If no active game is found, create a new game associated with the session
    game = Game.objects.create(session=session)

    # Return the ID of the newly created game
    return Response({'message': 'New game started successfully', 'new_game_id': game.id}, status=status.HTTP_201_CREATED)

@api_view(['GET'])
def get_session_info(request):
    # Retrieve the session_id from URL request headers
    session_id = request.headers.get('sid')  # If session_id is in request headers
    

    if session_id is None:
        return Response({'error': 'Session ID is required'}, status=status.HTTP_400_BAD_REQUEST)
    
    try:
        # Retrieve the session and its associated active game (if any)
        session = Session.objects.get(session_id=session_id)
        active_game = Game.objects.filter(session=session, is_over=False).first()
        # Retrieve finished games associated with the session
        finished_games = Game.objects.filter(session=session, is_over=True)
        
        # Serialize the active game (if any)
        active_game_data = GameSerializer(active_game).data if active_game else None
        
        # Serialize the finished games
        finished_games_data = GameSerializer(finished_games, many=True).data

        # Construct the response JSON
        response_data = {
            'current_game': active_game_data,
            'finished_games': finished_games_data
        }

        return Response(response_data, status=status.HTTP_200_OK)
    
    except Session.DoesNotExist:
        return Response({'error': 'Session does not exist'}, status=status.HTTP_404_NOT_FOUND)
    

@api_view(['GET'])
def place_bet(request, bet_amount):
    session_id = request.headers.get('sid')
    game_id = request.headers.get('gid')

    bet = int(bet_amount)

    # Retrieve the session object or return 404 if not found
    session = get_object_or_404(Session, session_id=session_id)

    # Filter the Game objects associated with the session by game_id
    game = get_object_or_404(Game, id=game_id, session=session)

    # Check if the bet has already been placed for the current game
    if game.bet_placed:
        return Response({'error': 'Bet has already been placed for this game'}, status=status.HTTP_400_BAD_REQUEST)

    if not isinstance(bet, int):
        return Response({'error': 'Bet must be a number', 'possible options': [ '10', '25', '50', '75', '100']}, status=status.HTTP_400_BAD_REQUEST)

    #placing bet
    game.bet = bet
    game.bet_placed = True
    game.save()

    # adding first 2 cards 
    dealer.start_game(hand=game.player_hand, game_cards=game.get_deck())
    dealer.start_game(hand=game.dealer_hand, game_cards=game.get_deck())
    game.save()

    # Serialize the current game data
    game_serializer = GameSerializer(game)

    return Response({'message': 'Bet successfully placed', 'bet_amount': bet_amount, 'current_game': game_serializer.data})
    
@api_view(['GET'])
def hit(request):
    session_id = request.headers.get('sid')
    game_id = request.headers.get('gid')

    # Retrieve the session object or return 404 if not found
    session = get_object_or_404(Session, session_id=session_id)

    # Filter the Game objects associated with the session by game_id
    game = get_object_or_404(Game, id=game_id, session=session)

    player_hand = game.player_hand
    dealer.hit(hand=player_hand, game_cards=game.get_deck())
    game.save()

    score = dealer.count_score(game.player_hand)
    burst = dealer.check_if_burts(score=score)

    if burst:
        game.is_over = True
        game.winner = 'Dealer'
        # session.bank = bank value - game.bet
        with transaction.atomic():
            session.bank -= game.bet
            session.save()
    
    game_serializer = GameSerializer(game)
    
    return Response(data={'current_game': game_serializer.data})

@api_view(['GET'])
def stand(request):
    session_id = request.headers.get('sid')
    game_id = request.headers.get('gid')

    # Retrieve the session object or return 404 if not found
    session = get_object_or_404(Session, session_id=session_id)

    # Filter the Game objects associated with the session by game_id
    game = get_object_or_404(Game, id=game_id, session=session)


    player_score = dealer.count_score(game.player_hand)
    dealer_score = dealer.count_score(game.dealer_hand)

    while dealer_score <= 16:
        dealer_hand = game.dealer_hand
        dealer.hit(hand=dealer_hand, game_cards=game.get_deck())
        game.save()
        dealer_score = dealer.count_score(game.dealer_hand)
        
    
    result = dealer.evaluate(player_score=player_score, dealer_score=dealer_score)

    bet_result = {
        0: -1,
        1: 1,
        2: 0,
    }

    outcome = {
        0: 'Dealer',
        1: 'Player',
        2: 'Tie'
    }

    game.is_over=True
    game.winner=outcome[result]
    game.save()
    with transaction.atomic():
            session.bank += game.bet * bet_result[result]
            session.save()

    game_serializer = GameSerializer(game)

    return Response({"message": "Game ended", 'result': game_serializer.data})
