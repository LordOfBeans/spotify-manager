from spotify.user import User

import yaml

# Spotify config contains: Client Id, Client Secret, Callback Port, Access Token Path, User Market
SPOTIFY_CONFIG_PATH = 'credentials/spotify-config.yaml'
# Postgres config contains: Host Name, Port Number, Username, Password, Database Name, Schema
POSTGRES_CONFIG_PATH = 'credentials/postgres-config.yaml'
# App config is where you outline source/playlist relationships
APP_CONFIG_PATH = 'config.yaml'

def main():
    me = User(SPOTIFY_CONFIG_PATH)
    with open(APP_CONFIG_PATH, 'r') as f:
        config = yaml.safe_load(f)

    source_set = set()
    for alias, info in config['sources'].items():
        id = info['id']
        source_type = info['type']
        print(f'Getting songs from {source_type} {alias}')
        songs = me.getPlaylistSongs(id)
        for song in songs:
            source_set.add(song)
    for song in source_set:
        print(song)
    print(f'Found {len(source_set)} songs from sources')

    aggregate_id = '2KQG7aBYkQAL8FmUduWkij'
    aggregate_set = set()
    aggregate_songs = me.getPlaylistSongs('2KQG7aBYkQAL8FmUduWkij')
    for song in aggregate_songs:
        aggregate_set.add(song)
    print(f'Found {len(aggregate_set)} songs on product')

    diff_set = source_set - aggregate_set
    diff_list = list(diff_set)
    print(f'Found {len(diff_list)} songs to add')

    me.addPlaylistSongs(aggregate_id, diff_list, position=4)

if __name__ == '__main__':
    main()
