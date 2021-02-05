import re
import tqdm
import pathlib
import requests


class Downloader:

    # url of bigbluebutton presentation
    __URL_PATTERN = r"{0}/playback/presentation/{1}/playback.html\?meetingId={2}".format(
        r"(?P<website>https?://[^/]+)",
        r"(?P<version>[0-9.]+)",
        r"(?P<video_id>[0-9a-f\-]+)"
    )

    def __init__(self, url: str):

        """
        :param url: url of bigbluebutton presentation
        """

        self.__match = re.match(self.__URL_PATTERN, url)

        if self.__match is None:
            raise Exception("invalid bbb-url")

    def __get_file_url(self, file_name: str):

        """
        :param file_name: name of presentation file
        :return: return presentation file_url
        """

        return "{0}/presentation/{1}/{2}".format(
            self.__match.group("website"),
            self.__match.group("video_id"),
            file_name
        )

    @staticmethod
    def __download_file(output_directory: pathlib.Path,
                        file_url: str, file_name: str,
                        chunk_size: int = 1024,
                        verify: bool = True, timeout: int = 60):

        """
        :param output_directory: directory for saveing video_files
        :param file_url: url of file
        :param file_name: name of output_file
        :param chunk_size: size of stream_chunks
        :param timeout: timout for get request
        :param verify: verify cerificate for get request
        :return: paths of file
        """

        response = requests.get(
            file_url,
            stream=True,
            verify=verify,
            timeout=timeout
        )

        # raise exception if status_code != 200
        response.raise_for_status()

        file = output_directory.joinpath(file_name)

        if not file.exists():
            with file.open("wb") as fp:

                # progressbar size
                file_size = int(response.headers["Content-Length"])
                tqdm_size = int(file_size / chunk_size)

                # pipe request_stream through progressbar
                tqdm_stream = tqdm.tqdm(
                    response.iter_content(chunk_size),
                    total=tqdm_size,
                    desc=file_name,
                    unit="KB"
                )

                # loop request_stream
                for chunk in tqdm_stream:
                    fp.write(chunk)

                tqdm_stream.close()

        return file

    def _get_url_meta(self):

        """
        :return: return meta_url
        """

        return self.__get_file_url("metadata.xml")

    def _get_url_chat(self):

        """
        :return: return chat_url
        """

        return self.__get_file_url("slides_new.xml")

    def _get_url_videos(self, video_file_extension: str = "webm"):

        """
        :param video_file_extension: type of video_file
        :return: yield tuples of video_name and video_url
        """

        # order is important
        video_name2subpath = {
            "webcams": "video/webcams",
            "deskshare": "deskshare/deskshare"
        }

        for video_name, video_subpath in video_name2subpath.items():
            yield "{0}.{1}".format(
                video_name,
                video_file_extension
            ), self.__get_file_url(
                "{0}.{1}".format(
                    video_subpath,
                    video_file_extension
                )
            )

    def download_meta(self, output_directory: pathlib.Path):

        return self.__download_file(
            output_directory,
            self._get_url_meta(),
            "meta.xml"
        )

    def download_chat(self, output_directory: pathlib.Path):

        return self.__download_file(
            output_directory,
            self._get_url_chat(),
            "chat.xml"
        )

    def download_videos(self, output_directory: pathlib.Path, video_file_extensions: list):

        """
        :param output_directory: directory for saveing video_files
        :param video_file_extensions: list of diffenrent video_types
        :return: yield paths of video_files
        """

        for video_file_extension in video_file_extensions:

            try:

                for video_name, video_url in self._get_url_videos(video_file_extension):
                    yield self.__download_file(
                        output_directory,
                        video_url, video_name
                    )

                break

            except requests.exceptions.HTTPError:
                continue
