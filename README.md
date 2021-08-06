# BigBlueButtonDownloader
##### BigBlueButton Video Downloader

<p align="center">
  <img src="https://repository-images.githubusercontent.com/331634964/0abaea80-5c90-11eb-80e0-4413ca30e08a" />
</p>

---

### Support
  
&#x2713; &ensp; webcams video  
&#x2713; &ensp; deskshare video  
&#x2713; &ensp; change video speed  
&#x2713; &ensp; live chat  
&#x2717; &ensp; **shapes/slides not supported!!!**  
  
use [bbb-dl](https://github.com/C0D3D3V/bbb-dl) or docker image [th3r3alduk3/bbb-dl](https://hub.docker.com/r/th3r3alduk3/bbb-dl)

---

Install [Python 3](https://www.python.org/downloads/) on your operating system.  

```
sudo apt install python3
```

Or use the [Microsoft Store](https://go.microsoft.com/fwlink?linkID=2082640) to install Python 3.

### RUN STANDALONE PYTHON APPLICATION

Run the following **zipapp.sh** file to create a standalone Python 3 application.  
Otherwise, you can download and run the [latest release](https://github.com/Th3R3alDuk3/BigBlueButtonDownloader/releases) - 
[bbbdownloader_v1.3.pyz](https://github.com/Th3R3alDuk3/BigBlueButtonDownloader/releases/download/v1.3/downloader.pyz). 

```
usage: python downloader.pyz [-h] 
                   output_directory url

positional arguments:
  output_directory
  url

optional arguments:
  -h, --help            show this help message and exit
```
Use following command to download webcams- and deskshare-video.
```
python downloader.pyz meeting_2021-03-11 https://website.org/playback/presentation/2.0/playback.html?meetingId=123...
```

### Shortcut Keys

| Key | Key Code | Impact  |
|:---:|:---:|---|
| `1` | #49 | video time -= 10 sec |
| `2` | #50 | video time -= 30 sec |
| `3` | #51 | video time -= 60 sec |
| `4` | #52 | video time += 10 sec |
| `5` | #53 | video time += 30 sec |
| `6` | #54 | video time += 60 sec |
| `7` | #55 | video speed = 100% |
| `8` | #56 | video speed = 150% |
| `9` | #57 | video speed = 200% |

##### USE WEBVIEW

Open the **output_directory/webview.html** file in your Browser and enjoy!
