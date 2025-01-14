import utils
import logging

logging.basicConfig(level=logging.DEBUG, format="\n%(asctime)s - %(levelname)s - %(message)s")


def handle_empty(directories, action: str):
    if action == 'n':
        return

    file_paths = utils.detect_empty(directories)
    print(f'\nFound {len(file_paths)} empty files')
    if action == 'y':
        utils.remove_files(file_paths)
    elif action == 'ask':
        for file_path in file_paths:
            if utils.get_decision(f"{file_path} is empty. Remove it?"):
                utils.remove_files([file_path])


def handle_temporary(directories, temp_suffixes, action):
    if action == 'n':
        return

    file_paths = utils.detect_temporary(directories, temp_suffixes)
    print(f'\nFound {len(file_paths)} temporary files')
    if action == 'y':
        utils.remove_files(file_paths)
    elif action == 'ask':
        for file_path in file_paths:
            if utils.get_decision(f"{file_path} is temporary. Remove it?"):
                utils.remove_files([file_path])


def handle_abnormal_permissions(directories, default_access, action):
    if action == 'n':
        return

    file_paths = utils.detect_invalid_permissions(directories, default_access)
    print(f'\nFound {len(file_paths)} files with abnormal permissions')
    if action == 'y':
        utils.change_permissions(file_paths, default_access)
    if action == 'ask':
        for file_path in file_paths:
            if utils.get_decision(f"{file_path} has wrong permissions. Change it?"):
                utils.change_permissions([file_path], default_access)


def handle_symbols_in_name(directories, tricky_letters, substitute, action):
    if action == 'n':
        return

    file_paths = utils.detect_problematic_names(directories, tricky_letters)
    print(f'\nFound {len(file_paths)} files with problematic names')
    for file_path in file_paths:
        if action == 'y' or (action == 'ask' and utils.get_decision(f"{file_path} contains problematic chars. Rename it?")):
            utils.change_file_name(file_path, tricky_letters, substitute)


def handle_duplicates(directories, action):
    if action == 'n':
        return

    duplicates = utils.detect_duplicates(directories)
    print(f'\nFound {len(duplicates)} sets of files with same content')
    for files in duplicates.values():
        try:
            oldest = utils.get_oldest_file(files)
            other = [file for file in files if file != oldest]
            if action == 'y':
                utils.remove_files(other)
            if action == 'ask':
                for file in other:
                    if utils.get_decision(f"{file} is copy of {oldest}. Remove it?"):
                        utils.remove_files([file])
        except ValueError:
            logging.warning(f'Could not handle duplicates among group: {files}')
            continue


def handle_same_name(directories, action):
    if action == 'n':
        return

    same_name = utils.detect_same_name(directories)
    print(f'\nFound {len(same_name)} sets of files with same name')
    for files in same_name.values():
        try:
            newest = utils.get_newest_file(files)
            other = [file for file in files if file != newest]
            if action == 'y':
                utils.remove_files(other)
            if action == 'ask':
                for file in other:
                    if utils.get_decision(f"{file} is older then {newest}. Remove it?"):
                        utils.remove_files([file])
        except ValueError:
            logging.warning(f'Could not handle same name files among group: {files}')
            continue


def handle_missing_in_main(main_dir, other_dirs, action):
    if action == 'n':
        return

    missing = utils.detect_not_in_main_dir(main_dir, other_dirs)
    print(f'\nFound {len(missing)} files missing in main directory')
    for file_path in missing:
        if action == 'y' or (action == 'ask' and utils.get_decision(f"{file_path} is not in {main_dir}. Move it?")):
            utils.move_file_to_main_dir(file_path, main_dir)
