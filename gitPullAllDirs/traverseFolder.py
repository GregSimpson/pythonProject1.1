import os

# /home/gsimpson/gjs/git_stuff/RealPlay

def traverse(startDir):
    t_folders = []
    t_files = []

    for entry in os.scandir(startDir):
        if entry.is_dir():
            t_folders.append(entry.path)
        elif entry.is_file():
            t_files.append(entry.path)
    return sorted(t_folders, key=str.lower), sorted(t_files)

if __name__ == "__main__":
    #folders = []
    #files = []

    folders, files = traverse('/home/gsimpson/gjs/git_stuff')

    #print("Folders:\n\t {0} : \n\nFiles:\n\t {1} ".format(folders, files))

    for eachProject in folders:
        os.chdir(eachProject)
        print(os.getcwd())
        os.system("git pull")
        #os.system("cd " + eachProject)
        #print(os.path.basename(eachProject) )
