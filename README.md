# BigBlueButtonDownloader
##### BigBlueButton Video Downloader

<p align="center">
  <img src="https://repository-images.githubusercontent.com/331634964/0abaea80-5c90-11eb-80e0-4413ca30e08a" />
</p>

Install [Python 3](https://www.python.org/downloads/) on your operating system.  

```
sudo apt install python3
```

Or use the [Microsoft Store](https://go.microsoft.com/fwlink?linkID=2082640) to install Python 3.

### RUN STANDALONE PYTHON APPLICATION

Run the following **zipapp.sh** file to create a standalone Python 3 application.  
Otherwise, you can download and run the [latest release](https://github.com/Th3R3alDuk3/BigBlueButtonDownloader/releases) - 
[bbbdownloader_v1.0.zip](https://github.com/Th3R3alDuk3/BigBlueButtonDownloader/files/5860274/bbbdownloader_v1.0.zip). 

```
usage: python downloader.pyz [-h] 
                   [--webview_title STRING] 
                   [--webview_start STRING]
                   output_directory url

positional arguments:
  output_directory
  url

optional arguments:
  -h, --help            show this help message and exit
  --webview_title STRING
  --webview_start STRING   
```
Use following command to download webcams- and deskshare-video.
```
python downloader.pyz meeting https://website.org/playback/presentation/2.0/playback.html?meetingId=123...
```

##### USE WEBVIEW

Open the **output_directory/webview.html** file in your Browser and enjoy!
