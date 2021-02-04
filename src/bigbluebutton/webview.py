import pathlib
import datetime
import importlib.resources
import xml.etree.ElementTree


class WebView:

    __TEMPLATES = [
        importlib.resources.read_text("bigbluebutton", "template.html"),
        importlib.resources.read_text("bigbluebutton", "template.css"),
        importlib.resources.read_text("bigbluebutton", "template.js")
    ]

    def __init__(self, video1_file: pathlib.Path, video2_file: pathlib.Path,
                 chat_file: pathlib.Path, meta_file: pathlib.Path, url: str):

        """
        :param video1_file: path of first video file
        :param video2_file: path of second video file
        :param chat_file: path of chat file
        :param meta_file: path of meta file
        """

        # CEATE HTML CONTENT

        self.__html = self.__TEMPLATES[0].format(
            self.__TEMPLATES[1],
            self.__TEMPLATES[2],
            video1_file.name,
            video2_file.name,
            chat_file.name,
            meta_file.name,
            url,
            *self.__parse_xml_meta(
                meta_file,
                "meta/meetingName",
                "start_time"
            ),
        )

    @staticmethod
    def __parse_xml_chat(chat_file):

        """
        :param chat_file: path of chat file
        :return: yield formatted chat history
        """

        etree_root = xml.etree.ElementTree.parse(chat_file)

        for element in etree_root.findall("chattimeline"):
            yield "<b>[{0}]</b>:<br>{1}<br>".format(
                element.attrib["name"],
                element.attrib["message"]
            )

    @staticmethod
    def __parse_xml_meta(meta_file, *args):

        """
        :param meta_file:
        :param args: path of meta file
        :return:
        """

        etree_root = xml.etree.ElementTree.parse(meta_file)

        # TODO: get more infos from meta
        for match in args:

            text = etree_root.findtext(match, "unknown")

            # convert timestamps
            if match.endswith("_time"):

                text = int(text) / 1000
                text = datetime.datetime.fromtimestamp(text)
                text = text.strftime("Date: %d.%m.%Y Time: %H:%M")

            yield text

    def save(self, output_directory: pathlib.Path):

        """
        :param output_directory: directory for saveing webview_file
        :return: webview_file
        """

        webview_file = output_directory.joinpath("webview.html")
        webview_file.write_text(self.__html)

        return webview_file
