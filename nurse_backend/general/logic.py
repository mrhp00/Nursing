import random

"""
example input:
nurse = {'id': 'nurse_id', 'exp': 220, 'D': [1, 7], 'E': [], 'N': [],
         '-': [], 'X': [], 'duty': 0, 'over_duty': 0}
"""


def set_shifts(d, e, n, x, nurse, month):
    org_days = []
    for i in range(1, month + 1):
        org_days.append(i)

    if "D" not in nurse.keys():
        nurse.update({"D": []})
    if "E" not in nurse.keys():
        nurse.update({"E": []})
    if "N" not in nurse.keys():
        nurse.update({"N": []})
    if "-" not in nurse.keys():
        nurse.update({"-": []})
    if "X" not in nurse.keys():
        nurse.update({"X": []})
    nurse.update({"duty": 0})
    nurse.update({"over_duty": 0})
    current_do = (len(nurse["D"]) * 7) + (len(nurse["E"]) * 7) + (len(nurse["N"]) * 19)
    if current_do > 230:
        return "over duty already exist!"
    else:
        if current_do >= 150:
            nurse["duty"] = current_do
            nurse["over_duty"] = current_do - 150
        else:
            nurse["duty"] += current_do

    def set_duty(number):
        if (nurse["duty"] + number) > 150:
            rem = (nurse["duty"] + number) - 150
            nurse["over_duty"] += rem
            nurse["duty"] = 150
        else:
            nurse["duty"] += number

    days = org_days.copy()

    if (d + e + (n * 2) + x) > month:
        rtn = "entry check: days out of range"
        return rtn
    if ((d * 7) + (e * 7) + (n * 19)) > 230:
        rtn = "entry check: overdose shifts"
        return rtn
    loop_prevent = days.copy()
    while len(nurse["N"]) < n:
        gen = random.randint(0, len(days))
        current_day = days[gen - 1]
        if (current_day not in nurse["D"]) and (current_day not in nurse["E"]) and (current_day not in nurse["N"]) and (
                current_day not in nurse["-"]) and (current_day not in nurse["X"]) and (
                (current_day + 1) not in nurse["D"]) and ((current_day + 1) not in nurse["E"]) and (
                (current_day + 1) not in nurse["N"]) and ((current_day + 1) not in nurse["-"]) and (
                (current_day + 1) not in nurse["X"]):
            current_day = days.pop(gen - 1)
            nurse["N"].append(current_day)
            nurse["-"].append(current_day + 1)
            set_duty(19)
            loop_prevent = days.copy()
        else:
            if (len(loop_prevent)) == 0:
                break
            elif current_day in loop_prevent:
                loop_prevent.remove(current_day)
                continue

    while len(nurse["D"]) < d:
        gen = random.randint(0, len(days))
        current_day = days[gen - 1]
        if (current_day not in nurse["D"]) and (current_day not in nurse["E"]) and (current_day not in nurse["N"]) and (
                current_day not in nurse["-"]) and (current_day not in nurse["X"]):
            current_day = days.pop(gen - 1)
            nurse["D"].append(current_day)
            set_duty(7)

    while len(nurse["E"]) < e:
        gen = random.randint(0, len(days))
        current_day = days[gen - 1]
        if (current_day not in nurse["D"]) and (current_day not in nurse["E"]) and (current_day not in nurse["N"]) and (
                current_day not in nurse["-"]) and (current_day not in nurse["X"]):
            current_day = days.pop(gen - 1)
            nurse["E"].append(current_day)
            set_duty(7)

    # loop_prevent = days.copy()
    # while len(nurse["X"]) < x:
    #     gen = random.randint(0, len(days))
    #     current_day = days[gen - 1]
    #     if (current_day not in nurse["D"]) and (current_day not in nurse["E"]) and
    #     (current_day not in nurse["N"]) and (current_day not in nurse["-"]) and (current_day not in nurse["X"]):
    #         current_day = days.pop(gen - 1)
    #         nurse["X"].append(current_day)
    #         loop_prevent = days.copy()
    #     else:
    #         if (len(loop_prevent)) == 0:
    #             break
    #         elif current_day in loop_prevent:
    #             loop_prevent.remove(current_day)
    #             continue

    for i in org_days:
        if (i not in nurse["D"]) and (i not in nurse["E"]) and (i not in nurse["N"]) and (
                i not in nurse["-"]) and (i not in nurse["X"]):
            nurse["X"].append(i)

    return nurse
