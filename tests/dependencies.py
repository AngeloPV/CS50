import importlib

def import_components(module_and_components):
    components = {}
    for module_name, component_names in module_and_components.items():
        try:
            module = importlib.import_module(module_name)
            components[module_name] = {}
            for component_name in component_names:
                try:
                    components[module_name][component_name] = getattr(module, component_name)
                except AttributeError:
                    print(f"Warning: Component '{component_name}' not found in module '{module_name}'.")
        except ModuleNotFoundError:
            print(f"Warning: Module '{module_name}' could not be found.")
    return components