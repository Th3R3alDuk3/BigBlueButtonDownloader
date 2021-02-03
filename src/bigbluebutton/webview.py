import pathlib
import importlib.resources


class WebView:

    # webview template
    __TEMPLATE = importlib.resources.read_text("bigbluebutton", "template.html")

    def __init__(self, video1_file: pathlib.Path, video2_file: pathlib.Path, *args):

        """
        :param title: title of bigbluebutton presentation (meetingName)
        :param timestamp: timestamp of bigbluebutton presentation
        :param video1_file: path of first video
        :param video2_file: path of second video
        """

        # CEATE HTML CONTENT

        self.__html = self.__TEMPLATE.format(
            video1_file.name,
            video1_file.suffix[1:],
            video2_file.name,
            video2_file.suffix[1:],
            *args
        )

    def save(self, output_directory: pathlib.Path):

        """
        :param output_directory: directory for saveing webview_file
        :return: webview_file
        """

        webview_file = output_directory.joinpath("webview.html")
        webview_file.write_text(self.__html)

        return webview_file
