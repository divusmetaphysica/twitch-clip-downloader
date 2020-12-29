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