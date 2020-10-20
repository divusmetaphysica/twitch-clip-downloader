# Twitch Clip Downloader

## Environment

Tested on Python 3.7 and 3.8 on Windows 10

```bash
git clone https://github.com/divusmetaphysica/twitch-clip-downloader.git
cd twitch-clip-downloader/
python -m venv --copies .venv
.venv/Scripts/activate

python.exe -m pip install -r requirements.txt
```

## How to run?

### First: Download a list of all your clips

- Open your browser
- Log in to twitch if you are not already logged in
- Go to: https://www.twitch.tv/manager/clips
- Make sure to scroll down if you have a lot of clips so that all of them are pre-loaded otherwise the script won't be able to find them all
- Press F12 to open the dev tools of the browser
- Select the Console tab in the dev tools
- Paste the following code in there:

```javascript
// find all images on the page (even those unrelated to our clips)
const allImageTags = [...document.getElementsByTagName('img')];

// filter and transform
const linksAndTitles = allImageTags
    // only keep the ones that have promising URLs (there are many other images apart from clip thumbnails and we
    // don't want those
    .filter(o => o.src.match(/https...clips-media/))
    .map(o => {
        return {
            // build the clip URL from the preview URL
            link: o.src.replace('-preview-260x147.jpg', '.mp4'),
            // try to make a title for the clip
            title: o.parentNode.parentNode.nextSibling.innerText + ' - ' + o.nextSibling.innerText
        }
    });

// transform the output to a text format (JSON)
const outputAsJson = JSON.stringify(linksAndTitles, null, 2);

// trigger a download
const link = document.createElement('a');
link.href = URL.createObjectURL(new Blob([outputAsJson], {
    type: 'application/octet-stream'
}));
link.download = 'clips.json';
link.click();
``` 
- Press enter
- A file called **clips.json** should now download
- Move the downloaded file to the **twitch-clip-downloader** folder and make sure the name is **clips.json** (might not be the case any more if you do this again)

### Now that we have a list, let's do the actual download

- Open the file explorer
- Go to the **twitch-clip-downloader** folder
- In the location bar type `cmd` then `<Enter key>`
- Type `python.exe clip_downloader.py` followed by `<Enter key>` 
- There should now be a folder called **downloaded** with your clips in it