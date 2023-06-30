import csv

class Artist:
    def __init__(self, name, streams, tracks, genres):
        self.name = name
        self.streams = int(streams)
        self.tracks = tracks
        self.genres = genres
        self.related_artists = []
    
    def add_related_artist(self, artist):
        self.related_artists.append(artist)
    
    def __repr__(self):
        return self.name

def read_csv(file_path):
    artists = []
    with open(file_path, 'r', encoding='utf-8') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            artist = Artist(row['Artist'], row['Streams'], row['Tracks'], row['Genres'])
            artists.append(artist)
    return artists

def build_graph(artists):
    graph = {}
    for artist in artists:
        graph[artist.name] = artist
    return graph

def add_related_artists(graph):
    for artist in graph.values():
        genres = set(artist.genres.split(', '))
        for related_artist in graph.values():
            if related_artist != artist:
                related_genres = set(related_artist.genres.split(', '))
                if len(genres.intersection(related_genres)) > 0:
                    artist.add_related_artist(related_artist)

def dfs(artist, visited, results, min_streams=0, genres=None):
    if artist.streams < min_streams:
        return
    if genres and not set(genres).intersection(artist.genres.split(', ')):
        return

    print(f"{artist.name} - Streams: {artist.streams}")
    results.append(artist)
    visited.add(artist)

    for related_artist in artist.related_artists:
        if related_artist not in visited:
            dfs(related_artist, visited, results, min_streams, genres)


# Optional: Perform initial setup or actions when the module is executed as the main script
if __name__ == "__main__":
    csv_file = 'artists.csv'
    artists = read_csv(csv_file)
    print(f"Artists: {len(artists)}")
    graph = build_graph(artists)
    add_related_artists(graph)

    start_artist = graph['Bad Bunny']
    print(f"Related artists for {start_artist.name}:")
    results = []
    dfs(start_artist, set(), results, min_streams=500000, genres=['reggaeton'])
    print(results)
