from flask import Flask, request, jsonify



app = Flask(__name__)

s = 0
class Song:
    def __init__(self, title, artist, duration, genre):
        global s
        self.title = title
        self.artist = artist
        self.duration = duration
        self.genre = genre
        self.id = s

    def __str__(self):
        return f"{self.title} by {self.artist}\nDuration: {self.duration}\nGenre: {self.genre}"

class Node:
    def __init__(self, song):
        self.song = song
        self.next = None
        self.prev = None

class PlaylistManager:
    def __init__(self, name):
        self.name = name
        self.head = None
        self.current_song = None

    def add_song(self, title, artist, duration, genre):
        # Create a new Song instance with the args
        new_song = Song(title, artist, duration, genre)
        global s
        s += 1
        # Create a node with the Song
        new_node = Node(new_song)
        if self.head is None:
            self.head = new_node
        else:
            node = self.head
            while node.next is not None:
                node = node.next
            node.next = new_node
            new_node.prev = node

    def remove_song(self, id):
        if self.head is None:
            print(f"The playlist '{self.name}' is empty")
            return
        # If the first node is the node we are trying to removing
        if self.head.song.id == id:
            # Set the .head attribute to be the next node
            self.head = self.head.next
            # If the new head is a node
            if self.head:
                self.head.prev = None
            return
        # Start at the first node
        current_node = self.head
        # While the current node is not None
        while current_node:
            # If the current node is the one we are trying to remove
            if current_node.song.id == id:
                # Adjust the pointers
                if current_node.prev:
                    current_node.prev.next = current_node.next
                if current_node.next:
                    current_node.next.prev = current_node.prev
                return
            # If not, move on to the next node
            current_node = current_node.next
        # If we get to the end of the Linked List without returning, the node was never there
        print(f"song {id} is not in the '{self.name}' playlist.")

    def search_song(self, title):
        if self.head is None:
            return(-1)
        # If the first node is the node we are trying to removing
        if self.head.song.title == title:
            return self.head.song
        # Start at the first node
        current_node = self.head
        # While the current node is not None
        while current_node:
            # If the current node is the one we are trying to remove
            if current_node.song.title == title:
                return current_node.song
            # If not, move on to the next node
            current_node = current_node.next
        # If we get to the end of the Linked List without returning, the node was never there
        return -1

    def play_next(self):
        # If there is no current song
        if self.current_song is None:
            # Set the current song to the first song in the playlist
            self.current_song = self.head
        # if there is
        else:
            # Set the current song to the next song
            self.current_song = self.current_song.next
        # Make sure that the new current song exists
        if self.current_song is not None:
            song = self.current_song.song
            print(f"Currently Playing: {song}")
        # if self.current_song is None
        else:
            print(f"At the end of the '{self.name}' playlist")

    def go_back(self):
        if self.current_song is None:
            print('Cannot go back. At the beginning of the playlist')
        else:
            self.current_song = self.current_song.prev
            if self.current_song is not None:
                song = self.current_song.song
                print(f"Currently Playing: {song}")
            # if self.current_song is None
            else:
                print(f"At the beginning of the '{self.name}' playlist")

playlists = []


@app.route("/", methods = ["GET"])
def hi():
    return("Welcome to the playlist Site!!!!")



@app.route("/playlist/create", methods = ["POST"])
def create_playlist():
    playlist_data = request.json
    playlists.append(PlaylistManager(playlist_data["name"]))
    return(f"The playlist: {playlist_data["name"]}, has been created with the id {len(playlists) - 1}")


@app.route("/playlist/<int:id>", methods=["GET"])
def view_playlist(id):
    songs = []
    for song in playlists[id]:
        songs.append(song.title)
    f"\n".join()
    return(f"{playlists[id].name}:\n     {blah}")

@app.route("/playlist/update/<int:id>", methods=["PUT"])
def update_playlist(id):
    playlist_data = request.json
    playlists[id] = PlaylistManager(playlist_data["name"])
    return(f"The playlist: {playlist_data["name"]}, has been updated with the id {id}")


@app.route("/playlist/delete/<int:id>", methods=["DELETE"])
def delete_playlist(id):
    playlists.pop(id)
    return(f"The playlist was succesfully deleted!")


@app.route("/playlist/<int:id>/add_song", methods = ["POST"])
def add_song_to_playlist(id):
    song_data = request.json
    title = song_data["title"]
    artist = song_data["artist"]
    duration = song_data["duration"]
    genre = song_data["genre"]
    playlists[id].add_song(title, artist, duration, genre)
    return(f"The song: {song_data["title"]}, has been added to the playlist {playlists[id].name}")

@app.route("/playlist/<int:playlist_id>/remove_song/<int:song_id>", methods=["DELETE"])
def remove_song_from_playlist(playlist_id, song_id):
    song = playlists[playlist_id].remove_song(song_id)
    return("The song has been removed")

@app.route("/playlist/search/<title>", methods=["GET"])
def view_song(title):
    id = 0
    for playlist in playlists:
        song  = playlist.search_song(title)
        if song != -1:
            return(f"{song.title} by {song.artist}\n{song.duration}\n{song.genre}\nin playlist {id}\nwith the song id:{song.id}\n")
        else:
            id += 1
    return("Song not found")
    




if __name__ == "__main__":
    app.run(debug=True)