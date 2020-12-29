(function () {
    // wait time between requests, less might be faster but is more risky
    const WAIT_TIME = 500;

    // find all images on the page (even those unrelated to our clips)
    const relevantImageTags = [...document.getElementsByTagName('img')]
        // only keep the ones that have promising URLs (there are many other images apart from clip thumbnails and we
        // don't want those
        .filter(o => o.src.match(/https...clips-media/));

    const total = relevantImageTags.length;
    let linksAndTitles = [];
    let current = null;

    // let's go
    next();

    function tryAppendDate() {
        // try to retrieve the date of the clip (this is more likely to fail than other things so we just continue if
        // it didn't work (slow requests for example)
        try {
            var date = document.getElementsByClassName('tw-capcase tw-ellipsis')[0].innerText;
            //current.title += ' - ' + date;
            //console.log('Processing ' + linksAndTitles.length + '/' + total + ' (extracted clip date)');
            var views = document.getElementsByClassName('tw-pd-l-05')[0].innerText;
            var d = new Date(date);
            date = d.getFullYear() + "-" + (d.getMonth() + 1) + "-" + d.getDate();
            current.title = date + ' ' + current.title + ' [' + views + ']'
        } catch (e) {
            console.error(e);
        }
    }

    function next() {
        if (current) {
            tryAppendDate();
        }
        if (relevantImageTags.length) {
            console.log('Processing ' + (linksAndTitles.length + 1) + '/' + total);
            const img = relevantImageTags.pop();
            current = {
                // build the clip URL from the preview URL
                link: img.src.replace('-preview-260x147.jpg', '.mp4'),
                // try to make a title for the clip
                title: img.parentNode.parentNode.nextSibling.innerText + ' - ' + img.nextSibling.innerText
            };
            linksAndTitles.push(current);

            // click on the table row
            img.parentNode.parentNode.parentNode.parentNode.click();
            // wait for twitch to fetch things with graph query language
            setTimeout(next, WAIT_TIME);
        } else {
            end();
        }
    }

    function end() {
        // transform the output to a text format (JSON)
        const outputAsJson = JSON.stringify(linksAndTitles, null, 2);

        // trigger a download
        const link = document.createElement('a');
        link.href = URL.createObjectURL(new Blob([outputAsJson], {
            type: 'application/octet-stream'
        }));
        link.download = 'clips.json';
        link.click();
    }
})();