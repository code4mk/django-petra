class Router:
    """A class for generating Django-style path definitions based on HTTP methods.

    Methods:
    - generate(http_method, path, controller):
        Generates a Django path definition string based on the provided HTTP method, path, and controller.

    - get(path, controller):
        Generates a path definition for the 'GET' method.

    - post(path, controller):
        Generates a path definition for the 'POST' method.

    - put(path, controller):
        Generates a path definition for the 'PUT' method.

    - delete(path, controller):
        Generates a path definition for the 'DELETE' method.

    - patch(path, controller):
        Generates a path definition for the 'PATCH' method.
    """

    @classmethod
    def generate(cls, http_method, path, controller, show_lists = False):
        """Generate a Django path definition string.

        Args:
        - http_method (str): The HTTP method for the route ('get', 'post', 'put', 'delete', 'patch').
        - path (str): The URL path for the route.
        - controller (callable): The controller function or method.

        Returns:
        str: A Django path definition string.
        """
        class_name = ((controller.__qualname__).split('.'))[0]
        method_name = controller.__name__
        module_name = ((controller.__module__).split('.'))[1]
        path_split = path.split('/')
        path_name = '--'.join(path_split[:-1]) + path_split[-1].rstrip('/')

        route_lists = {
            'method': http_method,
            'path': f'{module_name}/{path}',
            'view': f'{class_name}.{method_name}',
            'name': f'{module_name}_{path_name}',
            'module': module_name
            }
        the_path = f"path('{path}', {class_name}.as_view({{'{http_method}': '{method_name}'}}), name='{module_name}_{path_name}')"
        data =  {
            'route_lists': route_lists,
            'path': the_path
        }
        return  data

    @classmethod
    def get(cls, path, controller):
        """Generate a path definition for the 'GET' method.

        Args:
        - path (str): The URL path for the route.
        - controller (callable): The controller function or method.

        Returns:
        str: A Django path definition string for the 'GET' method.
        """
        return cls.generate('get', path, controller)

    @classmethod
    def post(cls, path, controller):
        """Generate a path definition for the 'POST' method.

        Args:
        - path (str): The URL path for the route.
        - controller (callable): The controller function or method.

        Returns:
        str: A Django path definition string for the 'POST' method.
        """
        return cls.generate('post', path, controller)

    @classmethod
    def put(cls, path, controller):
        """Generate a path definition for the 'PUT' method.

        Args:
        - path (str): The URL path for the route.
        - controller (callable): The controller function or method.

        Returns:
        str: A Django path definition string for the 'PUT' method.
        """
        return cls.generate('put', path, controller)

    @classmethod
    def delete(cls, path, controller):
        """Generate a path definition for the 'DELETE' method.

        Args:
        - path (str): The URL path for the route.
        - controller (callable): The controller function or method.

        Returns:
        str: A Django path definition string for the 'DELETE' method.
        """
        return cls.generate('delete', path, controller)

    @classmethod
    def patch(cls, path, controller):
        """Generate a path definition for the 'PATCH' method.

        Args:
        - path (str): The URL path for the route.
        - controller (callable): The controller function or method.

        Returns:
        str: A Django path definition string for the 'PATCH' method.
        """
        return cls.generate('patch', path, controller)


class Route:
    """A class representing a collection of routes.

    Args:
    - routes (list): A list of routes.

    Methods:
    - get_all_routes():
        Retrieves all routes in the collection, combining routes with the same path.

    Returns:
    list: A list of combined route paths.
    """

    def __init__(self, routes):
        self.routes = routes

    def get_all_routes(self):
        """Retrieve all routes in the collection, combining routes with the same path.

        Returns:
        list: A list of combined route paths.
        """
        import random

        # Group routes by path
        path_groups = {}
        for route in self.routes:
            path = route["path"].split("path('")[1].split("'")[0]
            view_info = route["path"].split("as_view({")[1].split("})")[0]
            method_info = view_info.strip("'{}")
            method, func = method_info.split("': '")
            
            if path in path_groups:
                # Add method to existing path
                path_groups[path]["methods"][method] = func
            else:
                # Create new path entry
                class_name = route["path"].split("path('")[1].split(".as_view")[0].split(", ")[-1]
                module_name = route["path"].split("name='")[1].split("_")[0]
                
                path_segments = path.split("/")
                path_segments = [seg.lower() for seg in path_segments if seg and '<' not in seg]
                segments_part = '_'.join(path_segments)
                random_number = str(random.randint(1000000000, 9999999999))
                
                path_groups[path] = {
                    "class_name": class_name,
                    "methods": {method: func},
                    "module_name": module_name,
                    "path_segments": path_segments,
                    "random_number": random_number
                }
        
        # Generate combined paths
        combined_routes = []
        for path, info in path_groups.items():
            methods_dict = str(info["methods"]).replace("'", '"')
            # Sort methods alphabetically and join with underscore
            methods_str = '_'.join(sorted(info["methods"].keys()))
            segments_part = '_'.join(info["path_segments"])
            name = f"{info['module_name']}__{segments_part}__{methods_str}_{info['random_number']}"
            
            combined_path = f"path('{path}', {info['class_name']}.as_view({methods_dict}), name='{name}')"
            combined_routes.append(combined_path)
            
        return combined_routes

    def show_lists(self):
        return [route["route_lists"] for route in self.routes]