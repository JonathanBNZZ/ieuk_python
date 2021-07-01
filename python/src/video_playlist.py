"""A video playlist class."""


class Playlist:
    """A class used to represent a Playlist."""

    def __init__(self, playlist_title: str):
        """Playlist constructor."""
        self._title = playlist_title
        self._video_list = []

    @property
    def title(self) -> str:
        """Returns the title of a playlist."""
        return self._title

    @property
    def video_list(self) -> []:
        """Returns the set of video ids of a playlist."""
        return self._video_list

    def new_video(self, video_id):
        """Insert a new video id into playlist.

        Args:
            video_id: The video url.

        Return:
            True/False on unique/duplicate insert.
        """
        if video_id in self._video_list:
            return False
        self._video_list.append(video_id)
        return True