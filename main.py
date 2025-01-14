import parser
import config
import handlers
import os

DEFAULT_CONFIG_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), '.clean_files')


def main():
    args = parser.parse_args(DEFAULT_CONFIG_PATH)
    main_dir = args.main_dir
    other_dirs = args.dir if args.dir else []
    all_dirs = [main_dir] + other_dirs
    config_dict = config.load_config(args.config_file) if args.config_file else config.load_config(DEFAULT_CONFIG_PATH)

    handlers.handle_empty(all_dirs, args.empty)
    handlers.handle_temporary(all_dirs, config_dict['tmp'], args.temporary)
    handlers.handle_abnormal_permissions(all_dirs, config_dict['default_access'], args.abnormal_permissions)
    handlers.handle_symbols_in_name(all_dirs, config_dict['tricky_letters'], config_dict['substitute'], args.problematic_files)
    handlers.handle_duplicates(all_dirs, args.same_content)
    handlers.handle_same_name(all_dirs, args.same_name)
    handlers.handle_missing_in_main(main_dir, other_dirs, args.missing_in_main_dir)


if __name__ == "__main__":
    main()
