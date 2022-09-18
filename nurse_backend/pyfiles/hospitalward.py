from django.contrib.auth.decorators import login_required
from rest_framework.authtoken.models import Token
from rest_framework.decorators import api_view
from rest_framework.response import Response

from nurse_backend.general.permission_manager import read_permissions, check_admin
from nurse_backend.general.serialer import hospitalward_serializer as hws, hospital_serializer
from nurse_backend.models import Hospital, Ward, HospitalWard, NurseHistory, HospitalShift, Nurse


@api_view(["POST"])
def show_all(request):
    """
    will take token as input for verify access, then will take hospital id and return its wards.
    :param request: access token , hospital id
    :return: content of desire hospital's wards
    """
    permissions = read_permissions(request.data["token"], "HW", "R")
    if not permissions:
        content = {
            "error": True,
            "message": "Access Forbidden"
        }
        return Response(content)
    try:
        admin = check_admin(request.data["token"])
        if not admin:
            hospitalward = hws(request.data["hospital"])
            hospital = hospital_serializer(
                Hospital.objects.get(id=request.data["hospital"]))
            content = {
                "error": False,
                "message": "Retrieve success",
                "data": {
                    "hospitalward": hospitalward,
                    "hospitals": hospital
                }
            }
        else:
            hospitalward = hws(0)
            hospitals = hospital_serializer(Hospital.objects.all())
            content = {
                "error": False,
                "message": "Retrieve success",
                "data": {
                    "hospitalward": hospitalward,
                    "hospitals": hospitals
                }
            }

    except Exception as error:
        content = {
            "error": True,
            "message": error
        }
    return Response(content)


@api_view(["POST"])
def view_wards(request):
    """
    will take token as input for verify access, then will take hospital id and return its wards.
    :param request: access token , hospital id
    :return: content of desire hospital's wards
    """
    permissions = read_permissions(request.data["token"], "HW", "R")
    if not permissions:
        content = {
            "error": True,
            "message": "Access Forbidden"
        }
        return Response(content)
    try:
        hospitalward = hws(request.data["hospital"])
        content = {
            "error": False,
            "message": "Retrieve success",
            "data": {
                "hospitalward": hospitalward,
            }
        }
    except Exception as error:
        content = {
            "error": True,
            "message": error
        }
    return Response(content)


@api_view(["POST"])
def store(request):
    try:
        operation = request.data["operation"]
        if operation == "store":
            permissions = read_permissions(request.data["token"], "HW", "C")
            if not permissions:
                content = {
                    "error": True,
                    "message": "Access Forbidden"
                }
                return Response(content)
            hospital = Hospital.objects.get(id=request.data["hospital"])
            wards = request.data["wards"]
            for ward in wards:
                cursor = Ward.objects.get(id=ward)
                HospitalWard.objects.create(hospital=hospital, ward=cursor)
            hospitalward = hws(request.data["hospital"])
            content = {
                "error": False,
                "message": "Retrieve success",
                "data": {
                    "hospitalward": hospitalward
                }
            }
            return Response(content)
        elif operation == "update":
            permissions = read_permissions(request.data["token"], "HW", "U")
            if not permissions:
                content = {
                    "error": True,
                    "message": "Access Forbidden"
                }
                return Response(content)
            hospital = Hospital.objects.get(id=request.data["hospital"])
            new_wards = request.data["wards"]
            old_wards = []

            # Filling old wards :
            hospital_filter = HospitalWard.objects.filter(hospital=hospital)
            for ward in hospital_filter:
                old_wards.append(ward.ward.id)

            # comparing old and new wards:
            compare_list = set(old_wards).intersection(new_wards)

            # removing unused wards from list
            for ward in old_wards:
                if ward not in compare_list:
                    condition_one = NurseHistory.objects.filter(
                        ward=HospitalWard.objects.get(hospital=hospital, ward=Ward.objects.get(id=ward)))
                    condition_two = HospitalShift.objects.filter(
                        ward=HospitalWard.objects.get(hospital=hospital, ward=Ward.objects.get(id=ward)))
                    if condition_one.__len__() == 0 and condition_two.__len__() == 0:
                        delete_selector = HospitalWard.objects.get(
                            hospital=hospital, ward=Ward.objects.get(id=ward))
                        delete_selector.delete()

            # adding new wards from list
            for ward in new_wards:
                if ward not in compare_list:
                    cursor = Ward.objects.get(id=ward)
                    HospitalWard.objects.create(hospital=hospital, ward=cursor)
            hospitalward = hws(request.data["hospital"])
            content = {
                "error": False,
                "message": "Retrieve success",
                "data": {
                    "hospitalward": hospitalward
                }
            }
            return Response(content)
    except Exception as error:
        raise error


def delete_local(id):
    selected_h_ward = HospitalWard.objects.get(id=id)
    n_history_check = NurseHistory.objects.filter(ward=selected_h_ward)
    h_shift_check = HospitalShift.objects.filter(ward=selected_h_ward)
    if (len(n_history_check) == 0) and (len(h_shift_check) == 0):
        selected_h_ward.delete()
        return True
    else:
        return False


@api_view(["POST"])
def delete(request):
    permissions = read_permissions(request.data["token"], "HW", "D")
    if not permissions:
        content = {
            "error": True,
            "message": "Access Forbidden"
        }
        return Response(content)
    try:
        status = delete_local(request.data["id"])
        if status:
            error = False
            message = "delete success"
        else:
            error = True
            message = "delete failed due to relation in history of nurse or hospital's shifts"
        admin = check_admin(request.data["token"])
        if not admin:
            hospitalward = hws(request.data["hospital"])
            hospital = hospital_serializer(
                Hospital.objects.get(id=request.data["hospital"]))
            content = {
                "error": error,
                "message": message,
                "data": {
                    "hospitalward": hospitalward,
                    "hospitals": hospital
                }
            }
        else:
            hospitalward = hws(0)
            hospitals = hospital_serializer(Hospital.objects.all())
            content = {
                "error": error,
                "message": message,
                "data": {
                    "hospitalward": hospitalward,
                    "hospitals": hospitals
                }
            }
        return Response(content)
    except Exception as error:
        raise error
