import os
import importlib

# This file serves as the initializer for the `routes` package.
# Dynamically imports and manages all route modules ending with `_routes.py`.

__all__ = []  # Keeps track of imported modules for external usage

# Dynamically import all route modules in the `routes` directory
route_folder = os.path.dirname(__file__)  # Get the folder containing this file
for module in os.listdir(route_folder):
    if module.endswith("_routes.py") and module != "__init__.py":  # Identify all *_routes.py files
        module_name = f"app.routes.{module[:-3]}"  # Remove `.py` for module name
        try:
            # Dynamically import the module
            imported_module = importlib.import_module(module_name)
            globals()[module[:-3]] = imported_module  # Add the module to globals()
            __all__.append(module[:-3])  # Add the module name to `__all__`
        except ModuleNotFoundError as e:
            print(f"Error: Module '{module_name}' not found - {e}")
        except Exception as e:
            print(f"Error: Failed to import module '{module_name}' - {e}")
