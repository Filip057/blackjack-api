from django.db import models
import uuid
import json

# Create your models here.
class Session(models.Model):
    username = models.CharField(max_length=50)
    session_id = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)
    bank = models.IntegerField(default=1000)

class Game(models.Model):
    session = models.ForeignKey(Session, on_delete=models.CASCADE)
    is_over = models.BooleanField(default=False)
    bet_placed = models.BooleanField(default=False)
    bet = models.PositiveIntegerField(choices=[
        (10, '10'),
        (25, '25'),
        (50, '50'),
        (75, '75'),
        (100, '100'),
        ], default=0)
    player_hand = models.JSONField(default=list)
    dealer_hand = models.JSONField(default=list)
    winner = models.CharField(max_length=50, blank=True, null=True)
    deck = models.TextField(default=json.dumps(['2', '3', '4', '5', '6', '7', '8', '9', '10', 'J', 'Q', 'K', 'A'] * 4))

    def get_deck(self):
        return json.loads(self.deck)


                                          