import jdatetime

from nurse_backend.models import NurseHistory, Hospital, HospitalWard, Nurse, NurseShift


def hospital_serializer(hospitals):
    """
    taking list of hospital objects and return list of serialized nurse objects
    :param hospitals: nurses as object
    :return: list of nurses as serialized objects
    """
    output = []
    for hospital in hospitals:
        object_creator = {
            "id": hospital.id,
            "title": hospital.title,
            "phone": hospital.phone,
            "address": hospital.address,
        }
        output.append(object_creator)
    return output


def ward_serializer(wards):
    """
    taking list of ward objects and return list of serialized ward objects
    :param wards: wards as object
    :return: list of wards as serialized objects
    """
    output = []
    for ward in wards:
        object_creator = {
            "id": ward.id,
            "title": ward.title,
        }
        output.append(object_creator)
    return output


def shift_serializer(shifts):
    """
    taking list of shift objects and return list of serialized shift objects
    :param shifts: shifts as object
    :return: list of shifts as serialized objects
    """
    output = []
    for shift in shifts:
        object_creator = {
            "id": shift.id,
            "title": shift.title,
            "hours": shift.hours
        }
        output.append(object_creator)
    return output


def nurse_serializer(nurses):
    """
    taking list of nurse objects and return list of serialized nurse objects
    :param nurses: nurses as object
    :return: list of nurses as serialized objects
    """
    output = []
    for nurse in nurses:
        ward_collector = NurseHistory.objects.filter(
            nurse_id=nurse.id, active=True)
        ward_list = []
        for ward in ward_collector:
            ward_list.append({"id": ward.id,
                             "hospital": ward.ward.hospital.title, "ward": ward.ward.ward.title})
        object_creator = {
            "id": nurse.id,
            "first_name": nurse.first_name,
            "last_name": nurse.last_name,
            "social_number": nurse.social_number,
            "ward": ward_list,
            "experience": nurse.experience,
            "phone": nurse.phone,
            "address": nurse.address,
            "email": nurse.email,
        }
        output.append(object_creator)
    return output


def permissions_serializer(permissions):
    """
    This function will serialize list of permissions.
    :param permissions: Array of permission objects.
    :return: List of permissions
    """
    output = []
    for permission in permissions:
        # print(permission.category)
        # if permission.category == 'admin':
        #     continue
        object_creator = {
            "id": permission.id,
            "category": permission.category,
            "title": permission.title,
            "obbr": permission.crud
        }
        output.append(object_creator)
    return output


def hospitalward_serializer(hospital):
    """
    This function will serialize list of wards.
    :param hospital: hospital ID
    :return: List of wards belonging to selected hospital
    """
    output = []
    if hospital != 0:
        cursor_hospital = Hospital.objects.get(id=hospital)
        wards = HospitalWard.objects.filter(hospital=cursor_hospital)

        for ward in wards:
            object_creator = {
                "id": ward.id,
                "hospital": ward.hospital.title,
                "title": ward.ward.title,
            }
            output.append(object_creator)
        return output
    else:
        hospitals = Hospital.objects.all()
        for hospital in hospitals:
            wards = HospitalWard.objects.filter(hospital=hospital)
            for ward in wards:
                object_creator = {
                    "id": ward.id,
                    "hospital": ward.hospital.title,
                    "title": ward.ward.title,
                }
                output.append(object_creator)
            return output


def nurse_history_serializer(nurse_id):
    """
    This function will return history of desire nurse
    :param nurse_id: id of desire nurse for fetching data
    :return: all history of desire nurse
    """
    nurse = Nurse.objects.get(id=nurse_id)
    history = []
    all_history = NurseHistory.objects.filter(nurse=nurse)
    for h in all_history:
        hospital = h.ward.hospital.title
        ward = h.ward.ward.title
        object_creator = {
            "hospital": hospital,
            "ward": ward,
            "first_name": nurse.first_name,
            "last_name": nurse.last_name,
            "social_number": nurse.social_number,
            "phone": nurse.phone,
            "start": h.start,
            "end": h.end,
            "active": h.active
        }
        history.append(object_creator)
    return history


def nurse_shifts(ward, selected_year, selected_month):
    """
    will show nurses shift of specified ward.
    :param ward: currently logged in ward
    :param selected_year: specified year (Jalali)
    :param selected_month: specified month (Jalali)
    :return: Grid of shifts.
    """
    date = []
    for i in range(1, 32, 1):
        date.append(str(selected_year) + "/" +
                    str(selected_month) + "/" + str(i))
    if int(selected_month) > 6:
        date.pop()
    if int(selected_month) == 12:
        date.pop()

    header = {' Nurses / Date ': date}
    temp = {}
    temp.update(header)

    selected_ward = HospitalWard.objects.get(id=ward)
    all_nurses = NurseHistory.objects.filter(ward=selected_ward, active=True)
    for nurse in all_nurses:
        nurse_object = {}
        name = nurse.nurse.first_name + " " + nurse.nurse.last_name

        if int(selected_month) < 7:
            date1 = jdatetime.date(year=int(selected_year), month=int(
                selected_month), day=1).togregorian()
            date2 = jdatetime.date(year=int(selected_year), month=int(
                selected_month), day=31).togregorian()
        elif int(selected_month) < 12:
            date1 = jdatetime.date(year=int(selected_year), month=int(
                selected_month), day=1).togregorian()
            date2 = jdatetime.date(year=int(selected_year), month=int(
                selected_month), day=30).togregorian()
        else:
            date1 = jdatetime.date(year=int(selected_year), month=int(
                selected_month), day=1).togregorian()
            date2 = jdatetime.date(year=int(selected_year), month=int(
                selected_month), day=29).togregorian()

        shifts = NurseShift.objects.filter(
            nurse=nurse.nurse, date__range=[str(date1), str(date2)])
        tmp = {}
        for shift in shifts:
            temp.update({shift.date: shift.shift.title})
        sorted_tmp = sorted(tmp.items())
        nurse_object.update({name: sorted_tmp})
        temp.update(nurse_object)
    return temp
