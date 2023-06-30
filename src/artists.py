import os
import csv
from flask import Blueprint, jsonify, request

from src.utils.graph_dfs_script import read_csv, build_graph, add_related_artists, dfs

artists = Blueprint("artists",__name__, url_prefix="/api/v1/artists")

# Get the directory of the current file
current_dir = os.path.dirname(os.path.abspath(__file__))

# Construct the path to the CSV file
csv_file_path = os.path.join(current_dir, 'utils', 'artists.csv')

@artists.get('/')
def get_all():
    artists = []
    with open(csv_file_path, 'r', encoding='utf-8') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            artists.append(row['Artist'])
    return jsonify({"artists": artists})

@artists.get('/genres')
def get_genres():
    genres = set()
    with open(csv_file_path, 'r', encoding='utf-8') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            genres.update(row['Genres'].split(', '))
    return jsonify({"genres": list(genres)})

@artists.get('/related')
def related_artists():
    artist_name = request.args.get('artist_name', 'Bad Bunny')  # Default value for artist_name
    min_streams = int(request.args.get('min_streams', 0))  # Default value for min_streams
    genres = request.args.get('genres', None)  # Default value for genres
    #split the genres and the push it to an array
    genres_arr=genres.split(',')
    genres=genres_arr

    artists = read_csv(csv_file_path)
    graph = build_graph(artists)
    add_related_artists(graph)

    start_artist = graph[artist_name]
    print(f"Related artists for {start_artist.name}:")
    results = []
    print(f"Min streams: {min_streams}")
    print(f"Genres: {genres}")
    dfs(start_artist, set(), results, min_streams=min_streams, genres=genres)
    return {
        "artist": start_artist.name,
        "Min streams": min_streams,
        "genres": genres if genres else None,
        "related_artists": [artist.name for artist in results],
        "count": len(results)
            }

@artists.delete('/<id>')
def delete(id):
    return "bookmark deleted"