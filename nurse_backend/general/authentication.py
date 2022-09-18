from django.contrib.auth.models import User
from rest_framework.authtoken.models import Token
from django.contrib.auth import authenticate, login, logout
from rest_framework.decorators import api_view
from rest_framework.response import Response
import random
import string

# noinspection PyUnusedLocal
from nurse_backend.models import Nurse, NurseHistory


def create_password():
    """
    This function will create 8 character password containing 5 letters (lower and upper case),
    2 symbols and 3 numbers.
    :return: generated password.
    """
    letters = string.ascii_letters
    numbers = string.digits
    chars = string.punctuation
    result_str = ''.join(random.choice(letters) for i in range(5))
    result_str += ''.join(random.choice(chars) for i in range(2))
    result_str += ''.join(random.choice(numbers) for i in range(3))
    return result_str


def create_user(nurse):
    """
    This function will create a user based on Nurse model.
    :param nurse: which is nurse object.
    :return: auto generated password
    """
    username = nurse.social_number
    email = nurse.email
    password = create_password()
    user = User.objects.create_user(username, email, password)
    user.first_name = nurse.first_name
    user.last_name = nurse.last_name
    user.save()
    return password


def update_user(nurse):
    """
    This function will update user as requested. you can not update username due to policies.
    :param nurse: which is nurse object.
    :return: True for successful operation.
    """
    user = User.objects.get(username=nurse.social_number)
    user.first_name = nurse.first_name
    user.last_name = nurse.last_name
    user.save()
    return True


def delete_user(user_id):
    """
    will delete desire user.
    :param user_id: nurse social number.
    :return: True on success.
    """
    user = User.objects.get(username=user_id)
    user.delete()
    return True


@api_view(["POST"])
def create_nurse_user(request):
    """
    this function will create a user coming from front end side.
    :param request: "social_number","email","first_name","last_name" coming within request data.
    :return: a message of success with a auto generated password.
    """
    username = request.data["social_number"]
    email = request.data["email"]
    password = create_password()
    user = User.objects.create_user(username, email, password)
    user.first_name = request.data["first_name"]
    user.last_name = request.data["last_name"]
    user.save()
    content = {
        "error": False,
        "message": "User has been created successfully",
        "data": {"password": password}
    }
    return Response(content)


@api_view(["POST"])
def change_password_user(request):
    """
    This function will change user password.
    :param request: request["social_number"] which is nurse's social number,
    request["password"] which is new password for setting in user model,
    request["old_password"] which is old password of user (not necessarily if operation is forgotten).
    :return: either successfully changed password or user not found message.
    """
    user = User.objects.filter(username=request.data["social_number"])
    if request.data["operation"] == "forgotten":
        if len(user) != 0:
            user = User.objects.get(username=request.data["social_number"])
            user.set_password(request.data["password"])
            user.save()
            content = {
                "error": False,
                "message": "password changed successfully"
            }
        else:
            content = {
                "error": True,
                "message": "user not found"
            }
    elif request.data["operation"] == "change":
        if len(user) != 0:
            user = User.objects.get(username=request.data["social_number"])
            if user.check_password(request.data["old_password"]):
                user.set_password(request.data["password"])
                user.save()
                content = {
                    "error": False,
                    "message": "password changed successfully"
                }
            else:
                content = {
                    "error": True,
                    "message": "invalid password"
                }
        else:
            content = {
                "error": True,
                "message": "user not found"
            }
    else:
        content = {
            "error": True,
            "message": "Please define operation"
        }

    return Response(content)


@api_view(["POST"])
def login_user(request):
    username = request.data['username']
    password = request.data['password']
    user = authenticate(username=username, password=password)
    if user is not None:
        user_cursor = Nurse.objects.get(social_number=username)
        nurse_cursor = NurseHistory.objects.filter(nurse=user_cursor, active=True)
        if len(nurse_cursor) == 0:
            nurse_cursor = NurseHistory.objects.filter(nurse=user_cursor)

        hospital_title = nurse_cursor[0].ward.hospital.title
        hospital_id = nurse_cursor[0].ward.hospital.id
        ward_title = nurse_cursor[0].ward.ward.title
        ward_id = nurse_cursor[0].ward.id
        try:
            token = Token.objects.get(user_id=user.id)
        except:
            token = Token.objects.create(user_id=user.id)
        content = {
            "error": False,
            "token": token.key,
            "hospital_title": hospital_title,
            "hospital_id": hospital_id,
            "ward_title": ward_title,
            "ward_id": ward_id
        }
        return Response(content)
    else:
        content = {
            "error": True,
            "message": "NOT logged in"
        }
        print("failed", content)
        return Response(content)


@api_view(["POST"])
def logout_user(request):
    # print("step1")
    # token = Token.objects.get(key=request.data["token"])
    # print("step2")
    # token.delete()
    logout(request)
    content = {"message": "Logout Success"}
    return Response(content)
