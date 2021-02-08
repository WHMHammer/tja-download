from multiprocessing import Process, Queue
from os import listdir, makedirs
from os.path import dirname, join
from rarfile import BadRarFile, RarCannotExec, RarFile
from shutil import copyfile
from zipfile import BadZipFile, ZipFile

downloads_dir = "downloads"
extracted_dir = "extracted"
raw_formats = (".m4a", ".mp3", ".ogg", ".tja")
src_codecs = (
    "cp437",
    "utf-8"
)
dest_codecs = (
    "utf-8",
    "cp932"
)


def extract_all(dir_path, q):
    try:
        makedirs(join(extracted_dir, dir_path))
    except FileExistsError:
        pass
    for filename in listdir(join(downloads_dir, dir_path)):
        print(filename)
        ext = filename[-4:]
        if ext in (".zip", ".rar"):
            if not extract(dir_path, filename):
                q.put(join(dir_path, filename))
        elif ext in raw_formats:
            copyfile(
                join(downloads_dir, dir_path, filename),
                join(extracted_dir, dir_path, filename)
            )
        else:
            q.put(join(dir_path, filename))


def extract(dir_path, filename):
    ext = filename[-4:]
    if ext == ".zip":
        File = ZipFile
        BadFile = BadZipFile
    elif ext == ".rar":
        File = RarFile
        BadFile = BadRarFile
    else:
        return False
    with open(join(downloads_dir, dir_path, filename), "rb") as f:
        try:
            with File(f) as archive:
                for raw_name in archive.namelist():
                    if raw_name[-4:] not in raw_formats:
                        continue
                    name = recode(raw_name)
                    dir_name = dirname(name)
                    if dir_name:
                        try:
                            makedirs(join(extracted_dir, dir_path, dir_name))
                        except FileExistsError:
                            pass
                    try:
                        with open(join(extracted_dir, dir_path, name), "wb") as target_f:
                            target_f.write(archive.read(raw_name))
                    except IsADirectoryError:
                        continue
        except (BadFile, RarCannotExec):
            return False
    return True


def recode(s):
    for src_codec in src_codecs:
        try:
            encoded = s.encode(src_codec)
        except UnicodeEncodeError:
            continue
        for dest_codec in dest_codecs:
            if src_codec == dest_codec:
                continue
            try:
                return encoded.decode(dest_codec)
            except UnicodeDecodeError:
                pass
    return s


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
    for process in processes:
        process.join()
    print("Not extracted:")
    while not q.empty():
        print(q.get())
