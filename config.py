import configparser


def load_config(file):
    def parse_list(s):
        return [item.strip() for item in s.split(',')]

    config = configparser.ConfigParser()
    config.read(file)

    default_access = config['DEFAULT']['default_access']
    tmp = parse_list(config['DEFAULT']['tmp'])
    tricky_letters = parse_list(config['DEFAULT']['tricky_letters'])
    substitute = config['DEFAULT']['substitute']

    return {
        'default_access': int(default_access, base=8),
        'tmp': tmp,
        'tricky_letters': tricky_letters,
        'substitute': substitute
    }
