import json
import time
import requests
import logging
from pathlib import Path
from concurrent.futures import ThreadPoolExecutor
from contextlib import contextmanager

logging.basicConfig(format='[%(levelname)s]: %(message)s', level=logging.INFO)
num_of_workers = 10
allowed_characters = 'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789_- .'
target_dir = Path('downloaded')
if not target_dir.exists():
    target_dir.mkdir()


@contextmanager
def timer(description: str):
    start = time.time_ns()
    yield
    end = time.time_ns()
    logging.warning(f'{description} took {(end-start)/1e6:.2f}ms')


def download_link(entry) -> Path:
    link, title = entry['link'], entry['title']  # Each object contains keys title, link

    logging.info(f'Processing: {title}')
    try:
        request = requests.get(link, allow_redirects=True)
    except Exception as e:
        logging.error(f'Failed title: {title}', exc_info=e)

    filtered_title = ''.join(c for c in title if c in allowed_characters)
    file_name = target_dir / f'{filtered_title}.mp4'

    if file_name.is_file():
        stem, ext = file_name.stem, file_name.suffix
        for i in range(2, 100):
            file_name = target_dir / f'{stem} ({i}){ext}'
            if not file_name.is_file():
                break

    with file_name.open('wb') as file:
        file.write(request.content)

    return file_name


with ThreadPoolExecutor(max_workers=num_of_workers) as executor:
    with open('clips.json', encoding='utf8') as file:
        data = json.load(file)

    files = executor.map(download_link, data)

logging.info('Finished all downloads.')
