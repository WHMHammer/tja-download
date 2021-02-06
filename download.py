from bs4 import BeautifulSoup
from csv import reader
from multiprocessing import Process, Queue
from os import listdir, makedirs
from re import compile
from requests import get, post
from time import sleep

links_dir = "links"
downloads_dir = "downloads"
sleep_time = 0.01


def download_from_csv(csv_filename, q):
    try:
        makedirs(f"{downloads_dir}/{csv_filename[:-4]}/本家")
    except FileExistsError:
        pass
    try:
        makedirs(f"{downloads_dir}/{csv_filename[:-4]}/others")
    except FileExistsError:
        pass
    with open(f"{links_dir}/{csv_filename}") as csv_f:
        r = reader(csv_f)
        for filename, comment, url in r:
            print(filename)
            if "本家" in comment:
                target_dir = f"{downloads_dir}/{csv_filename[:-4]}/本家/"
            else:
                target_dir = f"{downloads_dir}/{csv_filename[:-4]}/others/"
            with open(target_dir+filename, "wb") as f:
                link = get_download_link(url)
                if link is None:
                    q.put(url)
                    continue
                try:
                    f.write(get(link).content)
                finally:
                    # removing this may cause your IP address to be banned
                    sleep(sleep_time)


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
            post(url, data={"token": token}).text,
            features="html.parser"
        ).find(
            "a",
            title=compile("をダウンロード$")
        )["href"]
    except (KeyError, TypeError):
        return
    finally:
        sleep(sleep_time)  # removing this may cause your IP address to be banned


if __name__ == "__main__":
    q = Queue()
    processes = []
    for filename in listdir(links_dir):
        if filename[-4:] == ".csv":
            process = Process(
                target=download_from_csv,
                args=(filename, q)
            )
            process.start()
            processes.append(process)
    for process in processes:
        process.join()
    print("Not downloaded:")
    while not q.empty():
        print(q.get())
