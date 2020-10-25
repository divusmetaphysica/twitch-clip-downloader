import argparse
import asyncio
import functools
import json
import logging
import re
from dataclasses import dataclass
from pathlib import Path
from typing import List, Set

import aiofiles
import aiohttp

logging.basicConfig(format="[%(levelname)s]: %(message)s", level=logging.INFO)
allowed_characters = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789_- .'[]"
old_files: Set[Path] = set()  # Used as a global previous file name cache


@dataclass(frozen=True)
class Link:
    __slots__ = ["link", "title"]
    link: str
    title: str


async def load_config(config_file: Path) -> List[Link]:
    async with aiofiles.open(str(config_file), mode="r", encoding="utf-8") as file:
        data = json.loads(await file.read())
    logging.info(f"Found {len(data)} clips in {config_file}")
    return [Link(**obj) for obj in data]


async def download_clips(session: aiohttp.ClientSession, target_dir: Path, entry: Link) -> None:
    async with session.get(entry.link) as resp:
        if resp.status == 200:
            contents = await resp.read()
        else:
            contents = None

    if contents is None:
        logging.warning(f"No content {entry.title}")
        return entry.title

    filtered_title = "".join(c for c in entry.title if c in allowed_characters)
    file_name = target_dir / f"{filtered_title}.mp4"

    if file_name.exists():
        last_file = sorted(
            [
                target_dir / f"{file_name.stem} (0){file_name.suffix}",  # add original 0th
                *(file for file in old_files if file.name.startswith(file_name.stem))
            ]
        )[-1]
        last_count = int(last_file.name.rsplit("(", 1)[-1].rsplit(")", 1)[0])
        file_name = target_dir / f"{file_name.stem} ({last_count+1}){file_name.suffix}"

    async with aiofiles.open(file_name, mode="wb") as stream:
        await stream.write(contents)

    logging.info(f"Downloaded clip {entry.title}")


async def main(links_file: Path, target_dir: Path):
    clips: List[Link] = await load_config(links_file)

    logging.info("Starting downloads")
    async with aiohttp.ClientSession() as session:
        fun = functools.partial(download_clips, session=session, target_dir=target_dir)
        await asyncio.gather(*[fun(entry=entry) for entry in clips])
    logging.info("Finished")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Twitch clip download tool")
    parser.add_argument("--file", default="clips.json", help="Name of the clip name json file")
    parser.add_argument(
        "--output-dir", default="downloads", help="Directory to download the clips"
    )
    args = parser.parse_args()

    links_file, target_dir = Path(args.file), Path(args.output_dir)
    if not target_dir.exists():
        target_dir.mkdir()
    old_files = set(target_dir.glob("*(*).txt"))

    loop = asyncio.get_event_loop()
    loop.run_until_complete(main(links_file, target_dir))
