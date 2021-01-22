# BigBlueButtonDownloader
##### BigBlueButton Video Downloader

<p align="center">
  <img src="https://repository-images.githubusercontent.com/331634964/0abaea80-5c90-11eb-80e0-4413ca30e08a" />
</p>

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
