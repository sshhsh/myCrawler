import os
import shutil
import zipfile

import progressbar


def un_zip(zip_name):
    """unzip zip file"""
    zip_file = zipfile.ZipFile(zip_name)

    for names in zip_file.namelist():
        zip_file.extract(names, "temp/")
    zip_file.close()
    for temp_root, temp_dirs, temp_files in os.walk("temp"):
        for temp_name in temp_files:
            temp_path = os.path.join(temp_root, temp_name)
            temp_type = os.path.splitext(temp_name)
            if temp_type[1] == ".txt":
                shutil.move(temp_path, "books_gutenberg/" + temp_name)
            else:
                os.remove(temp_path)
    for temp_root, temp_dirs, temp_files in os.walk("temp"):
        for temp_dir in temp_dirs:
            temp_path = os.path.join(temp_root, temp_dir)
            shutil.rmtree(temp_path)


if not os.path.isdir("books_gutenberg"):
    os.mkdir("books_gutenberg")
if not os.path.isdir("temp"):
    os.mkdir("temp")
path = "gutenberg"
for root, dirs, files in progressbar.progressbar(os.walk(path), redirect_stdout=True):
    for name in files:
        file_path = os.path.join(root, name)
        extra = os.path.splitext(name)
        file_name = extra[0]

        if extra[1] == ".zip":
            index = file_name.find('-')
            if not index == -1:
                file_name2 = file_name[0:index]
                if not os.path.exists("books_gutenberg/" + file_name2 + ".txt"):
                    un_zip(file_path)
                    try:
                        os.rename("books_gutenberg/" + file_name + ".txt", "books_gutenberg/" + file_name2 + ".txt")
                    except Exception as e:
                        print(e)
            else:
                if not os.path.exists("books_gutenberg/" + file_name + ".txt"):
                    un_zip(file_path)
        # if extra[1] == ".zip":
        #     un_zip(file_path)
