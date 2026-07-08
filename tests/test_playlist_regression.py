from app import create_app
from models import Playlist
from services.playlist_service import get_playlist_songs


def test_get_playlist_songs_returns_all_playlist_songs():
    app = create_app()

    with app.app_context():
        playlist = Playlist.query.filter_by(name="Friday Energy").first()

        songs = get_playlist_songs(playlist.id)

        assert len(songs) == len(playlist.songs)