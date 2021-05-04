import pathlib
import sys
import re
import shutil
import os
def normalize(text):
    slovar = {'а':'a','б':'b','в':'v','г':'g','д':'d','е':'e','ё':'e',
      'ж':'zh','з':'z','и':'i','й':'i','к':'k','л':'l','м':'m','н':'n',
      'о':'o','п':'p','р':'r','с':'s','т':'t','у':'u','ф':'f','х':'h',
      'ц':'c','ч':'cz','ш':'sh','щ':'scz','ъ':'','ы':'y','ь':'','э':'e',
      'ю':'u','я':'ja', 'А':'A','Б':'B','В':'V','Г':'G','Д':'D','Е':'E','Ё':'E',
      'Ж':'ZH','З':'Z','И':'I','Й':'I','К':'K','Л':'L','М':'M','Н':'N',
      'О':'O','П':'P','Р':'R','С':'S','Т':'T','У':'U','Ф':'F','Х':'H',
      'Ц':'C','Ч':'CZ','Ш':'SH','Щ':'SCH','Ъ':'','Ы':'y','Ь':'','Э':'E',
      'Ю':'U','Я':'YA'}
    for key in slovar:
        text = text.replace(key, slovar[key])
        text=re.sub(r'[^\w\s]', '_', text)
    return text
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
        for element in path.iterdir():
            if element.name in ('video', 'documents', 'archives', 'music', 'images'):
                pass
            else:
                if not os.listdir(path):
                    os.remove(element)
                else:
                    sort_files(element)
    else:
        new_file_name = normalize(pathlib.Path(path).resolve().stem)
        if path.suffix in ('.jpg', '.png', '.jpeg', '.svg'): 
            new_path = f'images/{new_file_name}{path.suffix}'
            os.rename(path,new_path)
        elif path.suffix in ('.avi', '.mp4', '.mov', '.mkv'):                
            new_path = f'video/{new_file_name}{path.suffix}'
            os.rename(path,new_path)
        elif path.suffix in ('.doc', '.docx', '.txt', '.pdf', '.xlsx', '.pptx'):  
            new_path = f'documents/{new_file_name}{path.suffix}'
            os.rename(path,new_path)
        elif path.suffix in ('.mp3', '.ogg', '.wav', '.amr'):   
            new_path = f'music/{new_file_name}{path.suffix}'
            os.rename(path,new_path)
        elif path.suffix in ('.zip', '.gz', '.tar'):   
            new_path = f'archives/{new_file_name}'
            shutil.unpack_archive(path,new_path)
            os.remove(path)
def main():
    path = sys.argv[0]
    path = pathlib.Path()
    sort_files(path)
if __name__ == '__main__':
    main()
