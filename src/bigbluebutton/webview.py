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

    def __init__(self, chat_file: pathlib.Path, meta_file: pathlib.Path, url: str):

        """
        :param chat_file: path of chat file
        :param meta_file: path of meta file
        """

        # CEATE HTML CONTENT

        self.__html = self.__TEMPLATES[0].format(
            self.__TEMPLATES[1],
            self.__TEMPLATES[2],
            url, "".join(
                self.__parse_xml_chat(chat_file)
            ),
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
        :return: yield formatted chat messages
        """

        etree_root = xml.etree.ElementTree.parse(chat_file)

        for element in etree_root.findall("chattimeline"):
            yield """
            <div class="message" seconds="{0}">
                <span class="time">{3}</span>&ensp;
                <span class="name">{1}</span>
                <p class="text">{2}</p>
            </div>
            """.format(
                element.attrib["in"],
                element.attrib["name"],
                element.attrib["message"],
                datetime.timedelta(
                    seconds=int(element.attrib["in"])
                ),
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
        webview_file.write_text(self.__html, encoding="utf-8")

        return webview_file
