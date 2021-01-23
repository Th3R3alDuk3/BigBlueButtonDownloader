#!/usr/bin/env python3

import re
import requests
import pkg_resources
import xml.etree.ElementTree as ElementTree

from tqdm import tqdm
from pathlib import Path
from datetime import datetime
from argparse import ArgumentParser


class WebView:

    # webview template
    __TEMPLATE = pkg_resources.resource_string(
        __name__, "template.html"
    ).decode()

    def __init__(self, title: str, timestamp: datetime,
                 video1_file: Path, video2_file: Path,
                 video1_height: int = 250, video2_height: int = 450):

        """
        :param title: title of bigbluebutton presentation (meetingName)
        :param timestamp: timestamp of bigbluebutton presentation
        :param video1_file: path of first video
        :param video2_file: path of second video
        :param video1_height: height of first video
        :param video2_height: height of second video
        """

        # CEATE HTML CONTENT

        self.__html = self.__TEMPLATE.format(
            title, timestamp,
            video1_height,
            video1_file.name,
            video1_file.suffix[1:],
            video2_height,
            video2_file.name,
            video2_file.suffix[1:]
        )

    def save(self, output_directory: Path):

        """
        :param output_directory: directory for saveing webview_file
        """

        output_directory.joinpath("webview.html").write_text(self.__html)


class BigBlueButtonDownloader:

    # url of bigbluebutton
    __URL_PATTERN = r"{0}/playback/presentation/{1}/playback.html\?meetingId={2}".format(
        r"(?P<website>https?://[^/]+)",
        r"(?P<version>[0-9.]+)",
        r"(?P<video_id>[0-9a-f\-]+)"
    )

    def __init__(self, url: str):

        """
        :param url: url of bigbluebutton
        """

        self.__match = re.match(self.__URL_PATTERN, url)

        if self.__match is None:
            raise Exception("invalid bbb-url")

    def download_metadata(self, timeout: int = 3, verify: bool = True):

        """
        :param timeout: timeout for request
        :param verify: verify cerificate for request
        :return: content of metadata (xml format)
        """

        try:

            response = requests.get(
                "{0}/presentation/{1}/metadata.xml".format(
                    self.__match.group("website"),
                    self.__match.group("video_id")
                ), timeout=timeout, verify=verify
            )

            # raise exception if status_code != 200
            response.raise_for_status()

            return response.text

        except requests.exceptions.RequestException:
            return

    def _get_video_urls(self, video_file_extension: str = "webm"):

        """
        :param video_file_extension: type of video_file
        :return: yield tuples of video_name and video_url
        """

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

    def download_videos(self, output_directory: Path, video_file_extensions: list,
                        chunk_size: int = 1024, verify: bool = True):

        """
        :param output_directory: directory for saveing video_files
        :param video_file_extensions: list of diffenrent video_types
        :param chunk_size: size of stream_chunks
        :param verify: verify cerificate for request
        :return: yield paths of video_files
        """

        # loop video_file_extensions
        for video_file_extension in video_file_extensions:

            try:

                # loop tuples of video_name and video_url
                for video_name, video_url in self._get_video_urls(video_file_extension):

                    response = requests.get(
                        video_url,
                        stream=True, verify=verify
                    )

                    # raise exception if status_code != 200
                    response.raise_for_status()

                    video_file = output_directory.joinpath(video_name)

                    if video_file.exists():
                        yield video_file; continue

                    with video_file.open("wb") as fp:

                        # total size for progressbar
                        video_size = int(response.headers["Content-Length"])
                        total_size = int(video_size / chunk_size)

                        # pipe request_stream through progressbar
                        tqdm_stream = tqdm(
                            response.iter_content(chunk_size),
                            total=total_size, desc=video_name, unit="KB"
                        )

                        # loop request_stream
                        for chunk in tqdm_stream:
                            fp.write(chunk)

                    yield video_file

                # exit loop because of successful video_file_extension download
                break

            # try next video_file_extension
            except requests.exceptions.HTTPError:
                continue


def main():

    parser = ArgumentParser()

    # positional arguments
    parser.add_argument("output_directory")
    parser.add_argument("url")
    # optional arguments
    parser.add_argument("--webview_title")
    parser.add_argument("--webview_timestamp")
    parser.add_argument("--webview_video1_height", type=int, default=250)
    parser.add_argument("--webview_video2_height", type=int, default=450)

    args = parser.parse_args()

    print("+--------------------------+")
    print("| BigBlueButton Downloader |")
    print("+--------------------------+")

    bbbd = BigBlueButtonDownloader(args.url)

    output_directory = Path(args.output_directory)
    output_directory.mkdir(exist_ok=True)

    ###
    # DOWNLOAD NECESSARY FILES

    # get presentation metadata
    metadata = bbbd.download_metadata()

    if not metadata:
        exit("!!! unable to download metadata")

    # save presentation metadata
    output_directory.joinpath("metadata.xml").write_text(metadata)

    # download webcams- and deskshare-video
    video_files = bbbd.download_videos(output_directory, ["webm", "mp4"])
    video_files = list(video_files)

    if len(video_files) != 2:
        exit("!!! unable to download videos")

    ###
    # EXTRACT META_INFOS

    # xml element_tree
    etree_root = ElementTree.fromstring(metadata)

    title = args.webview_title
    if not title:
        title = etree_root.find("meta/meetingName").text

    timestamp = args.webview_timestamp
    if not timestamp:

        timestamp = etree_root.find("start_time").text
        timestamp = int(timestamp) / 1000
        timestamp = datetime.fromtimestamp(timestamp)
        timestamp = timestamp.strftime("Date: %d.%m.%Y Time: %H:%M")

    # TODO: get more infos from metadata

    ###
    # CREATE WEBVIEW

    print("create webview.html")

    WebView(
        title, timestamp,
        *video_files,
        args.webview_video1_height, args.webview_video2_height
    ).save(output_directory)


if __name__ == "__main__":
    main()
