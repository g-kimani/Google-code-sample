"""A video playlist class."""


class Playlist:
    """A class used to represent a Playlist."""
    def __init__(self, name):
        self.name = name
        self.videos = []
        self.playing = False
        self.current_video = None

    def display(self):
        return f"{self.name} ({len(self.videos)} Video{'s'if len(self.videos) > 1 or len(self.videos) == 0 else ''})"