from rest_framework.permissions import BasePermission

class Permissions(BasePermission):
    def __init__(self):
        super().__init__()  # Call parent's init
        self.all_permissions = []  # Initialize the list

    def set_permission(self, permission_class):
        # Create a permission entry with a default "all actions" setting
        perm_entry = PermissionEntry(permission_class, all_actions=True)
        self.all_permissions.append(perm_entry)
        return perm_entry

    def retrieve_permissions(self, view):
        # Apply permissions based on the view's action, considering exclusions
        return [
            perm_entry.permission_class()
            for perm_entry in self.all_permissions
            if (perm_entry.all_actions or view.action in perm_entry.actions) 
            and view.action not in perm_entry.excluded_actions
        ]

class PermissionEntry:
    def __init__(self, permission_class, all_actions=False):
        self.permission_class = permission_class
        self.all_actions = all_actions
        self.actions = []
        self.excluded_actions = []  # New: track excluded actions

    def only(self, *actions):
        # Handle both array input and multiple arguments
        if len(actions) == 1 and isinstance(actions[0], (list, tuple)):
            self.actions.extend(actions[0])
        else:
            self.actions.extend(actions)
        self.all_actions = False  # Turn off all_actions if specific actions are set
        return self  # Allow chaining

    def ignore(self, *actions):  # New method
        # Handle both array input and multiple arguments
        if len(actions) == 1 and isinstance(actions[0], (list, tuple)):
            self.excluded_actions.extend(actions[0])
        else:
            self.excluded_actions.extend(actions)
        return self  # Allow chaining