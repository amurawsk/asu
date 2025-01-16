import ConfigParser


def load_config(file):
    def parse_list(s):
        return [item.strip() for item in s.split(',') if item.strip()]

    config = ConfigParser.ConfigParser()
    config.read(file)

    default_access = config.get('DEFAULT', 'default_access')
    tmp = parse_list(config.get('DEFAULT', 'tmp'))
    tricky_letters = parse_list(config.get('DEFAULT', 'tricky_letters'))
    substitute = config.get('DEFAULT', 'substitute')

    return {
        'default_access': int(default_access, 8),
        'tmp': tmp,
        'tricky_letters': tricky_letters,
        'substitute': substitute
    }
