from unicodedata import category
from rest_framework.authtoken.models import Token
from rest_framework.decorators import api_view
from rest_framework.response import Response

from ..general.permission_manager import read_permissions, create_main_menu
from ..general.serialer import permissions_serializer as ps
from ..models import Permission, Nurse, NurseHistory
from django.db.models import Q


# noinspection PyUnusedLocal
@api_view(["POST"])
def show_all(request):
    """
    This function will generate list of permissions.
    :param request: No entry required.
    :return: content with list of permissions
    """
    permissions = read_permissions(request.data["token"], "PERMISSIONS", "R")
    if not permissions:
        content = {
            "error": True,
            "message": "Access Forbidden"
        }
        return Response(content)
    permissions = ps(Permission.objects.filter(~Q(category='admin')))

    content = {
        "error": False,
        "message": "permissions retrieval success",
        "data": {
            "permissions": permissions
        }
    }
    return Response(content)


@api_view(["POST"])
def create_menu(request):
    """
    this function will create UI main menu.
    :param request: token which is user auth token.
    :return: list of main menu items
    """
    if request.data["token"]:
        token_object = Token.objects.get(key=request.data["token"])
        nurse_cursor = Nurse.objects.get(id=token_object.user.id)
        ward_cursor = NurseHistory.objects.get(nurse=nurse_cursor, active=True)
        hospital_cursor = ward_cursor.ward.hospital
        main = create_main_menu(request.data["token"])
        content = {
            "error": False,
            "menu": main,
            "hospital": hospital_cursor.id
        }
    else:
        main = create_main_menu("")
        content = {
            "error": True,
            "message": "Please login first",
            "menu": main
        }

    return Response(content)
