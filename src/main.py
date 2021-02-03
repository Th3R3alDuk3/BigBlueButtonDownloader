#!/usr/bin/env python3


import pathlib
import datetime
import argparse
import xml.etree.ElementTree
# own packages
from bigbluebutton import WebView, Downloader


def main():

    parser = argparse.ArgumentParser()

    # positional arguments
    parser.add_argument("output_directory")
    parser.add_argument("url")
    # optional arguments
    parser.add_argument("--webview_title")
    parser.add_argument("--webview_start")

    args = parser.parse_args()

    print("+--------------------------+")
    print("| BigBlueButton Downloader |")
    print("+--------------------------+")

    downloader = Downloader(args.url)

    output_directory = pathlib.Path(args.output_directory)
    output_directory.mkdir(exist_ok=True)

    ###
    # DOWNLOAD NECESSARY FILES

    # download presentation meta
    meta_file = downloader.download_meta(output_directory)
    # TODO: catch requests.exceptions

    # download presentation chat
    chat_file = downloader.download_chat(output_directory)
    # TODO: catch requests.exceptions

    # download webcams- and deskshare-video
    video_files = downloader.download_videos(output_directory, ["webm", "mp4"])
    video_files = list(video_files)
    video_files.reverse()

    if len(video_files) != 2:
        exit("!!! unable to download videos")

    ###
    # EXTRACT META_INFOS

    webview_args = ["Meeting", "unknown"]

    if meta_file:

        etree_root = xml.etree.ElementTree.fromstring(
            meta_file.read_text()
        )

        title = args.webview_title
        if not title:
            title = etree_root.find("meta/meetingName").text

        start = args.webview_start
        if not start:

            start = etree_root.find("start_time").text
            start = int(start) / 1000

            start = datetime.datetime.fromtimestamp(start)
            start = start.strftime("Date: %d.%m.%Y Time: %H:%M")

        webview_args = [title, start]

        # TODO: get more infos from meta

    ###
    # CREATE WEBVIEW

    print("create webview.html")

    _ = WebView(
        *video_files,
        *webview_args
    ).save(output_directory)


if __name__ == "__main__":
    main()
