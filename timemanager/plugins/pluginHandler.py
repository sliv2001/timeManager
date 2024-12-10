import os
import importlib, importlib.util
from timemanager.utils.settings import Settings

_mod_funcs = {}

# These decorators are designed to change the very core functionality of the presenter.
# Therefore, they normally should be avoided in favor of adding new members to classes by means of Python
# and/or adding functionalities by Qt Signal/Slot mechanism.

def modifiable_by_plugin(func):
  def inner(*args, **kwargs):
    if func.__name__ in _mod_funcs.keys():
      _mod_funcs[func.__name__](*args, **kwargs)
    return func(*args, **kwargs)
  return inner

def modify_func(func):
  def decorator(func):
    _mod_funcs[func.__name__] = func
    return func
  return decorator

class pluginHandler:

  collectedPlugins = {}

  def __init__(self, settings: Settings, view, presenter) -> None:
    self.settings = settings
    self.view = view
    self.presenter = presenter
    self.updateAccessiblePlugins()

  def updateAccessiblePlugins(self):
    path = os.path.dirname(__file__)
    for dirpath, dirnames, filenames in os.walk(path):
      if dirpath == path: continue
      try:
        module_name = dirpath.split('/')[-1]
        if any([filename.endswith('.py') and filename.startswith(module_name) for filename in filenames]):
          spec = importlib.util.spec_from_file_location('module_name', dirpath+'/'+module_name+'.py')
          mod = importlib.util.module_from_spec(spec)
          spec.loader.exec_module(mod)
          # sys.modules[module_name] = mod
          self.collectedPlugins[module_name] = mod
          mod.presenterUpdate(self.presenter)
          mod.viewUpdate(self.view)
      except Exception as e:
        print(e)
