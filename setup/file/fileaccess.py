'''
Simple class to help with file access of the site
'''
import os

def fileaccess_getfilesandfolders(initialpath):
    '''
    Get the files and folders from the initial path
    returns (directorieslist, fileslist)
    '''
    if os.path.exists(initialpath):
        files = list()
        directories = list()
        for value in os.listdir(initialpath):
            if os.path.isdir(os.path.join(initialpath, value)):
                directories.append(value)
            else:
                files.append(value)
        return (directories, files)
    return None

def fileaccess_getuploadspath():
    '''
    gets the upload path of the uploads directory
    '''
    tempbasepath = os.path.dirname(os.path.abspath(__file__)) \
                                   .replace('\\setup', "") \
                                   .replace("/setup", "") \
                                   .replace("\\file", "") \
                                   .replace("/setup", "")
    return os.path.join(tempbasepath, *("static", "uploads"))

def fileaccess_fileexists(folder, file):
    '''
    checks if a file exists in the folder
    '''
    return os.path.isfile(os.path.join(folder, file))
