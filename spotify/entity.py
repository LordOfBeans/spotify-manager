class Song:
    def __init__(self, info, format):
        if format == 'spotify':
            track = info['track']
            self.id = track['id']
            self.name = track['name']
        elif format == 'postgres':
            self.id = info['song_id']
            self.name = info['name']

    def __str__(self):
        return f'{self.id}: {self.name}'

