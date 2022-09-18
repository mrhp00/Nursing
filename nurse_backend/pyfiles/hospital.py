from rest_framework.decorators import api_view
from rest_framework.response import Response
from nurse_backend.models import Hospital, HospitalWard
from ..general.permission_manager import read_permissions
from ..general.serialer import hospital_serializer as hs


# noinspection PyUnusedLocal
@api_view(["POST"])
def show_all(request):
    """
    This function will provide list of hospitals which fetched from database
    :param request: no entry required
    :return: serialized list of hospitals object
    """
    permissions = read_permissions(request.data["token"], "HOSPITAL", "R")
    if not permissions:
        content = {
            "error": True,
            "message": "Access Forbidden"
        }
        return Response(content)
    else:

        if request.data["id"] != 0:
            hospitals = hs(Hospital.objects.filter(id=request.data["id"]))
        else:
            hospitals = hs(Hospital.objects.all())
        content = {
            "error": False,
            "message": "success",
            "data": {"hospitals": hospitals}
        }
        return Response(content)


@api_view(["POST"])
def store(request):
    """
    This function will save/update hospital object coming within request into database.
    :param request:'title','phone','address','operation are compulsory but in 'operation' update you need to provide
    hospital 'id' too
    :return: serialized list of hospitals object after operation
    """
    try:
        if request.data["operation"] == "store":
            permissions = read_permissions(request.data["token"], "HOSPITAL", "C")
            if not permissions:
                content = {
                    "error": True,
                    "message": "Access Forbidden"
                }
                return Response(content)
            else:
                title = request.data["title"]
                phone = request.data["phone"]
                address = request.data["address"]
                Hospital.objects.create(title=title, phone=phone, address=address)
                hospitals = hs(Hospital.objects.all())
                content = {
                    "error": False,
                    "message": "saving success",
                    "data": {"hospitals": hospitals}
                }
        elif request.data["operation"] == "update":
            permissions = read_permissions(request.data["token"], "HOSPITAL", "U")
            if not permissions:
                content = {
                    "error": True,
                    "message": "Access Forbidden"
                }
                return Response(content)
            else:
                hospital = Hospital.objects.get(id=request.data["id"])
                hospital.title = request.data["title"]
                hospital.phone = request.data["phone"]
                hospital.address = request.data["address"]
                hospital.save()
                hospitals = hs(Hospital.objects.all())
                content = {
                    "error": False,
                    "message": "update success",
                    "data": {"hospitals": hospitals}
                }
        else:
            content = {
                "error": True,
                "message": "Please provide operation"
            }
    except Exception as error:
        content = {
            "error": True,
            "message": error
        }
    return Response(content)


@api_view(["POST"])
def delete(request):
    """
    This function will delete desired hospital from database
    :param request: 'id' which is id of hospital
    :return: serialized list of hospitals object after delete
    """
    try:
        permissions = read_permissions(request.data["token"], "HOSPITAL", "D")
        if not permissions:
            content = {
                "error": True,
                "message": "Access Forbidden"
            }
            return Response(content)
        else:
            hospital = Hospital.objects.get(id=request.data["id"])
            checker = HospitalWard.objects.filter(hospital=hospital)
            if len(checker) == 0:
                hospital.delete()
                hospitals = hs(Hospital.objects.all())
                content = {
                    "error": False,
                    "message": "delete success",
                    "data": {"hospitals": hospitals}
                }
            else:
                hospitals = hs(Hospital.objects.all())
                content = {
                    "error": True,
                    "message": "please remove assigned wards first",
                    "data": {"hospitals": hospitals}
                }
    except Exception as error:
        content = {
            "error": True,
            "message": error
        }
    return Response(content)
