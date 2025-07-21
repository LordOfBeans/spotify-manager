from spotify.user import User

# Spotify config contains: Client Id, Client Secret, Callback Port, Access Token Path, User Market
SPOTIFY_CONFIG_PATH = 'credentials/spotify-config.yaml'
# Postgres config contains: Host Name, Port Number, Username, Password, Database Name, Schema
POSTGRES_CONFIG_PATH = 'credentials/postgres-config.yaml'
# Application config is where you outline source/playlist relationships
APPLICATION_CONFIG_PATH = 'config.yaml'

def main():
    me = User(SPOTIFY_CONFIG_PATH)
    songs = me.getPlaylistSongs('2KQG7aBYkQAL8FmUduWkij')
    for song in songs:
        print(song)

if __name__ == '__main__':
    main()
