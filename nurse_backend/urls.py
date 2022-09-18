"""
The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.urls import path
from nurse_backend.general import authentication
from nurse_backend.pyfiles import hospital, ward, shift, nurse, hospitalward, permissions, nursehistory

urlpatterns = [
    path('load/', permissions.create_menu),
    path('hospitals/', hospital.show_all),
    path('hospital/store/', hospital.store),
    path('hospital/delete/', hospital.delete),

    path('wards/', ward.show_all),
    path('ward/store/', ward.store),
    path('ward/delete/', ward.delete),

    path('shifts/', shift.show_all),
    path('shift/store/', shift.store),
    path('shift/delete/', shift.delete),
    path('shifts/autoassign/', shift.set_shifts),
    path('shifts/store/', shift.store_shifts),
    path('shifts/view/', shift.view_shifts),

    path('nurses/', nurse.show_all),
    path('nurse/view/', nurse.view_nurse),
    path('nurse/store/', nurse.create),
    path('nurse/delete/', nurse.delete_unused),
    path('nurse/deactive/', nurse.deactive_nurse),

    path('hospital/wards/', hospitalward.show_all),
    path('hospital/ward/', hospitalward.view_wards),
    path('hospital/ward/store/', hospitalward.store),
    path('hospital/ward/delete/', hospitalward.delete),

    path('permissions/', permissions.show_all),
    # path('permission/store', permissions.create),

    path('nurse/history/', nursehistory.show_all),
    path('nurse/history/store/', nursehistory.store),

    path('signup/nurses/', authentication.create_nurse_user),
    path('change_password/', authentication.change_password_user),
    path('login/', authentication.login_user),
    path('logout/', authentication.logout_user),
]
