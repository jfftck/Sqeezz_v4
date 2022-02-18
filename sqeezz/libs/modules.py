from importlib import import_module
from importlib.util import find_spec, module_from_spec, spec_from_file_location
from os import path
from sys import modules

from ..sqeezzutils import LazyLoad


_base_package = modules['__main__']


def lazy_module(mod: str):
  def __inner():
    return module(mod)

  return LazyLoad(__inner)


def module(mod: str):
  global _base_package

  if find_spec(mod) is not None:
    return import_module(mod)

  root = path.dirname(path.abspath(_base_package.__file__))
  spec = spec_from_file_location(mod, path.join(root, '{}.py'.format(path.join(*mod.split('.')))))
  
  module = module_from_spec(spec)
  modules[mod] = module
  spec.loader.exec_module(module)

  return module
