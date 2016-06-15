import os

def os_getfilesandfolders(initialpath):
    if os.path.exists(initialpath):
        files = list()
        dir = list()
        for f in os.listdir(initialpath):
            if (os.path.isdir(os.path.join(initialpath, f))):
                dir.append(f)
            else:
                files.append(f)
        return (dir, files)
    return None

def os_getuploadspath():
    tempbasepath = os.path.dirname(os.path.abspath(__file__)).replace('\\setup', "").replace("/setup", "").replace("\\file", "").replace("/setup", "")
    return os.path.join(tempbasepath, *("static", "uploads"))

def os_fileexists(folder, file):
    return os.path.isfile(os.path.join(folder, file))