#!/usr/bin/env python3

import re
import tqdm
import pathlib
import argparse
import requests

from moviepy.editor import VideoFileClip


class BigBlueButtonDownloader:

    __URL_PATTERN = r"{0}/playback/presentation/{1}/playback.html\?meetingId={2}".format(
        r"(?P<website>https?://[^/]+)",
        r"(?P<version>[0-9.]+)",
        r"(?P<video_id>[0-9a-f\-]+)"
    )

    def __init__(self, url):

        self.__match = re.match(self.__URL_PATTERN, url)

        if self.__match is None:
            raise Exception("invalid url")

    def get_metadata(self, timeout: int = 3, verify: bool = False):

        response = requests.get(
            "{0}/presentation/{1}/metadata.xml".format(
                self.__match.group("website"),
                self.__match.group("video_id")
            ), timeout=timeout, verify=verify
        )

        # raise exception if status_code != 200
        response.raise_for_status()

        return response.text

    def get_video_urls(self, video_extension: str = "webm"):

        # order is important
        video_name2subpath = {
            "webcams": "/video/webcams",
            "deskshare": "/deskshare/deskshare"
        }

        for video_name, video_subpath in video_name2subpath.items():
            yield ("{0}.{1}".format(
                video_name,
                video_extension
            ), "{0}/presentation/{1}{2}.{3}".format(
                self.__match.group("website"),
                self.__match.group("video_id"),
                video_subpath,
                video_extension
            ))

    def download_videos(self, directory: pathlib.Path, video_extensions: list, chunk_size: int = 1024):

        for video_extension in video_extensions:

            try:

                for video_name, video_url in self.get_video_urls(video_extension):

                    response = requests.get(
                        video_url,
                        stream=True, verify=False
                    )

                    # raise exception if status_code != 200
                    response.raise_for_status()

                    video_file = directory.joinpath(video_name)

                    with video_file.open("wb") as fp:

                        # total size for progressbar
                        video_size = int(response.headers["Content-Length"])
                        total_size = int(video_size / chunk_size)

                        tqdm_stream = tqdm.tqdm(
                            response.iter_content(chunk_size),
                            total=total_size, desc=video_name, unit="KB"
                        )

                        for chunk in tqdm_stream:
                            fp.write(chunk)

                    yield video_file

                break

            except Exception:
                continue

    @staticmethod
    def sync_audio(video_file1: pathlib.Path, video_file2: pathlib.Path):

        video1 = VideoFileClip(video_file1)
        video2 = VideoFileClip(video_file2)

        video2.audio = video1.audio
        video2.write_videofile(video_file2)


def main():

    parser = argparse.ArgumentParser()

    parser.add_argument("directory")
    parser.add_argument("url")
    parser.add_argument("-s", "--sync", action="store_true")

    args = parser.parse_args()

    bbbd = BigBlueButtonDownloader(args.url)

    directory = pathlib.Path(args.directory)
    directory.mkdir(exist_ok=True)

    # get presentation metadata
    metadata = bbbd.get_metadata()
    # save presentation metadata
    directory.joinpath("metadata.xml").write_text(metadata)

    # download webcams- and deskshare-video
    video_files = bbbd.download_videos(directory, ["webm", "mp4"])
    video_files = list(video_files)

    # sync deskshare- with webcams-audio
    if args.sync:
        bbbd.sync_audio(*video_files)


if __name__ == "__main__":
    main()
