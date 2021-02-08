from multiprocessing import Process, Queue
from os import listdir, makedirs
from os.path import dirname, join
from shutil import copyfile
from zipfile import BadZipFile, ZipFile

downloads_dir = "downloads"
extracted_dir = "extracted"


def extract_all(dir_path, q):
    try:
        makedirs(join(extracted_dir, dir_path))
    except FileExistsError:
        pass
    for filename in listdir(join(downloads_dir, dir_path)):
        print(filename)
        ext = filename[-4:]
        if ext == ".zip":
            if not extract_zip(dir_path, filename):
                q.put(join(dir_path, filename))
        elif ext == ".rar":
            if not extract_rar(dir_path, filename):
                q.put(join(dir_path, filename))
        elif ext in (".mp3", ".ogg", ".tja"):
            copyfile(
                join(downloads_dir, dir_path, filename),
                join(extracted_dir, dir_path, filename)
            )
        else:
            q.put(join(dir_path, filename))


def extract_zip(dir_path, filename):
    with open(join(downloads_dir, dir_path, filename), "rb") as f:
        try:
            with ZipFile(f) as z:
                for raw_name in z.namelist():
                    try:
                        name = raw_name.encode("cp437").decode("cp932")
                    except UnicodeError:
                        name = raw_name
                    dir_name = dirname(name)
                    if dir_name:
                        try:
                            makedirs(join(extracted_dir, dir_path, dir_name))
                        except FileExistsError:
                            pass
                    with open(join(extracted_dir, dir_path, name), "wb") as target_f:
                        target_f.write(z.read(raw_name))
        except BadZipFile:
            return False
    return True


def extract_rar(dir_path, filename):
    return False


if __name__ == "__main__":
    q = Queue()
    processes = []
    for dir_path in listdir(downloads_dir):
        process = Process(
            target=extract_all,
            args=(join(dir_path, "本家"), q)
        )
        process.start()
        processes.append(process)
        process = Process(
            target=extract_all,
            args=(join(dir_path, "others"), q)
        )
        process.start()
        processes.append(process)
    print("Not extracted:")
    while not q.empty():
        print(q.get())
