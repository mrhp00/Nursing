from rest_framework.authtoken.models import Token
from nurse_backend.general.serialer import permissions_serializer
from nurse_backend.models import Nurse


def read_permissions(token, category, item):
    """
    this function will reveal if user has specified permission
    :param token: this is logged in user token
    :param category: permission category
    :param item: permission type
    :return: True for access granted and False for access forbidden
    """
    token_object = Token.objects.get(key=token)
    nurse_cursor = Nurse.objects.get(id=token_object.user.id)
    all_permissions = nurse_cursor.permissions.all()
    permissions = permissions_serializer(all_permissions)
    access = False
    for permission in permissions:
        if permission["category"] == "admin":
            access = True
            return access
        if permission["category"] == category:
            if permission["obbr"][0] == item:
                access = True
    return access


def create_main_menu(token):
    """
    internal function for creating menu based on access leve;
    :param token: auth token
    :return: list containing menu items
    """
    temp = []
    if token != "":
        token_object = Token.objects.get(key=token)
        nurse_cursor = Nurse.objects.get(id=token_object.user.id)
        permissions = nurse_cursor.permissions.all()
        for permission in permissions:
            if (permission.category == "admin") and (permission.crud == "S"):
                temp = [
                    {"name": "Hospital", "active": 1},
                    {"name": "HospitalWard", "active": 1},
                    {"name": "Shifts", "active": 1},
                    {"name": "Permissions", "active": 1},
                    {"name": "Nurses", "active": 1},
                    {"name": "Logout", "active": 1}
                ]
                return temp
            if (permission.category == "Hospital") and (permission.crud == "U"):
                temp.append({"name": "Hospital", "active": 1})
            if (permission.category == "HW") and (permission.crud == "R"):
                temp.append({"name": "HospitalWard", "active": 1})
            if (permission.category == "SET_SHIFT") and (permission.crud == "R"):
                temp.append({"name": "Shifts", "active": 1})
            if (permission.category == "Permission") and (permission.crud == "R"):
                temp.append({"name": "Permissions", "active": 1})
            if (permission.category == "Nurse") and (permission.crud == "R"):
                temp.append({"name": "Nurses", "active": 1})
    temp.append({"name": "Login", "active": 1})
    return temp


def check_admin(token):
    token_object = Token.objects.get(key=token)
    if token_object.user.is_superuser:
        return True
    else:
        return False
