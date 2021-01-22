# BigBlueButtonDownloader
##### BigBlueButton Video Downloader

<p align="center">
  <img src="https://repository-images.githubusercontent.com/331634964/0abaea80-5c90-11eb-80e0-4413ca30e08a" />
</p>

Install required dependencies.
```
pip install -r requirements.txt
python -m pip install -r requirements.txt
```

Use following command to download webcams- and deskshare-video.

```
usage: download.py [-h] [--webview_title STRING] [--webview_timestamp STRING]
                   [--webview_video1_height INTEGER]
                   [--webview_video2_height INTEGER]
                   output_directory url

positional arguments:
  output_directory
  url

optional arguments:
  -h, --help            show this help message and exit
  --webview_title STRING
  --webview_timestamp STRING
  --webview_video1_height INTEGER
  --webview_video2_height INTEGER
```

```
python download.py meeting https://website.org/playback/presentation/2.0/playback.html?meetingId=123...
```

Open the **output_directory/webview.html** file in your Browser and enjoy!
