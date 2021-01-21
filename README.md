# BigBlueButtonDownloader
##### BigBlueButton Presentation Downloader

Install required dependencies.
```
pip install tqdm
python -m pip install tqdm
```

Use following command to download webcams- and deskshare-video.
```
python download.py [-h] output_directory url
python download.py meeting https://mywebsite.org/playback/presentation/2.0/playback.html?meetingId=3a309914f0...
```

Open the **output_directory/webview.html** file in your Browser and enjoy!
