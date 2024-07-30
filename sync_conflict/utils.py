import os
import sys
import subprocess
from datetime import datetime
import click


def check_folder_exist(path):
    if not os.path.isdir(path):
        click.echo(f'The path "{path}" is not a folder or does not exist.')
        sys.exit(0)
    return True


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
    data['size'] = stat.st_size
    data['creation_date'] = stat.st_ctime
    data['modified_date'] = stat.st_mtime
    data['last_access_date'] = stat.st_atime

    return data


def get_file_name(file_path):
    conflict_name = os.path.basename(file_path)

    name_split = conflict_name.split('.')
    original_name = ''
    for string in name_split:
        if not 'sync-conflict' in string:
            original_name += string + '.'
    original_name = original_name[:-1]
    return original_name, conflict_name



def resolve_conflict(conflict_file_path):
    # if sync_conflict is folder name, skip
    if 'sync_conflict' in conflict_file_path:
        click.echo(f'The file {conflict_file_path} can not be resolve.')
        click.echo('A folder name contain "sync_conflict", please rename the folder.')
        return False

    # get file name of conflict file & original file
    original_name, conflict_name = get_file_name(conflict_file_path)

    # get directory of conflict file location
    dir_path = conflict_file_path.replace(conflict_name, '')

    # get metadata of files
    original = get_stat_dict(os.path.join(dir_path, original_name))
    original['name'] = original_name
    conflict = get_stat_dict(os.path.join(conflict_file_path))
    conflict['name'] = conflict_name

    # resolve conflict
    # 

    if conflict['size'] < original['size'] and conflict['modified_date'] < original['modified_date']:
        os.remove(conflict_file_path)
        click.echo(f'Removed "{conflict_name}" in "{dir_path}"')
        return True
    else:
        click.echo(f'Could not solve conflict for "{conflict_file_path}"')
        datetime_string = str(datetime.utcfromtimestamp(original['modified_date']))
        datetime_string += ' (original)|(conflict) '
        datetime_string += str(datetime.utcfromtimestamp(conflict['modified_date']))
        click.echo(datetime_string)
        size_string = str(original['size']) + ' (original)|(conflict) ' + str(conflict['size'])
        click.echo(size_string)
        click.echo('---')
        return False


def open_file_explorer(path):
    """Open file explroer at the specified path """
    path = os.path.dirname(os.path.abspath(path))
    if sys.platform == "win32": # windows
        os.startfile(path)
    else:
        if sys.platform == "darwin":    # mac
            opener = "open"
        else:
            opener = "xdg-open" # unix
        subprocess.Popen([opener, path])
