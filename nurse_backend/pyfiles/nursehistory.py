from rest_framework.decorators import api_view
from rest_framework.response import Response
from nurse_backend.models import Nurse, NurseHistory, HospitalWard
from nurse_backend.general.serialer import nurse_history_serializer as nhs
import jdatetime


@api_view(["POST"])
def show_all(request):
    """
    This function will create selected nurse's history
    :param request: id (nurse_id)
    :return:
    """
    try:
        history = nhs(request.data["id"])
        content = {
            "error": False,
            "message": "Retrieval success",
            "data": {
                "history": history
            }
        }
    except Exception as error:
        content = {
            "error": True,
            "message": error,
        }
    return Response(content)


@api_view(["POST"])
def store(request):
    """
    This function will store or edit selected nurse's history.
    :param request: operation (store/update)

    operation "store" will need following parameters:
        ward (ward_id), nurse(nurse_id), sy (start year), sm (start month), sd (start day),
        active (0 for not active and 1 for active)
        *NOTE:
        for NOT active status you need following parameters too: ey (end year), em (end month), ed (end day)

    operation "update" will need following parameter in addition to "store" operation's parameter:
        history_id



    :return: list of selected nurse's history in content object
    """
    operation = request.data["operation"]
    ward = HospitalWard.objects.get(id=request.data["ward"])
    nurse = Nurse.objects.get(id=request.data["nurse"])
    start_date_year = request.data["sy"]
    start_date_month = request.data["sm"]
    start_date_day = request.data["sd"]
    start_date = jdatetime.date(year=start_date_year, month=start_date_month, day=start_date_day).togregorian()
    if operation == "store":
        if request.data["active"] == 0:
            end_date_year = request.data["ey"]
            end_date_month = request.data["em"]
            end_date_day = request.data["ed"]
            end_date = jdatetime.date(year=end_date_year, month=end_date_month, day=end_date_day).togregorian()
            NurseHistory.objects.create(ward=ward, nurse=nurse, start=start_date, end=end_date, active=False)
        else:
            NurseHistory.objects.create(ward=ward, nurse=nurse, start=start_date, end=None, active=True)

        nurse_history = nhs(request.data["nurse"])
        content = {
            "error": False,
            "message": "Creating record was successful",
            "data": {
                "history_history": nurse_history
            }
        }
        return Response(content)
    if operation == "update":
        history_record = NurseHistory.objects.get(request.data["id"])
        if request.data["active"] == 0:
            end_date_year = request.data["ey"]
            end_date_month = request.data["em"]
            end_date_day = request.data["ed"]
            end_date = jdatetime.date(year=end_date_year, month=end_date_month, day=end_date_day).togregorian()
            history_record.ward = ward
            history_record.start = start_date
            history_record.end = end_date
            history_record.active = False
            history_record.save()

        else:
            history_record.ward = ward
            history_record.start = start_date
            history_record.end = None
            history_record.active = False
            history_record.save()

        nurse_history = nhs(request.data["nurse"])
        content = {
            "error": False,
            "message": "Creating record was successful",
            "data": {
                "history_history": nurse_history
            }
        }
        return Response(content)
