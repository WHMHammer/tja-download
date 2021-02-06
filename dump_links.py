from bs4 import BeautifulSoup
from csv import writer
from multiprocessing import Process
from os import mkdir
from requests import get
from time import sleep
from urllib.parse import urlsplit

links_dir = "links"
urls = (  # only ux.getuploader.com URLs are acceptable
    "https://ux.getuploader.com/e2339999zp/",
    "https://ux.getuploader.com/e2337650/",
    "https://ux.getuploader.com/toukyuutoyoko9000/",
    "https://ux.getuploader.com/e2351000/",
    "https://ux.getuploader.com/koganei231/",
    "https://ux.getuploader.com/koganei233/",
    "https://ux.getuploader.com/koganei235/",
    "https://ux.getuploader.com/yokohama205/"
)
sleep_time = 0.01


def dump_links(url):
    page_no = 1
    has_fetched_all = False
    try:
        heading = BeautifulSoup(
            get(url).text,
            features="html.parser"
        ).find("h1").contents[0].strip()
    except (TypeError, IndexError):
        heading = urlsplit(url).path.strip("/")
    finally:
        sleep(sleep_time)  # removing this may cause your IP address to be banned
    with open(f"{links_dir}/{heading}.csv", "w") as f:
        w = writer(f)
        while not has_fetched_all:
            has_fetched_all = True
            page_url = f"{url}index/filename/asc/{page_no}"
            page_records = []
            print(page_url)
            try:
                for tr in BeautifulSoup(
                    get(page_url).text,
                    features="html.parser"
                ).find("tbody").findAll("tr"):
                    has_fetched_all = False
                    comment = tr.findAll("td")[1].string
                    a = tr.find("a")
                    try:
                        page_records.append(
                            (a.string, comment, a["href"])
                        )
                    except KeyError:
                        pass
            except AttributeError:
                print(
                    "The owner of ux.getuploader.com has likely banned your IP address."
                )
                return
            finally:
                # removing this may cause your IP address to be banned
                sleep(sleep_time)
            w.writerows(page_records)
            page_no += 1


if __name__ == "__main__":
    try:
        mkdir(links_dir)
    except FileExistsError:
        pass
    processes = []
    for url in urls:
        process = Process(
            target=dump_links,
            args=(url,)
        )
        process.start()
        processes.append(process)
    for process in processes:
        process.join()
