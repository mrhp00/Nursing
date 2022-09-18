from datetime import date
from rest_framework.decorators import api_view
from rest_framework.response import Response

from ..general.permission_manager import read_permissions, check_admin
from ..general.serialer import nurse_serializer as ns
from ..general.authentication import create_user as cu, delete_user
from ..general.authentication import update_user as uu
from ..models import Nurse, HospitalWard, NurseHistory


def delete_nurse(nurse_id):
    """
    this function will delete nurse base on nurse id. main reason creating this is because
    we want to delete with transaction method.
    :param nurse_id: it is id of nurse.
    :return: True on success and false if nurse not found.
    """
    validate = Nurse.objects.filter(id=nurse_id)
    if len(validate) != 0:
        nurse = Nurse.objects.get(id=nurse_id)
        nurse.delete()
        return True
    else:
        return False


# noinspection PyUnusedLocal
@api_view(["POST"])
def show_all(request):
    """
    This function will create list nurses
    :param request: no entry required
    :return: serialized list of hospitals object
    """
    permissions = read_permissions(request.data["token"], "N", "R")
    if not permissions:
        content = {
            "error": True,
            "message": "Access Forbidden"
        }
        return Response(content)
    admin = check_admin(request.data["token"])
    if not admin:
        ward = request.data["ward_id"]
        nurses = ns(Nurse.objects.filter(nursehistory__ward=ward, nursehistory__active=True))
    else:
        nurses = ns(Nurse.objects.all())
    content = {
        "error": False,
        "message": "success",
        "data": {"nurses": nurses}
    }
    return Response(content)

@api_view(["POST"])
def view_nurse(request):
    permissions = read_permissions(request.data["token"], "N", "U")
    if not permissions:
        content = {
            "error": True,
            "message": "Access Forbidden"
        }
        return Response(content)
    nurses = ns(Nurse.objects.filter(id=request.data["id"]))
    content = {
        "error": False,
        "message": "success",
        "data": {"nurses": nurses}
    }
    return Response(content)


@api_view(["POST"])
def create(request):
    """
    This function will save/update hospital object coming within request into database.
    :param request: first_name, last_name, social_number, experience, phone, address, email, operation, hospitalward.
    :return: new list of nurses after create new one or update
    """
    try:
        validate = Nurse.objects.filter(social_number=request.data["social_number"])
        if request.data["operation"] == "store":
            if len(validate) == 0:
                nurse = Nurse.objects.create(first_name=request.data["first_name"], last_name=request.data["last_name"],
                                             social_number=request.data["social_number"],
                                             experience=request.data["experience"], phone=request.data["phone"],
                                             address=request.data["address"], email=request.data["email"])
                password = cu(nurse)
                NurseHistory.objects.create(ward=HospitalWard.objects.get(id=request.data["ward"]),
                                            nurse=nurse,
                                            active=True, start=date.today())
                nurses = ns(Nurse.objects.all())
                content = {
                    "error": False,
                    "message": "nurse has been created successfully",
                    "data": {
                        "password": password,
                        "nurses": nurses
                    }
                }
            else:
                content = {
                    "error": True,
                    "message": "Social number exist, operation has been canceled",
                }
        elif request.data["operation"] == "update":
            if len(validate) == 0:
                content = {
                    "error": True,
                    "message": "Nurse does not exist"
                }
            else:
                nurse = Nurse.objects.get(social_number=request.data["social_number"])
                nurse.first_name = request.data["first_name"]
                nurse.last_name = request.data["last_name"]
                nurse.experience = request.data["experience"]
                nurse.phone = request.data["phone"]
                nurse.address = request.data["address"]
                nurse.email = request.data["email"]
                nurse.save()
                user_update = uu(nurse)
                if user_update:
                    content = {
                        "error": False,
                        "message": "Update on nurse and user was successful",
                        "data": {"nurse": ns(Nurse.objects.all())}
                    }
                else:
                    content = {
                        "error": True,
                        "message": "User didn't update",
                        "data": {"nurse": ns(Nurse.objects.all())}
                    }
        else:
            content = {
                "error": True,
                "message": "Please provide operation name"
            }

    except Exception as error:
        content = {
            "error": True,
            "message": error
        }
    return Response(content)


@api_view(["POST"])
def deactive_nurse(request):
    """
    This function will deactive nurse from history base on given ward
    :param request: id => nurse id, ward => Hospitalward id
    :return: content with related message
    """
    validate = Nurse.objects.filter(id=request.data["id"])
    if len(validate) != 0:
        try:
            cursor = NurseHistory.objects.get(nurse=request.data["id"], ward=request.data["ward"], active=True)
        except Exception as error:
            content = {
                "error": True,
                "message": error
            }
        else:
            cursor.active = False
            cursor.save()
            content = {
                "error": False,
                "message": "Nurse has been de-activated"
            }
    else:
        content = {
            "error": True,
            "message": "Nurse not found"
        }
    return Response(content)


@api_view(["POST"])
def delete_unused(request):
    """
    This function will delete nurse and his/her user data off the database with transaction method.
    so after deleting nurse if anything happen during deleting user, same nurse will be re-created.
    :param request: nurse id is compulsory
    :return: relative content of message and data of nurses.
    """
    validate = Nurse.objects.filter(id=request.data["id"])
    if len(validate) != 0:
        nurse = Nurse.objects.get(id=request.data["id"])
        nurse_id = request.data["id"]
        first_name = nurse.first_name
        last_name = nurse.last_name
        social_number = nurse.social_number
        experience = nurse.experience
        phone = nurse.phone
        address = nurse.address
        email = nurse.email
        condition_one = delete_nurse(nurse_id)
        if condition_one:
            condition_two = delete_user(social_number)
            if condition_two:
                nurses = Nurse.objects.all()
                content = {
                    "error": False,
                    "message": "nurse has been deleted successfully",
                    "data": {
                        "nurses": nurses
                    }
                }
            else:
                Nurse.objects.create(first_name=first_name, last_name=last_name,
                                     social_number=social_number,
                                     experience=experience, phone=phone,
                                     address=address, email=email)
                nurses = Nurse.objects.all()
                content = {
                    "error": True,
                    "message": "Transaction has been canceled",
                    "data": {
                        "nurses": nurses,
                    }
                }
        else:
            nurses = Nurse.objects.all()
            content = {
                "error": True,
                "message": "Transaction has been canceled",
                "data": {
                    "nurses": nurses,
                }
            }
    else:
        content = {
            "error": True,
            "message": "nurse not found",
        }
    return Response(content)
