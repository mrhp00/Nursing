from datetime import datetime
from rest_framework.decorators import api_view
from rest_framework.response import Response
from nurse_backend.models import Shift, NurseHistory, ShiftRequest, HospitalWard, NurseShift, Nurse
from ..general.permission_manager import read_permissions
from ..general.serialer import shift_serializer as ss, nurse_shifts
from ..general.logic import set_shifts as setter
from ..general.calculator import next_month_days as nmd
from ..general.calculator import past_month_last_day as pmld


# noinspection PyUnusedLocal
@api_view(["POST"])
def show_all(request):
    """
    This function will provide list of shifts which fetched from database
    :param request: no entry required
    :return: serialized list of shifts object
    """
    permissions = read_permissions(request.data["token"], "SHIFT", "R")
    if not permissions:
        content = {
            "error": True,
            "message": "Access Forbidden"
        }
        return Response(content)
    shifts = ss(Shift.objects.all())
    content = {
        "error": False,
        "message": "success",
        "data": {"shifts": shifts}
    }
    return Response(content)


@api_view(["POST"])
def store(request):
    """
    This function will save/update shift object coming within request into database.
    :param request:'title', 'hours', 'operation are compulsory but in 'operation' update you need to provide
    ward 'id' too
    :return: serialized list of shifts object after operation
    """
    try:
        if request.data["operation"] == "store":
            permissions = read_permissions(request.data["token"], "SHIFT", "C")
            if not permissions:
                content = {
                    "error": True,
                    "message": "Access Forbidden"
                }
                return Response(content)
            title = request.data["title"]
            hours = request.data["hours"]
            Shift.objects.create(title=title, hours=hours)
            shifts = ss(Shift.objects.all())
            content = {
                "error": False,
                "message": "saving success",
                "data": {"shifts": shifts}
            }
        elif request.data["operation"] == "update":
            permissions = read_permissions(request.data["token"], "SHIFT", "U")
            if not permissions:
                content = {
                    "error": True,
                    "message": "Access Forbidden"
                }
                return Response(content)
            shift = Shift.objects.get(id=request.data["id"])
            shift.title = request.data["title"]
            shift.hours = request.data["hours"]
            shift.save()
            shifts = ss(Shift.objects.all())
            content = {
                "error": False,
                "message": "update success",
                "data": {"shifts": shifts}
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
    This function will delete desired shifts from database
    :param request: 'id' which is id of shifts
    :return: serialized list of shifts object after delete
    """
    try:
        permissions = read_permissions(request.data["token"], "SHIFT", "D")
        if not permissions:
            content = {
                "error": True,
                "message": "Access Forbidden"
            }
            return Response(content)
        shift = Shift.objects.get(id=request.data["id"])
        shift.delete()
        wards = ss(Shift.objects.all())
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


@api_view(["POST"])
def set_shifts(request):
    """
    :param request:
    ward : ward id from nurse history,
    manual : if user want to set specified shift design for a nurse,
    D : number of morning shifts,
    E : number of evening shifts,
    N : number of night shifts,
    X : number of offs
    :return:
    """
    try:
        permissions = read_permissions(request.data["token"], "SET_SHIFT", "C")
        if not permissions:
            content = {
                "error": True,
                "message": "Access Forbidden"
            }
            return Response(content)
        ward_id = request.data["ward"]
        ward = HospitalWard.objects.get(id=ward_id)
        nurses = NurseHistory.objects.filter(ward=ward, active=True)
        assigned = []
        days = nmd()
        if request.data["manual"] == 0:
            for nurse in nurses:  # checking for active nurses in current ward
                current_nurse = {"id": nurse.nurse.id}

                requests = ShiftRequest.objects.filter(nurse=nurse.nurse)
                for requesting in requests:  # selecting all requested shifts for currently selected nurse
                    desire_day = requesting.desire_date.day
                    last_month_check = NurseShift.objects.filter(nurse=nurse.nurse, date=pmld())

                    if len(last_month_check) != 0:  # checking if last day of passed month for night shift
                        if last_month_check[0].shift.title == "N":
                            current_nurse.update({"-": [1]})
                            # days -= 1
                    if requesting.shift.title in current_nurse.keys():
                        current_nurse[requesting.shift.title].append(desire_day)
                    else:
                        current_nurse.update({requesting.shift.title: [desire_day]})

                if nurse.nurse.experience >= 180:  # sending nurse for auto shift assign by experience
                    dawn = (days // 7) * 3
                    evening = (days // 7) * 2
                    night = (days // 7) * 1
                    off = days - (dawn + evening + (night * 2))
                    output = setter(dawn, evening, night, off, current_nurse, days)
                    assigned.append(output)
                elif (nurse.nurse.experience >= 60) and (nurse.nurse.experience < 180):
                    dawn = (days // 7) * 2
                    evening = (days // 7) * 2
                    night = (days // 7)
                    off = days - (dawn + evening + (night * 2))
                    output = setter(dawn, evening, night, off, current_nurse, days)
                    assigned.append(output)
                elif nurse.nurse.experience < 60:
                    dawn = (days // 7) * 1
                    evening = (days // 7) * 2
                    night = (days // 7) * 1
                    off = days - (dawn + evening + (night * 2))
                    output = setter(dawn, evening, night, off, current_nurse, days)
                    assigned.append(output)
            content = {
                "error": False,
                "message": "Auto assigning complete",
                "data": {
                    "assigned": assigned
                }
            }
        else:
            content = "manual mode on"
    except Exception as error:
        content = {
            "error": True,
            "message": error
        }

    return Response(content)


@api_view(["POST"])
def store_shifts(request):  # gonna rework on this
    """
    Store shifts in data base
    :param request:
    :return:
    """
    permissions = read_permissions(request.data["token"], "SET_SHIFT", "U")
    if not permissions:
        content = {
            "error": True,
            "message": "Access Forbidden"
        }
        return Response(content)
    grid = request.data["assigned"]
    for nurse in grid:
        selected_nurse = Nurse.objects.get(id=nurse["id"])
        d = Shift.objects.get(title="D")
        e = Shift.objects.get(title="E")
        n = Shift.objects.get(title="N")
        x = Shift.objects.get(title="X")
        s = Shift.objects.get(title="-")
        date = datetime.now().date()

        for day in nurse["D"]:
            selected_date = date.replace(date.year, date.month + 1, day)
            validate = NurseShift.objects.filter(nurse=selected_nurse, date=selected_date)
            if (len(validate)) == 0:
                NurseShift.objects.create(shift=d, nurse=selected_nurse, date=selected_date)
            else:
                selected = validate[0]
                selected.shift = d
                selected.nurse = selected_nurse
                selected.date = selected_date
                selected.save()

        for day in nurse["E"]:
            selected_date = date.replace(date.year, date.month + 1, day)
            validate = NurseShift.objects.filter(nurse=selected_nurse, date=selected_date)
            if (len(validate)) == 0:
                NurseShift.objects.create(shift=e, nurse=selected_nurse, date=selected_date)
            else:
                selected = validate[0]
                selected.shift = e
                selected.nurse = selected_nurse
                selected.date = selected_date
                selected.save()

        for day in nurse["N"]:
            selected_date = date.replace(date.year, date.month + 1, day)
            validate = NurseShift.objects.filter(nurse=selected_nurse, date=selected_date)
            if (len(validate)) == 0:
                NurseShift.objects.create(shift=n, nurse=selected_nurse, date=selected_date)
            else:
                selected = validate[0]
                selected.shift = n
                selected.nurse = selected_nurse
                selected.date = selected_date
                selected.save()

        for day in nurse["-"]:
            selected_date = date.replace(date.year, date.month + 1, day)
            validate = NurseShift.objects.filter(nurse=selected_nurse, date=selected_date)
            if (len(validate)) == 0:
                NurseShift.objects.create(shift=s, nurse=selected_nurse, date=selected_date)
            else:
                selected = validate[0]
                selected.shift = s
                selected.nurse = selected_nurse
                selected.date = selected_date
                selected.save()

        for day in nurse["X"]:
            selected_date = date.replace(date.year, date.month + 1, day)
            validate = NurseShift.objects.filter(nurse=selected_nurse, date=selected_date)
            if (len(validate)) == 0:
                NurseShift.objects.create(shift=x, nurse=selected_nurse, date=selected_date)
            else:
                selected = validate[0]
                selected.shift = x
                selected.nurse = selected_nurse
                selected.date = selected_date
                selected.save()
    return Response("SUCCESS")


@api_view(["POST"])
def view_shifts(request):
    """
    returning all shifts base on selected ward
    :param request: ward , year , month
    :return: content with shifts in data
    """
    permissions = read_permissions(request.data["token"], "SET_SHIFT", "R")
    if not permissions:
        content = {
            "error": True,
            "message": "Access Forbidden"
        }
        return Response(content)
    ward = request.data["ward"]
    year = request.data["year"]
    month = request.data["month"]
    shifts = nurse_shifts(ward, year, month)
    content = {
        "error": False,
        "message": "Success",
        "data": {"shifts": shifts}
    }
    return Response(content)
