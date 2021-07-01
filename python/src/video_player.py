"""A video player class."""

from .video_library import VideoLibrary
from .video_playlist import Playlist
from random import randint

class VideoPlayer:
    """A class used to represent a Video Player."""

    def __init__(self):
        self._video_library = VideoLibrary()
        self._current_video = None
        self._paused = False
        self._playlist_list = {}

    def number_of_videos(self):
        num_videos = len(self._video_library.get_all_videos())
        print(f"{num_videos} videos in the library")

    def show_all_videos(self):
        """Returns all videos."""
        all_videos = self._video_library.get_all_videos()
        all_videos.sort(key = lambda x: x.title)
        print("Here's a list of all available videos:")
        for video in all_videos:
            print(f"{video.title} ({video.video_id}) ", end="")
            if video.flag:
                print(f"[{' '.join(video.tags)}] - FLAGGED (reason: {video.flag_reason})")
            else:
                print(f"[{' '.join(video.tags)}]")

    def play_video(self, video_id):
        """Plays the respective video.

        Args:
            video_id: The video_id to be played.
        """
        new_video = self._video_library.get_video(video_id)
        if new_video is None:
            print("Cannot play video: Video does not exist")
        else:
            if new_video.flag:
                print(f"Cannot play video: Video is currently flagged (reason: {new_video.flag_reason})")
                return 
            if self._current_video is not None:
                self.stop_video()
            self._current_video = video_id
            print(f"Playing video: {new_video.title}")

    def stop_video(self):
        """Stops the current video."""
        if self._current_video is None:
            print("Cannot stop video: No video is currently playing")
        else:
            old_video = self._video_library.get_video(self._current_video)
            self._current_video = None
            self._paused = False
            print(f"Stopping video: {old_video.title}")
            
    def play_random_video(self):
        """Plays a random video from the video library."""

        if self._current_video is not None:
            self.stop_video()

        all_videos = self._video_library.get_all_videos()
        all_videos.sort(key = lambda x: x.title)

        # remove flagged videos
        cleared_videos = []
        for video in all_videos:
            if video.flag == False:
                cleared_videos.append(video)
        
        if len(cleared_videos) == 0:
            print("No videos available")
            return
        
        new_video_number = randint(0, len(all_videos) - 1)
        self.play_video(all_videos[new_video_number].video_id)

    def pause_video(self):
        """Pauses the current video."""

        current_video = self._video_library.get_video(self._current_video)

        if current_video is None:
            print("Cannot pause video: No video is currently playing")
        else:
            if self._paused:
                print(f"Video already paused: {current_video.title}")
            else:
                self._paused = True
                print(f"Pausing video: {current_video.title}")

    def continue_video(self):
        """Resumes playing the current video."""

        current_video = self._video_library.get_video(self._current_video)

        if current_video is None:
            print("Cannot continue video: No video is currently playing")
        else:
            if self._paused:
                self._paused = False
                print(f"Continuing video: {current_video.title}")
            else:
                print("Cannot continue video: Video is not paused")            

    def show_playing(self):
        """Displays video currently playing."""

        current_video = self._video_library.get_video(self._current_video)

        if current_video is None:
            print("No video is currently playing")
        else:
            print(f"Currently playing: {current_video.title} ({current_video.video_id}) ", end= "")

            if self._paused:
                print(f"[{' '.join(current_video.tags)}] - PAUSED")
            else:
                print(f"[{' '.join(current_video.tags)}]")

    def create_playlist(self, playlist_name):
        """Creates a playlist with a given name.

        Args:
            playlist_name: The playlist name.
        """
        if playlist_name.upper() in self._playlist_list:
            print("Cannot create playlist: A playlist with the same name already exists")
            return
        else:
            self._playlist_list[playlist_name.upper()] = Playlist(
                playlist_name
            )
            print(f"Successfully created new playlist: {playlist_name}")

    def add_to_playlist(self, playlist_name, video_id):
        """Adds a video to a playlist with a given name.

        Args:
            playlist_name: The playlist name.
            video_id: The video_id to be added.
        """
        if playlist_name.upper() not in self._playlist_list:
            print(f"Cannot add video to {playlist_name}: Playlist does not exist")
        else:
            new_video = self._video_library.get_video(video_id)
            if new_video is None:
                print(f"Cannot add video to {playlist_name}: Video does not exist")
            else:
                if new_video.flag:
                    print(f"Cannot add video to {playlist_name}: Video is currently flagged (reason: {new_video.flag_reason})")
                    return
                
                attempt = self._playlist_list[playlist_name.upper()].new_video(video_id)
                if attempt:
                    print(f"Added video to {playlist_name}: {new_video.title}")
                else:
                    print(f"Cannot add video to {playlist_name}: Video already added")
        
    def show_all_playlists(self):
        """Display all playlists."""
        if len(self._playlist_list) == 0:
            print("No playlists exist yet")
        else:
            print("Showing all playlists:")
            for key, value in sorted(self._playlist_list.items()):
                print(value.title)

    def show_playlist(self, playlist_name):
        """Display all videos in a playlist with a given name.

        Args:
            playlist_name: The playlist name.
        """
        if playlist_name.upper() not in self._playlist_list:
            print(f"Cannot show playlist {playlist_name}: Playlist does not exist")
        else:
            video_list = self._playlist_list[playlist_name.upper()].video_list
            print(f"Showing playlist: {playlist_name}")
            if len(video_list) == 0:
                print("No videos here yet")
            else:
                for video_id in video_list:
                    video = self._video_library.get_video(video_id)
                    print(f"{video.title} ({video.video_id}) ", end="")
                    if video.flag:
                        print(f"[{' '.join(video.tags)}] - FLAGGED (reason: {video.flag_reason})")
                    else:
                        print(f"[{' '.join(video.tags)}]")

    def remove_from_playlist(self, playlist_name, video_id):
        """Removes a video to a playlist with a given name.

        Args:
            playlist_name: The playlist name.
            video_id: The video_id to be removed.
        """
        if playlist_name.upper() not in self._playlist_list:
            print(f"Cannot remove video from {playlist_name}: Playlist does not exist")
        else:
            removing_video = self._video_library.get_video(video_id)
            if removing_video is None:
                print(f"Cannot remove video from {playlist_name}: Video does not exist")
            else:
                video_list = self._playlist_list[playlist_name.upper()].video_list
                if video_id in video_list:
                    video_list.remove(video_id)
                    print(f"Removed video from {playlist_name}: {removing_video.title}")
                else:
                    print(f"Cannot remove video from {playlist_name}: Video is not in playlist")

    def clear_playlist(self, playlist_name):
        """Removes all videos from a playlist with a given name.

        Args:
            playlist_name: The playlist name.
        """
        if playlist_name.upper() not in self._playlist_list:
            print(f"Cannot clear playlist {playlist_name}: Playlist does not exist")
        else:
            self._playlist_list[playlist_name.upper()].video_list.clear()
            print(f"Successfully removed all videos from {playlist_name}")

    def delete_playlist(self, playlist_name):
        """Deletes a playlist with a given name.

        Args:
            playlist_name: The playlist name.
        """
        if playlist_name.upper() not in self._playlist_list:
            print(f"Cannot delete playlist {playlist_name}: Playlist does not exist")
        else:
            self._playlist_list.pop(playlist_name, None)
            print(f"Deleted playlist: {playlist_name}")

    def search_videos(self, search_term):
        """Display all the videos whose titles contain the search_term.

        Args:
            search_term: The query to be used in search.
        """
        all_videos = self._video_library.get_all_videos()
        all_videos.sort(key = lambda x: x.title)
        search_results = [video for video in all_videos if search_term.upper() in video.title.upper()]

        # removed flagged videos
        cleared_videos = []
        for video in search_results:
            if video.flag == False:
                cleared_videos.append(video)

        if len(cleared_videos) == 0:
            print(f"No search results for {search_term}")
            return

        self.search_video_prompt(search_term, cleared_videos)
        
    def search_videos_tag(self, video_tag):
        """Display all videos whose tags contains the provided tag.

        Args:
            video_tag: The video tag to be used in search.
        """
        all_videos = self._video_library.get_all_videos()
        all_videos.sort(key = lambda x: x.title)
        search_results = []
        for video in all_videos:
            for tag in video.tags:
                if video_tag.upper() == tag.upper():
                    search_results.append(video)

        #removed flagged videos
        cleared_videos = []
        for video in search_results:
            if video.flag == False:
                cleared_videos.append(video)

        if len(cleared_videos) == 0:
            print(f"No search results for {video_tag}")
            return

        self.search_video_prompt(video_tag, cleared_videos)
        
    def search_video_prompt(self, query, cleared_videos):
        """Display search results, wait for prompt,
        attempt to display video (if possible).

        Args:
            query: What was searched.
            cleared_videos: The list of videos that aren't flagged.

        Return:
            The result from prompt.
        """
        print(f"Here are the results for {query}:")
        for index, video in enumerate(cleared_videos):
            print(f"{str(index + 1)}) {video.title} ({video.video_id}) ", end= "")
            print(f"[{' '.join(video.tags)}]")
        print("Would you like to play any of the above? If yes, specify the number of the video.")
        print("If your answer is not a valid number, we will assume it's a no.")
        answer = input("")
        if str.isdigit(answer) and int(answer) in range(1, len(cleared_videos) + 1):
            self.play_video(cleared_videos[int(answer) - 1].video_id)

    def flag_video(self, video_id, flag_reason=""):
        """Mark a video as flagged.

        Args:
            video_id: The video_id to be flagged.
            flag_reason: Reason for flagging the video.
        """
        current_video = self._video_library.get_video(video_id)
        if current_video is None:
            print("Cannot flag video: Video does not exist")
        else:
            if current_video.flag:
                print("Cannot flag video: Video is already flagged")
            else:
                if self._current_video == video_id:
                    self.stop_video()
                current_video.assign_flag(True)
                if flag_reason == "":
                    flag_reason = "Not supplied"
                current_video.assign_flag_reason(flag_reason)
                print(f"Successfully flagged video: {current_video.title} (reason: {flag_reason})")

    def allow_video(self, video_id):
        """Removes a flag from a video.

        Args:
            video_id: The video_id to be allowed again.
        """
        current_video = self._video_library.get_video(video_id)
        if current_video is None:
            print("Cannot remove flag from video: Video does not exist")
        else:
            if not current_video.flag:
                print("Cannot remove flag from video: Video is not flagged")
            else:
                current_video.assign_flag(False)
                print(f"Successfully removed flag from video: {current_video.title}")
