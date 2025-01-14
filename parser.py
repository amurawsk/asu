import argparse


def parse_args(default_config_path):
    parser = argparse.ArgumentParser(description="Cleanup script, can detect all sorts of unwanted files. All options have choices 'y' (yes), 'n' (no), 'ask' (prompt).")
    parser.add_argument("-x", "--main-dir", help="Directory to store all files.", required=True)
    parser.add_argument("-d", "--dir", nargs='*', help="Additional directories to be cleaned up. Can be specified multiple times.")
    parser.add_argument(
        "--config-file", "--config",
        type=str,
        default=default_config_path,
        help=f"Path to custom configuration file (default: {default_config_path})."
    )
    parser.add_argument(
        "-m", "--missing-in-main-dir",
        help="Find files that are not present in the main directory. ",
        nargs='?',
        default='n',
        const='ask',
        choices=('y', 'n', 'ask')
    )
    parser.add_argument(
        "-c", "--same-content",
        help="Find files with the same content. ",
        nargs='?',
        default='n',
        const='ask',
        choices=('y', 'n', 'ask')
    )
    parser.add_argument(
        "-s", "--same-name",
        help="Find files with the same name. ",
        nargs='?',
        default='n',
        const='ask',
        choices=('y', 'n', 'ask')
    )
    parser.add_argument(
        "-t", "--temporary",
        help="Find temporary files. ",
        nargs='?',
        default='n',
        const='ask',
        choices=('y', 'n', 'ask')
    )
    parser.add_argument(
        "-e", "--empty",
        help="Find files with no content. ",
        nargs='?',
        default='n',
        const='ask',
        choices=('y', 'n', 'ask')
    )
    parser.add_argument(
        "-a", "--abnormal-permissions",
        help="Find files with abnormal access permissions. ",
        nargs='?',
        default='n',
        const='ask',
        choices=('y', 'n', 'ask')
    )
    parser.add_argument(
        "-p", "--problematic-files",
        help="Find files with special characters in their filename. ",
        nargs='?',
        default='n',
        const='ask',
        choices=('y', 'n', 'ask')
    )
    args = parser.parse_args()
    return args
