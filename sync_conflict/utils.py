import os


def index_all_files(folder_path):
    """ find all files in a folder """
    paths = []
    for root, dirs, files in os.walk(folder_path):
        for file in files:
            paths.append(os.path.join(root, file))
    return paths


def get_sync_conflict_files(files):
    """ find all files containing 'conflict' within a list of files """
    conflicted_files = []
    for name in files:
        if 'conflict'in name.split('/')[-1]:
            conflicted_files.append(name)
    return conflicted_files


def get_stat_dict(file_path):
    data = {}

    stat = os.stat(file_path)
    data['size'] = stat['st_size']
    data['creation_date'] = stat['st_ctime']
    data['modified_date'] = stat['st_mtime']
    data['last_access_date'] = stat['st_atime']

    return data



def resolve_conflict(conflict_file_path):
    conflict_file = {}
    original_file = {}

    # get dir path
    path = os.path.split(conflict_file_path)

    dir_path = ''
    for i in range(len(path) - 1):
        dir_path = os.path.join(dir_path, path[i])

    # get conflict file name (remove dir path)
    conflict_file['name'] = path[-1]

    # get original file name 
    split_name = conflict_file['name'].split('.')
    del split_name[len(split_name) - 2]
    name = ''
    for i in split_name:
        name += i + '.'
    original_file['name'] = name[:-1]

    # dictionnary for file stat

    # name: name
    # size (kb): st_size in bytes
    # creation_date : st_ctime
    # modified date: st_mtime
    # last access date: st_atime


    print(os.stat(os.path.join(dir_path, conflict_file['name'])))
    print(os.stat(os.path.join(dir_path, original_file['name'])))
    print('\n')