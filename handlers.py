from __future__ import print_function
import utils
import logging

logging.basicConfig(level=logging.DEBUG, format="%(asctime)s - %(levelname)s - %(message)s")


def handle_empty(directories, action):
    if action == 'n':
        return

    file_paths = utils.detect_empty(directories)
    print('\nFound {} empty files'.format(len(file_paths)))
    if action == 'y':
        utils.remove_files(file_paths)
    elif action == 'ask':
        for file_path in file_paths:
            if utils.get_decision("{} is empty. Remove it?".format(file_path)):
                utils.remove_files([file_path])


def handle_temporary(directories, temp_suffixes, action):
    if action == 'n':
        return

    file_paths = utils.detect_temporary(directories, temp_suffixes)
    print('\nFound {} temporary files'.format(len(file_paths)))
    if action == 'y':
        utils.remove_files(file_paths)
    elif action == 'ask':
        for file_path in file_paths:
            if utils.get_decision("{} is temporary. Remove it?".format(file_path)):
                utils.remove_files([file_path])


def handle_abnormal_permissions(directories, default_access, action):
    if action == 'n':
        return

    file_paths = utils.detect_invalid_permissions(directories, default_access)
    print('\nFound {} files with abnormal permissions'.format(len(file_paths)))
    if action == 'y':
        utils.change_permissions(file_paths, default_access)
    if action == 'ask':
        for file_path in file_paths:
            if utils.get_decision("{} has wrong permissions. Change it?".format(file_path)):
                utils.change_permissions([file_path], default_access)


def handle_symbols_in_name(directories, tricky_letters, substitute, action):
    if action == 'n':
        return

    file_paths = utils.detect_problematic_names(directories, tricky_letters)
    print('\nFound {} files with problematic names'.format(len(file_paths)))
    for file_path in file_paths:
        if action == 'y' or (action == 'ask' and utils.get_decision("{} contains problematic chars. Rename it?".format(file_path))):
            utils.change_file_name(file_path, tricky_letters, substitute)


def handle_duplicates(directories, action):
    if action == 'n':
        return

    duplicates = utils.detect_duplicates(directories)
    print('\nFound {} sets of files with same content'.format(len(duplicates)))
    for files in duplicates.values():
        try:
            oldest = utils.get_oldest_file(files)
            other = [file for file in files if file != oldest]
            if action == 'y':
                utils.remove_files(other)
            if action == 'ask':
                for file in other:
                    if utils.get_decision("{} is copy of {}. Remove it?".format(file, oldest)):
                        utils.remove_files([file])
        except ValueError:
            logging.warning('Could not handle duplicates among group: {}'.format(files))
            continue


def handle_same_name(directories, action):
    if action == 'n':
        return

    same_name = utils.detect_same_name(directories)
    print('\nFound {} sets of files with same name'.format(len(same_name)))
    for files in same_name.values():
        try:
            newest = utils.get_newest_file(files)
            other = [file for file in files if file != newest]
            if action == 'y':
                utils.remove_files(other)
            if action == 'ask':
                for file in other:
                    if utils.get_decision("{} is older than {}. Remove it?".format(file, newest)):
                        utils.remove_files([file])
        except ValueError:
            logging.warning('Could not handle same name files among group: {}'.format(files))
            continue


def handle_missing_in_main(main_dir, other_dirs, action):
    if action == 'n':
        return

    missing = utils.detect_not_in_main_dir(main_dir, other_dirs)
    print('\nFound {} files missing in main directory'.format(len(missing)))
    for file_path in missing:
        if action == 'y' or (action == 'ask' and utils.get_decision("{} is not in {}. Move it?".format(file_path, main_dir))):
            utils.move_file_to_main_dir(file_path, main_dir)
