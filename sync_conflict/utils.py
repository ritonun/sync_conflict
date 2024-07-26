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