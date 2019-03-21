import yaml
from os.path import isfile

def load():
    paths = ['~/.config/twiliogui.yml', '~/.twiliogui.yml', './config.yml']
    for filename in paths:
        if isfile(filename):
            return yaml.load(open(filename, 'r'), Loader=yaml.SafeLoader)
