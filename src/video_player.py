"""A video player class."""
from operator import attrgetter

from .video_library import VideoLibrary
from .video_playlist import Playlist
import random as rnd


class VideoPlayer:
    """A class used to represent a Video Player."""

    def __init__(self):
        self._video_library = VideoLibrary()
        self._playing = None
        self._paused = False
        self._playlists = {}
        self._current_playlist = None

    def number_of_videos(self):
        num_videos = len(self._video_library.get_all_videos())
        print(f"{num_videos} videos in the library")

    def show_all_videos(self):
        """Returns all videos."""
        videos = self._video_library.get_all_videos()
        print("Here's a list of all available videos:")
        videos.sort(key=attrgetter('title'))
        for video in videos:
            print(video.display())

    def play_video(self, video_id):
        """Plays the respective video.

        Args:
            video_id: The video_id to be played.
        """
        video = self._video_library.get_video(video_id)

        warning_message = "Cannot play video"

        if not self.video_exists(video_id, warning_message):
            return

        if video.flagged:
            print(f"{warning_message}: Video is currently flagged (reason: {video.flag_reason})")
            return

        if self._playing:
            print(f"Stopping video: {self._playing.title}")

        print(f"Playing video: {video.title}")
        self._playing = video
        self._paused = False

    def stop_video(self):
        """Stops the current video."""
        if self._playing:
            print(f"Stopping video: {self._playing.title}")
            self._playing = None
            self._paused = False
            return

        print("Cannot stop video: No video is currently playing")

    def play_random_video(self):
        """Plays a random video from the video library."""
        videos = self._video_library.get_all_videos()
        if not (len(videos) > 0) or len([video for video in videos if video.flagged]) == len(videos):
            print("No videos available")
            return

        video_picked = False
        video = None
        while not video_picked:
            video = rnd.choice(videos)
            if not video.flagged:
                video_picked = True

        if self._playing:
            print(f"Stopping video: {self._playing.title}")

        print(f"Playing video: {video.title}")
        self._playing = video
        self._paused = False

    def pause_video(self):
        """Pauses the current video."""
        if not self._playing:
            print("Cannot pause video: No video is currently playing")
            return
        if self._paused:
            print(f"Video already paused: {self._playing.title}")
            return

        self._paused = True
        print(f"Pausing video: {self._playing.title}")

    def continue_video(self):
        """Resumes playing the current video."""
        if not self._playing:
            print("Cannot continue video: No video is currently playing")
            return
        if not self._paused:
            print("Cannot continue video: Video is not paused")
            return

        print(f"Continuing video: {self._playing.title}")
        self._paused = False

    def show_playing(self):
        """Displays video currently playing."""
        if not self._playing:
            print("No video is currently playing")
            return

        print(f"Currently playing: {self._playing.display()}{'- PAUSED' if self._paused else ''}")

    def create_playlist(self, playlist_name):
        """Creates a playlist with a given name.

        Args:
            playlist_name: The playlist name.
        """
        playlist_exists = self._playlists.get(playlist_name.lower(), None)

        if playlist_exists:
            print("Cannot create playlist: A playlist with the same name already exists")
            return

        self._playlists[playlist_name.lower()] = Playlist(playlist_name)
        print(f"Successfully created new playlist: {playlist_name}")

    def add_to_playlist(self, playlist_name, video_id):
        """Adds a video to a playlist with a given name.

        Args:
            playlist_name: The playlist name.
            video_id: The video_id to be added.
        """
        warning_message = f"Cannot add video to {playlist_name}"

        if not self.playlist_exists(playlist_name, warning_message):
            return
        if not self.video_exists(video_id, warning_message):
            return

        video = self._video_library.get_video(video_id)
        if video.flagged:
            print(f"{warning_message}: Video is currently flagged (reason: {video.flag_reason})")
            return

        playlist = self._playlists[playlist_name.lower()]

        if video_id in playlist.videos:
            print(f"{warning_message}: Video already added")
            return

        playlist.videos.append(video_id)

        print(f"Added video to {playlist_name}: {video.title}")

    def show_all_playlists(self):
        """Display all playlists."""
        if len(self._playlists) > 0:
            print("Showing all playlists:")
            for playlist in sorted(self._playlists.keys()):
                print(self._playlists[playlist].display())
        else:
            print("No playlists exist yet")

    def show_playlist(self, playlist_name):
        """Display all videos in a playlist with a given name.

        Args:
            playlist_name: The playlist name.
        """

        warning_message = f"Cannot show playlist {playlist_name}"
        if not self.playlist_exists(playlist_name, warning_message):
            return

        playlist = self._playlists.get(playlist_name.lower(), None)

        print(f"Showing playlist: {playlist_name}")
        if len(playlist.videos) > 0:
            for video_id in playlist.videos:
                video = self._video_library.get_video(video_id)
                print(video.display())
        else:
            print("No videos here yet")

    def remove_from_playlist(self, playlist_name, video_id):
        """Removes a video to a playlist with a given name.

        Args:
            playlist_name: The playlist name.
            video_id: The video_id to be removed.
        """

        warning_message = f"Cannot remove video from {playlist_name}"

        if not self.playlist_exists(playlist_name, warning_message):
            return
        if not self.video_exists(video_id, warning_message):
            return

        playlist = self._playlists[playlist_name.lower()]
        video = self._video_library.get_video(video_id)
        if video_id in playlist.videos:
            playlist.videos.remove(video_id)
            print(f"Removed video from {playlist_name}: {video.title}")
            return
        else:
            print(f"{warning_message}: Video is not in playlist")

    def playlist_exists(self, playlist_name, warning_message):
        """ Checks that the playlist exists within the video player
            If not displays appropriate warning message
        """
        playlist = self._playlists.get(playlist_name.lower(), None)
        if not playlist:
            print(f"{warning_message}: Playlist does not exist")
            # create_choice = input(f"Would you like to create playlist: {playlist_name} (Y, N) ").lower()
            # if create_choice == 'y':
            #     self.create_playlist(playlist_name)
            #     return True
            # else:
            return False

        return True

    def video_exists(self, video_id, warning_message):
        video = self._video_library.get_video(video_id)
        if not video:
            print(f"{warning_message}: Video does not exist")
            return False

        return True

    def play_playlist(self, playlist_name):
        """ Starts playing the videos from a playlist """
        warning_message = f"Cannot play playlist {playlist_name}"
        if not self.playlist_exists(playlist_name, warning_message):
            return
        playlist = self._playlists.get(playlist_name)
        if not (len(playlist.videos) > 0):
            print("There are no videos to play")
        else:
            video_id = playlist.videos[0]
            playlist.current_video = 0
            self._current_playlist = playlist
            print(f"Starting playlist: {playlist_name}")
            self.play_video(video_id)

    def play_next(self):
        """Plays next video in play list, does nothing if playlist is not playing"""
        warning_message = "Cannot go to next video"
        if not self._current_playlist:
            print(f"{warning_message}: No playlist playing")
            return

        next_video = self._current_playlist.current_video + 1

        if self._playing:
            self.stop_video()

        if next_video > len(self._current_playlist.videos) - 1:
            print("You have reached the end of the playlist")
            return
        video_id = self._current_playlist.videos[next_video]
        self._current_playlist.current_video += 1
        self.play_video(video_id)

    def show_current_playlist(self):
        if self._current_playlist:
            print(self._current_playlist.display())
        else:
            print("No playlist playing")

    def clear_playlist(self, playlist_name):
        """Removes all videos from a playlist with a given name.

        Args:
            playlist_name: The playlist name.
        """

        warning_message = f"Cannot clear playlist {playlist_name}"
        if not self.playlist_exists(playlist_name, warning_message):
            return

        self._playlists[playlist_name.lower()].videos = []
        print(f"Successfully removed all videos from {playlist_name}")

    def delete_playlist(self, playlist_name):
        """Deletes a playlist with a given name.

        Args:
            playlist_name: The playlist name.
        """
        playlist = self._playlists.pop(playlist_name.lower(), None)
        if not playlist:
            print(f"Cannot delete playlist {playlist_name}: Playlist does not exist")
            return

        print(f"Deleted playlist: {playlist_name}")

    def search_videos(self, search_term):
        """Display all the videos whose titles contain the search_term.

        Args:
            search_term: The query to be used in search.
        """
        videos = [video for video in self._video_library.get_all_videos()
                  if search_term.lower() in video.title.lower() and not video.flagged]

        videos.sort(key=attrgetter('title'))
        if len(videos) > 0:
            print(f"Here are the results for {search_term}:")
            for i in range(len(videos)):
                print(f"{i + 1}) {videos[i].display()}")
            self.search_input(videos)
            return
        print(f"No search results for {search_term}")

    def search_videos_tag(self, video_tag):
        """Display all videos whose tags contains the provided tag.

        Args:
            video_tag: The video tag to be used in search.
        """
        videos = [video for video in self._video_library.get_all_videos()
                  if video_tag.lower() in [tag.lower() for tag in video.tags] and not video.flagged]

        videos.sort(key=attrgetter('title'))
        if len(videos) > 0:
            print(f"Here are the results for {video_tag}:")
            for i in range(len(videos)):
                print(f"{i + 1}) {videos[i].display()}")
            self.search_input(videos)
            return

        print(f"No search results for {video_tag}")

    def search_input(self, videos):
        """ Handles user input after a search """
        print("Would you like to play any of the above? If yes, specify the number of the video.")
        print("If your answer is not a valid number, we will assume it's a no.")
        try:
            choice = int(input(''))
            if len(videos) >= choice > 0:
                self.play_video(videos[choice - 1].video_id)
        except Exception as e:
            # print(e)
            pass

    def flag_video(self, video_id, flag_reason=""):
        """Mark a video as flagged.

        Args:
            video_id: The video_id to be flagged.
            flag_reason: Reason for flagging the video.
        """
        warning_message = "Cannot flag video"
        if not self.video_exists(video_id, warning_message):
            return

        video = self._video_library.get_video(video_id)

        if video.flagged:
            print(f"{warning_message}: Video is already flagged")
            return

        # Stop the video if it is same as one being flagged
        if self._playing and self._playing.video_id == video_id:
            self.stop_video()

        video.flagged = True
        if len(flag_reason) > 0:
            video.flag_reason = flag_reason
        else:
            video.flag_reason = 'Not supplied'

        print(f"Successfully flagged video: {video.title} (reason: {video.flag_reason})")

    def allow_video(self, video_id):
        """Removes a flag from a video.

        Args:
            video_id: The video_id to be allowed again.
        """
        warning_message = "Cannot remove flag from video"
        if not self.video_exists(video_id, warning_message):
            return

        video = self._video_library.get_video(video_id)

        if not video.flagged:
            print(f"{warning_message}: Video is not flagged")
            return

        video.flagged = False
        video.flag_reason = ''
        print(f"Successfully removed flag from video: {video.title}")

    def rate_video(self, video_id, rating):
        warning_message = "Cannot rate the video"
        if not self.video_exists(video_id, warning_message):
            return
        if int(rating) > 5 or int(rating) < 1:
            print("Ratings need to be between 1 and 5")
            return

        video = self._video_library.get_video(video_id)
        video.rating = rating
        print(f"Rated {video.title}: {rating}")
