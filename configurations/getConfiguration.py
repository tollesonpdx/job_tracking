import os
import configparser

def config(filename='database.ini', section='postgresql'):
    __location__ = os.path.realpath(os.path.join(os.getcwd(), os.path.dirname(__file__)))
    filename = os.path.join(__location__, filename)
    config = configparser.ConfigParser()
    config.read(filename)
    if config.has_section(section):
        config.set(section,'silly','Reubs')
        return {key:config.get(section, key) for key in config[section]}
    else:
        raise Exception(f'Section {section} not found in the "{filename}" file')

if __name__ == "__main__":
    params = config()
    print(params)