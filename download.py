#!python3

import re
import requests
import xml.etree.ElementTree as ET

from tqdm import tqdm
from pathlib import Path
from argparse import ArgumentParser


class WebView:

    __TEMPLATE_FILE = Path("template.html")

    def __init__(self, title: str, video_file_webcams: Path, video_file_deskshare: Path):

        self.__html = self.__TEMPLATE_FILE.read_text().format(
            title,
            "320", "240",   # 4:3 format
            video_file_webcams.name,
            video_file_webcams.suffix[1:],
            "800", "450",   # 16:9 format
            video_file_deskshare.name,
            video_file_deskshare.suffix[1:]
        )

    def save(self, directory: Path):
        directory.joinpath("webview.html").write_text(self.__html)


class BigBlueButtonDownloader:

    __URL_PATTERN = r"{0}/playback/presentation/{1}/playback.html\?meetingId={2}".format(
        r"(?P<website>https?://[^/]+)",
        r"(?P<version>[0-9.]+)",
        r"(?P<video_id>[0-9a-f\-]+)"
    )

    def __init__(self, url: str):

        self.__match = re.match(self.__URL_PATTERN, url)

        if self.__match is None:
            raise Exception("invalid bbb-url")

    def get_metadata(self, timeout: int = 3, verify: bool = True):

        response = requests.get(
            "{0}/presentation/{1}/metadata.xml".format(
                self.__match.group("website"),
                self.__match.group("video_id")
            ), timeout=timeout, verify=verify
        )

        # raise exception if status_code != 200
        response.raise_for_status()

        return response.text

    def get_video_urls(self, video_file_extension: str = "webm"):

        # order is important
        video_name2subpath = {
            "webcams": "/video/webcams",
            "deskshare": "/deskshare/deskshare"
        }

        for video_name, video_subpath in video_name2subpath.items():
            yield "{0}.{1}".format(
                video_name,
                video_file_extension
            ), "{0}/presentation/{1}{2}.{3}".format(
                self.__match.group("website"),
                self.__match.group("video_id"),
                video_subpath,
                video_file_extension
            )

    def download_videos(self, directory: Path, video_file_extensions: list, chunk_size: int = 1024):

        for video_file_extension in video_file_extensions:

            try:

                for video_name, video_url in self.get_video_urls(video_file_extension):

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

                        tqdm_stream = tqdm(
                            response.iter_content(chunk_size),
                            total=total_size, desc=video_name, unit="KB"
                        )

                        for chunk in tqdm_stream:
                            fp.write(chunk)

                    yield video_file

                break

            except Exception:
                continue


def main():

    parser = ArgumentParser()

    parser.add_argument("output_directory")
    parser.add_argument("url")

    args = parser.parse_args()

    bbbd = BigBlueButtonDownloader(args.url)

    output_directory = Path(args.output_directory)
    output_directory.mkdir(exist_ok=True)

    # DOWNLOAD FILES

    # get presentation metadata
    metadata = bbbd.get_metadata()
    # save presentation metadata
    output_directory.joinpath("metadata.xml").write_text(metadata)

    # download webcams- and deskshare-video
    video_files = bbbd.download_videos(output_directory, ["webm", "mp4"])
    video_files = list(video_files)

    # CREATE WEBVIEW

    root = ET.fromstring(metadata)
    name = root.find("meta/meetingName").text
    # TODO: get more infos from meta

    webview = WebView(name, *video_files)
    webview.save(output_directory)


if __name__ == "__main__":
    main()
