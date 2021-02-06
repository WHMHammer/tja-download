from bs4 import BeautifulSoup
from csv import reader
from io import BytesIO
from multiprocessing import Process
from os import listdir, mkdir
from pprint import pprint
from requests import get
from time import sleep
from zipfile import BadZipFile, ZipFile

links_dir = "_links"
downloads_dir = "downloads"
sleep_time = 0.01


def download_from_csv(path):
    not_downloaded = []
    with open(path) as f:
        r = reader(f)
        for filename, comment, url in r:
            ext = filename[-4:]
            if ext == ".zip":
                if not download_zip(filename[:-4], comment, url):
                    not_downloaded.append(url)
            elif ext == ".rar":
                if not download_rar(filename[:-4], comment, url):
                    not_downloaded.append(url)
            elif ext in (".mp3", ".ogg", ".tja"):
                if not download_raw(filename, comment, url):
                    not_downloaded.append(url)
            else:
                not_downloaded.append(url)
    pprint(not_downloaded)


def get_download_link(url):
    try:
        token = BeautifulSoup(
            get(url).text,
            features="html.parser"
        ).find(
            "input",
            {"name": "token"}
        )["value"]
    except (KeyError, TypeError):
        return
    finally:
        sleep(sleep_time)  # removing this may cause your IP address to be banned
    try:
        return BeautifulSoup(
            post(href, data={"token": token}).text,
            features="html.parser"
        ).find(
            "a",
            title=compile("をダウンロード$")
        )["href"]
    except (KeyError, TypeError):
        return
    finally:
        sleep(sleep_time)  # removing this may cause your IP address to be banned


def download_zip(filename, comment, url):
    link = get_download_link(url)
    if link is None:
        return False
    try:
        with ZipFile(BytesIO(get(link).content)) as z:
            z.extractall(f"{downloads_dir}/{filename}")
    finally:
        sleep(sleep_time)  # removing this may cause your IP address to be banned
    return True


def download_rar(filename, comment, url):
    return False


def download_raw(filename, comment, url):
    return False


if __name__ == "__main__":
    try:
        mkdir(downloads_dir)
    except FileExistsError:
        pass
    download_from_csv("_links/taikojiro2.83以前・太鼓さん小次郎・tjaplayer専用アップローダ.csv")
    exit()
    processes = []
    for filename in listdir(links_dir):
        if filename[-4:] == ".csv":
            process = Process(
                target=download_from_csv,
                args=(f"{links_dir}/{filename}",)
            )
            process.start()
            processes.append(process)
    for process in processes:
        process.join()
