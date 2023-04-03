import configparser

class Settings:
  __conf = None

  @staticmethod
  def get(name):
    if Settings.__conf is None:  # Read only once, lazy.
      Settings.__conf = configparser.ConfigParser()
      Settings.__conf.read('./Configuration/Config.ini')

    for section in Settings.__conf.sections():
      if name in Settings.__conf[section]:
        return Settings.__conf[section][name]
      
    return None

  @staticmethod
  def set(name, value):
    # if name in Settings.__setters:
    #   Settings.__conf[name] = value
    # else:
    #   raise NameError("Name not accepted in set() method")
    raise NotImplementedError