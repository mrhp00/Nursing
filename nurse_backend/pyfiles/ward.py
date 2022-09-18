from rest_framework.decorators import api_view
from rest_framework.response import Response
from nurse_backend.models import Ward
from ..general.serialer import ward_serializer as ws


# noinspection PyUnusedLocal
@api_view(["POST"])
def show_all(request):
    """
    This function will provide list of wards which fetched from database
    :param request: no entry required
    :return: serialized list of wards object
    """
    wards = ws(Ward.objects.all())
    content = {
        "error": False,
        "message": "success",
        "data": {"wards": wards}
    }
    return Response(content)


@api_view(["POST"])
def store(request):
    """
    This function will save/update ward object coming within request into database.
    :param request:'title', 'operation are compulsory but in 'operation' update you need to provide ward 'id' too
    :return: serialized list of wards object after operation
    """
    try:
        if request.data["operation"] == "store":
            title = request.data["title"]
            Ward.objects.create(title=title)
            wards = ws(Ward.objects.all())
            content = {
                "error": False,
                "message": "saving success",
                "data": {"wards": wards}
            }
        elif request.data["operation"] == "update":
            ward = Ward.objects.get(id=request.data["id"])
            ward.title = request.data["title"]
            ward.save()
            wards = ws(Ward.objects.all())
            content = {
                "error": False,
                "message": "update success",
                "data": {"wards": wards}
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
    This function will delete desired ward from database
    :param request: 'id' which is id of ward
    :return: serialized list of wards object after delete
    """
    try:
        ward = Ward.objects.get(id=request.data["id"])
        ward.delete()
        wards = ws(Ward.objects.all())
        content = {
            "error": False,
            "message": "delete success",
            "data": {"wards": wards}
        }
    except Exception as error:
        content = {
            "error": True,
            "message": error
        }
    return Response(content)
