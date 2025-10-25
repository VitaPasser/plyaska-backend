import importlib
import inspect
import pkgutil

from locust import TaskSet



def load_loading_tests(package_name: str):
    package = importlib.import_module(package_name)
    loading_tests = []

    for _, module_name, _ in pkgutil.iter_modules(package.__path__, package.__name__ + "."):
        module = importlib.import_module(module_name)
        for _, obj in inspect.getmembers(module, inspect.isclass):
            if issubclass(obj, TaskSet) and obj is not TaskSet:
                if obj in loading_tests:
                    continue
                if not getattr(obj, "_excluded", False):
                    loading_tests.append(obj)
    return loading_tests
