from bs4 import BeautifulSoup
from csv import writer
from multiprocessing import Process, Queue
from os import mkdir
from os.path import join
from requests import get

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


def dump_links(url, q):
    page_no = 1
    has_fetched_all = False
    try:
        heading = BeautifulSoup(
            get(url).text,
            features="html.parser"
        ).find("h1").contents[0].strip()
    except (TypeError, IndexError):
        print("The url you entered is not acceptable")
        return
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
            q.put(page_url)
    with open(join(links_dir, heading+".csv"), "w") as f:
        w = writer(f)
        w.writerows(page_records)
    page_no += 1


if __name__ == "__main__":
    try:
        mkdir(links_dir)
    except FileExistsError:
        pass
    q = Queue()
    """  The following part is commented out because it's so fast that the ux.getuploader.com will ban your IP address
    processes = []
    for url in urls:
        process = Process(
            target=dump_links,
            args=(url, q)
        )
        process.start()
        processes.append(process)
    for process in processes:
        process.join()
    """
    for url in urls:
        dump_links(url, q)
    print("Failed pages:")
    while not q.empty():
        print(q.get())
