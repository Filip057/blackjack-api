def get_session_and_game_ids(request):
    session_id = request.headers.get('sid')
    game_id = request.headers.get('gid')
    return session_id, game_id