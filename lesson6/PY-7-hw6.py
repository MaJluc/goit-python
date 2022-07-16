from genericpath import exists
import sys
import pathlib
import shutil
import os


def normalize(name):

    CYRILLIC_SYMBOLS = "абвгдеёжзийклмнопрстуфхцчшщъыьэюяєіїґ"
    TRANSLATION = ("a", "b", "v", "g", "d", "e", "e", "j", "z", "i", "j", "k", "l", "m", "n", "o", "p", "r", "s", "t", "u",
               "f", "h", "ts", "ch", "sh", "sch", "", "y", "", "e", "yu", "ya", "je", "i", "ji", "g")
    TRANS = {}
    for c, l in zip(CYRILLIC_SYMBOLS, TRANSLATION):
        TRANS[ord(c)] = l
        TRANS[ord(c.upper())] = l.upper()       
    b = ""
    a = name.translate(TRANS)
    for i in a:
        if i.lower() not in "abcdefghijklmnopqrstuvwxyz" and i not in "0123456789":
            i = "_"
            b += i
        else:
            b += i
        
    return b


def sort_files(path):
    if not os.path.exists(f'images'):
        os.mkdir(f'images')
    if not os.path.exists(f'video'):
        os.mkdir(f'video')
    if not os.path.exists(f'documents'):
        os.mkdir(f'documents')
    if not os.path.exists(f'archives'):
        os.mkdir(f'archives')
    if not os.path.exists(f'music'):
        os.mkdir(f'music')
    if path.is_dir():
        if len(os.listdir(path)) == 0:
            path.rmdir()
        else:           
            for element in path.iterdir():

                if element.name in ('video', 'documents', 'archives', 'music', 'images'):
                    pass                
                else:
                    sort_files(element)
    else:
        new_file_name = normalize(path.stem)
        if path.suffix.upper() in ('.JPEG', '.PNG', '.JPG', '.SVG'): 
            os.replace(path, f'.\\images\\{new_file_name}{path.suffix}')
        if path.suffix.upper() in ('.AVI', '.MP4', '.MOV', '.MKV'): 
            os.replace(path, f'.\\video\\{new_file_name}{path.suffix}')
        if path.suffix.upper() in ('.DOC', '.DOCX', '.TXT', '.PDF', '.XLSX', '.PPTX'): 
            os.replace(path, f'.\\documents\\{new_file_name}{path.suffix}')
        if path.suffix.upper() in ('.MP3', '.OGG', '.WAV', '.AMR'): 
            os.replace(path, f'.\\music\\{new_file_name}{path.suffix}')
        if path.suffix.upper() in ('.ZIP', '.GZ', '.TAR'):
            new_path = f'.\\{new_file_name}{path.suffix.lower()}'
            new_path_nosuffix = f'.\\{new_file_name}'
            os.rename(path, new_path) 
            path = new_path
            os.mkdir(f'.\\archives\\{new_file_name}')
            shutil.unpack_archive(path, f'.\\archives\\{new_file_name}')
            os.remove(path)


def main():
    path = sys.argv[1]
    path = pathlib.Path(path)
    sort_files(path)


if __name__ == '__main__':
    main()

