import subprocess
from enum import Enum, Flag, auto


class BasePermission(Enum):
    def _generate_next_value_(name, start, count, last_values):
        return 2 * count


class Permission(BasePermission, Flag):
    READ = auto()
    WRITE = auto()
    EXECUTE = auto()


class UserGroup(Enum):
    ADMIN = Permission.READ | Permission.WRITE | Permission.EXECUTE
    USER = Permission.READ
    MANAGER = Permission.READ | Permission.WRITE
    SUPPORT = Permission.EXECUTE


class User:
    def __init__(self, name, user_role=None):
        self.name = name
        self.user_role = user_role
        self.permission = Permission.READ

    @property
    def user_role(self):
        return self._user_role

    @user_role.setter
    def user_role(self, input):
        if not isinstance(input, str) and not isinstance(input, int):
            raise TypeError

        if isinstance(input, str):
            input = input.upper().strip()
            if not any(group.name == input for group in UserGroup):
                raise ValueError("Incompatible user group provided.")
            self._user_role = input
        else:
            total_score = 0
            for _, item in Permission.__members__.items():
                total_score += item.value

            if input > total_score:
                self._user_role = UserGroup(Permission.READ).name
            else:
                max_value = 0
                for index, (score, ug) in enumerate(
                    UserGroup._value2member_map_.items()
                ):
                    if score.value <= input:
                        if index == 0:
                            self._user_role = ug.name
                            max_value = score.value
                            continue
                        elif max_value <= score.value:
                            self._user_role = ug.name
                            max_value = score.value

    @property
    def permission(self):
        return self._permission

    @permission.setter
    def permission(self, value):
        if not isinstance(value, Permission):
            raise TypeError
        self._permission = UserGroup[self._user_role].value

    def read(self, file_path=""):
        if Permission.READ not in self.permission:
            raise PermissionError("User does not have read access.")

        try:
            with open(file_path, "r") as file:
                print(file.read())
        except IOError as e:
            print(f"Error reading from file: {e}")

    def write(self, file_path="", content=""):
        if Permission.WRITE not in self.permission:
            raise PermissionError("User does not have write access.")
        try:
            with open(file_path, "w") as file:
                file.write(content)
        except IOError as e:
            print(f"Error creating/writing to file: {e}")

    def execute(self, file_path=""):
        if Permission.EXECUTE not in self.permission:
            raise PermissionError("User does not have execute access.")
        subprocess.run(["python", file_path])
