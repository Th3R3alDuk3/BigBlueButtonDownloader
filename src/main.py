#!/usr/bin/env python3

import pathlib
import argparse
# own packages
from bigbluebutton import WebView, Downloader


def main():

    parser = argparse.ArgumentParser()

    # positional arguments
    parser.add_argument("output_directory")
    parser.add_argument("url")

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

    # download presentation chat
    shapes_file = downloader.download_shapes(output_directory)
    # TODO: catch requests.exceptions

    # download presentation chat
    cursor_file = downloader.download_cursor(output_directory)
    # TODO: catch requests.exceptions

    # download webcams- and deskshare-video
    video_files = downloader.download_videos(output_directory, ["webm", "mp4"])
    video_files = list(video_files)

    # create shapes
    downloader.create_shapes(shapes_file, output_directory)

    if len(video_files) == 0:
        exit("!!! unable to download videos")

    ###
    # CREATE WEBVIEW

    WebView(
        chat_file,
        meta_file,
        args.url,
    ).save(output_directory)

    print("create webview.html")


if __name__ == "__main__":
    main()
