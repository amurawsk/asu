import os
import collections
import hashlib
import logging
import base64

logging.basicConfig(level=logging.DEBUG, format="\n%(asctime)s - %(levelname)s - %(message)s")

# ------------------- HELP ---------------------------
def calculate_file_hash(file_path):
    hash_sha256 = hashlib.sha256()
    with open(file_path, "rb") as file:
        while chunk := file.read(4096):
            hash_sha256.update(chunk)
    return base64.b64encode(hash_sha256.digest()).decode("utf-8")


def get_decision(prompt):
    while True:
        choice = input(f"{prompt} ({'Y/n'}): ").lower()
        if choice in ("", "y"):
            return True
        if choice == "n":
            return False


# ------------------- ACTIONS -------------------------
def remove_files(file_paths):
    for file_path in file_paths:
        try:
            if os.path.exists(file_path):
                os.remove(file_path)
                logging.info(f'Removed file {file_path=}')
        except Exception:
            logging.warning(f'Could not remove file {file_path=}')


def change_permissions(file_paths, default_permissions):
    for file_path in file_paths:
        try:
            os.chmod(file_path, default_permissions)
            logging.info(f'Changed file permissions {file_path=}')
        except Exception:
            logging.warning(f'Could not change file permissions {file_path=}')


def change_file_name(file_path, tricky_letters, substitute):
    new_path = file_path
    for letter in tricky_letters:
        new_path = new_path.replace(letter, substitute)
    try:
        os.rename(file_path, new_path)
        logging.info(f'Changed file name {file_path=}, {new_path=}')
    except Exception:
        logging.warning(f'Could not change file name {file_path=}')


def get_oldest_file(file_paths):
    try:
        oldest_file = min(file_paths, key=os.path.getctime)
        return oldest_file
    except Exception:
        logging.error(f'Could not get file data for one or more files, {file_paths=}')
        raise ValueError('Could not get some file data')


def get_newest_file(file_paths):
    try:
        newest_file = max(file_paths, key=os.path.getctime)
        return newest_file
    except Exception:
        logging.error(f'Could not get file data for one or more files, {file_paths=}')
        raise ValueError('Could not get some file data')
    

def move_file_to_main_dir(file_path, main_dir):
    try:
        relative_path = os.path.relpath(file_path, start=os.path.commonpath([file_path, main_dir]))
        new_file_path = os.path.join(main_dir, relative_path)
        new_dir = os.path.dirname(new_file_path)
        if not os.path.exists(new_dir):
            os.makedirs(new_dir)
        os.rename(file_path, new_file_path)
        logging.info(f'Moved {file_path} to {new_file_path}')
    except Exception:
        logging.warning(f'Could not move {file_path=} to {main_dir=}')

# ------------------- DETECT ---------------------------
def detect_empty(directories):
    empty_files = []
    for directory in directories:
        for root, _, files in os.walk(directory):
            for file in files:
                file_path = os.path.join(root, file)
                if os.path.getsize(file_path) == 0:
                    empty_files.append(file_path)
    return empty_files


def detect_temporary(directories, temp_suffixes):
    temporary_files = []
    for directory in directories:
        for root, _, files in os.walk(directory):
            for file in files:
                file_path = os.path.join(root, file)
                if any(file.endswith(suffix) for suffix in temp_suffixes):
                    temporary_files.append(file_path)
    return temporary_files


def detect_invalid_permissions(directories, default_access):
    invalid_permissions_files = []
    for directory in directories:
        for root, _, files in os.walk(directory):
            for file in files:
                file_path = os.path.join(root, file)
                if os.path.isfile(file_path):
                    file_mode = os.stat(file_path).st_mode & 0o777
                    if file_mode != default_access:
                        invalid_permissions_files.append(file_path)
    return invalid_permissions_files


def detect_problematic_names(directories, tricky_letters):
    problematic_files = []
    for directory in directories:
        for root, _, files in os.walk(directory):
            for file in files:
                if any(letter in file for letter in tricky_letters):
                    problematic_files.append(os.path.join(root, file))
    return problematic_files


def detect_duplicates(directories):
    hash_to_paths = collections.defaultdict(list)
    for directory in directories:
        for root, _, files in os.walk(directory):
            for file in files:
                file_path = os.path.join(root, file)
                if os.path.isfile(file_path):
                    file_hash = calculate_file_hash(file_path)
                    hash_to_paths[file_hash].append(file_path)
    duplicate_files = {file_hash: paths for file_hash, paths in hash_to_paths.items() if len(paths) > 1}
    return duplicate_files


def detect_same_name(directories):
    name_to_paths = collections.defaultdict(list)
    for directory in directories:
        for root, _, files in os.walk(directory):
            for file in files:
                file_path = os.path.join(root, file)
                name_to_paths[file].append(file_path)
    same_name_files = {name: paths for name, paths in name_to_paths.items() if len(paths) > 1}
    return same_name_files


def detect_not_in_main_dir(main_dir, directories):
    main_dir_hashes = set()
    for root, _, files in os.walk(main_dir):
        for file in files:
            file_path = os.path.join(root, file)
            if os.path.isfile(file_path):
                main_dir_hashes.add(calculate_file_hash(file_path))

    not_in_main = []
    for directory in directories:
        for root, _, files in os.walk(directory):
            for file in files:
                file_path = os.path.join(root, file)
                if os.path.isfile(file_path):
                    file_hash = calculate_file_hash(file_path)
                    if file_hash not in main_dir_hashes:
                        not_in_main.append(file_path)
    return not_in_main
