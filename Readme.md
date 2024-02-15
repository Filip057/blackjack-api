# Blackjack API 

Blackjack API is a Django-based web application that allows users to play the popular card game Blackjack (also known as 21) through a RESTful API.

## Features

- Allows users to start a new game session.
- Supports placing bets and playing Blackjack rounds.
- Implements game logic for player and dealer actions.
- Keeps track of game state, including player and dealer hands, bet amount, and session 
information.

## Usage

# API Endpoints
- Start a new game session: POST /session/start/
Creates a new game session and returns session ID.
- Place a bet: GET /session/place_bet/<bet_amount>/
Places a bet for the current game session.
- Play a round: GET /session/hit/ or GET /session/stand/
Allows the player to either hit (draw a card) or stand (end their turn).

## Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/filip057/blackjack-api.git