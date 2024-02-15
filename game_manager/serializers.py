from rest_framework import serializers
from .models import Session, Game

class SessionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Session
        fields = ['session_id', 'username']

class GameSerializer(serializers.ModelSerializer):
    dealer_hand = serializers.SerializerMethodField()

    class Meta:
        model = Game
        fields = ['id', 'is_over', 'bet_placed', 'bet', 'player_hand', 'dealer_hand', 'winner']
    
    def get_dealer_hand(self, obj):
        # Process the dealer's hand to show only one card and 'X' for the other
        if obj.dealer_hand and not obj.is_over:
        # Show the first card in the dealer's hand
            visible_card = obj.dealer_hand[0]
        # Replace other cards with 'X'
            hidden_cards = 'X' * (len(obj.dealer_hand) - 1)
            return [visible_card] + [hidden_cards]
        else:
            return obj.dealer_hand

