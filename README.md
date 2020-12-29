# Twitch Clip Downloader

## Initial preparations

- Download and install python from here https://www.python.org/downloads/ (Tested on Python 3.7 and 3.8 on Windows 10 but newer version most likely will work as well)
- Download https://github.com/divusmetaphysica/twitch-clip-downloader/archive/main.zip
- Extract the **twitch-clip-downloader-main** folder from the ZIP
- Go to the new **twitch-clip-downloader-main** folder
- In the location bar type `cmd` then `<Enter key>`
- Enter the following lines in the **cmd.exe** window:
```bash
python -m venv --copies .venv
.venv\Scripts\activate.bat
python.exe -m pip install -r requirements.txt
```

## How to run?

### First: Download a list of all your clips

- Open your browser
- Log in to twitch if you are not already logged in
- Go to: https://www.twitch.tv/manager/clips
- Hold the `<End Key>` to scroll down and preload all the clip links otherwise the script won't be able to find them all
- Press F12 to open the dev tools of the browser
- Select the Console tab in the dev tools
- Pick one of ["fast"](https://raw.githubusercontent.com/divusmetaphysica/twitch-clip-downloader/main/get_metadata_without_dates.js) or ["slow but has clip date"](https://raw.githubusercontent.com/divusmetaphysica/twitch-clip-downloader/main/get_metadata_with_dates.js) and paste the contents of that script in there 
- Press enter
- A file called **clips.json** should now download
- Move the downloaded file to the **twitch-clip-downloader-main** folder and make sure the name is **clips.json** (might not be the case any more if you do this again)

### Now that we have a list, let's do the actual download

- Open the file explorer
- Go to the **twitch-clip-downloader-main** folder
- In the location bar type `cmd` then `<Enter key>`
- Enter the following lines in the **cmd.exe** window:
```bash
.venv\Scripts\activate.bat
python.exe clip_downloader.py
``` 
- There should now be a folder called **downloaded** with your clips in it