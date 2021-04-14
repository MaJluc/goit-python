import pathlib
import sys
def recursive_print(path):
    pic=[]
    vid=[]
    doc=[]
    musc=[]
    arch=[]
    unknown=[]
    file_type=set()
    unknown_type=set()
    if path.is_dir():
        for element in path.iterdir():
            recursive_print(element)
    else:
        if path.suffix(path) in ('JPEG', 'PNG', 'JPG', 'SVG'):
            pic.append(path.name)
            file_type.add(path.suffix)
        elif path.suffix(path) in ('AVI', 'MP4', 'MOV', 'MKV'):
            vid.append(path.name)
            file_type.add(path.suffix)
        elif path.suffix(path) in ('DOC', 'DOCX', 'TXT', 'PDF', 'XLSX', 'PPTX'):
            doc.append(path.name)
            file_type.add(path.suffix)
        elif path.suffix(path) in ('MP3', 'OGG', 'WAV', 'AMR'):
            musc.append(path.name)
            file_type.add(path.suffix)
        elif path.suffix(path) in ('ZIP', 'GZ', 'TAR'):
            arch.append(path.name)
            file_type.add(path.suffix)
        else:
            unknown.append(path.name)
            unknown_type.add(path.suffix)
    return pic
    return vid
    return doc
    return musc
    return arch
    return unknown
    return file_type
    return unknown_type
def main():
    path = sys.argv[1]
    path = pathlib.Path(path)
    recursive_print(path)
if __name__ == '__main':
    main()
