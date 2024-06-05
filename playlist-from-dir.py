import os
import sys

def get_unique_filename(directory, base_name, extension):
    number = 0
    while True:
        if number == 0:
            filename = f"{base_name}{extension}"
        else:
            filename = f"{base_name}{number}{extension}"
        if not os.path.exists(os.path.join(directory, filename)):
            return filename
        number += 1

def create_playlist(directory):
    # Get the directory name to use as the base playlist name
    base_playlist_name = os.path.basename(os.path.normpath(directory))
    playlist_filename = get_unique_filename(directory, base_playlist_name, '.m3u8')

    # Get a list of all files in the directory
    files = os.listdir(directory)

    # Filter the list to include only audio files (you can add more extensions if needed)
    audio_extensions = ['.mp3', '.wav', '.flac', '.ogg', '.m4a', '.wma', '.aac', '.aiff', '.alac']
    songs = [file for file in files if os.path.splitext(file)[1].lower() in audio_extensions]

    # Create the playlist file
    with open(os.path.join(directory, playlist_filename), 'w', encoding='utf-8') as playlist_file:
        playlist_file.write('#EXTM3U\n\n')
        
        for song in songs:
            # Get the song name without the extension
            song_name = os.path.splitext(song)[0]
            
            # Get the song duration (in seconds)
            song_path = os.path.join(directory, song)
            song_duration = int(os.path.getsize(song_path) / 1000)  # Approximate duration based on file size
            
            playlist_file.write(f'#EXTINF:{song_duration}, {song_name}\n')
            playlist_file.write(f'{song}\n\n')

    print(f'Playlist "{playlist_filename}" created successfully with {len(songs)} songs.')

if __name__ == "__main__":
    if len(sys.argv) > 1:
        directory = sys.argv[1]
    else:
        directory = os.getcwd()
    
    if not os.path.isdir(directory):
        print(f'Error: The directory "{directory}" does not exist.')
    else:
        create_playlist(directory)
