import os
import datetime
import pandas as pd
import csv
import spotipy
import concurrent.futures
from spotipy.oauth2 import SpotifyClientCredentials

def get_track_info(song_name):
    print(song_name)

def get_file_names(folder):
    current_date = datetime.date.today()
    date_range = pd.date_range(start="2023-01-01", end=current_date, freq="W-THU")
    file_names = [os.path.join(folder, f"regional-global-weekly-{date.strftime('%Y-%m-%d')}.csv") for date in date_range]
    return file_names

def process_file(file_name):
    csv_data = pd.read_csv(file_name)
    csv_data['uri'] = csv_data['uri'].str.split(":").str[2]
    return csv_data[['artist_names', 'track_name', 'uri', 'streams']]

def read_data(folder):
    file_names = get_file_names(folder)
    csv_data = pd.concat([process_file(file_name) for file_name in file_names if os.path.isfile(file_name)], ignore_index=True)
    return csv_data

def transform_data(data):
    transformed_data = {}
    for index, row in data.iterrows():
        artist_names = row['artist_names'].split(", ")  # Separate artist names if they contain a comma
        
        for artist_name in artist_names:
            track_name = row['track_name']
            uri = row['uri']
            streams = int(row['streams'])
            
            if artist_name not in transformed_data:
                transformed_data[artist_name] = {
                    'streams': streams,
                    'tracks': [{'track_name': track_name, 'uri': uri}],
                    'genres': []
                }
            else:
                transformed_data[artist_name]['streams'] = streams
                transformed_data[artist_name]['tracks'].append({'track_name': track_name, 'uri': uri})
    
    return transformed_data

def add_genres_for_artist(artist_name, sp):
    artist_info = sp.search(q=artist_name, type='artist')
    genres = []
    
    if artist_info['artists']['items']:
        genres = artist_info['artists']['items'][0]['genres']
    
    return artist_name, genres

def add_genres(transformed_data):
    # Initialize Spotify client credentials
    client_id = os.environ.get('CLIENT_ID')
    client_secret = os.environ.get('CLIENT_SECRET')
    auth_manager = SpotifyClientCredentials(client_id=client_id, client_secret=client_secret)
    sp = spotipy.Spotify(auth_manager=auth_manager)
    
    with concurrent.futures.ThreadPoolExecutor() as executor:
        futures = []
        for artist_name in transformed_data:
            futures.append(executor.submit(add_genres_for_artist, artist_name, sp))
        req=0
        for future in concurrent.futures.as_completed(futures):
            req+=1
            print(req)
            artist_name, genres = future.result()
            if genres:
                transformed_data[artist_name]['genres'] = genres
            else:
                transformed_data.pop(artist_name)
    
    return transformed_data

def remove_duplicates(data):
    # Sort the data by streams in descending order
    sorted_data = data.sort_values('streams', ascending=False)
    
    # Drop duplicates keeping the first occurrence (highest streams)
    unique_data = sorted_data.drop_duplicates(subset=['artist_names', 'track_name', 'uri'], keep='first')
    
    return unique_data


def save_to_csv(data, filename):
    with open(filename, 'w', newline='', encoding='utf-8') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(['Artist', 'Streams', 'Tracks', 'Genres'])
        
        for artist_name, artist_data in data.items():
            streams = artist_data['streams']
            tracks = artist_data['tracks']
            genres = artist_data['genres']
            
            track_names = [track['track_name'] for track in tracks]
            
            writer.writerow([artist_name, streams, ', '.join(track_names), ', '.join(genres)])

if __name__ == "__main__":
    folder_path = "mocks"
    data = read_data(folder_path)
    print(len(data))
    data = remove_duplicates(data)
    print(len(data))
    transformed_data = transform_data(data)
    print(len(transformed_data))
    transformed_data_with_genres = add_genres(transformed_data)
    print(transformed_data_with_genres)
    print(len(transformed_data_with_genres))
    save_to_csv(transformed_data_with_genres, 'artists.csv')
    print("Data saved to artists.csv")