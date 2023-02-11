import json


def get_schedule_from_json():
    f = open("jsons_config/schedule.json", "r", encoding="utf-8")
    schedule = json.loads(f.read())
    f.close()
    return schedule


def set_schedule_to_json(schedule):
    try:
        with open('jsons_config/schedule.json', 'w', encoding='utf-8') as f:
            json.dump(schedule, f, ensure_ascii=False, indent=4)
        return True
    except:
        return False


def get_and_set_order_id_from_json():
    f = open("jsons_config/settings.json", "r", encoding="utf-8")
    buf = json.loads(f.read())
    f.close()
    order_id = buf["order_id"] + 1
    buf["order_id"] = order_id
    with open('jsons_config/settings.json', 'w', encoding='utf-8') as f:
        json.dump(buf, f, ensure_ascii=False, indent=4)
    return order_id


def get_price_and_time():
    f = open("jsons_config/price_and_time.json", "r", encoding="utf-8")
    buf = json.loads(f.read())
    f.close()
    room_price = buf["room_price"]
    bathroom_price = buf["bathroom_price"]
    check_in_price = buf["check_in_price"]

    room_time = buf["room_time"]
    bathroom_time = buf["bathroom_time"]
    check_in_time = buf["check_in_time"]

    return room_price, room_time, bathroom_price, bathroom_time, check_in_time, check_in_price


def get_feedbacks_from_json():
    f = open("jsons_config/feedback.json", "r", encoding="utf-8")
    feedbacks = json.loads(f.read())
    f.close()
    return feedbacks["feedbacks"]


def set_feedbacks_to_json(feedbacks_list):
    try:
        with open('jsons_config/feedback.json', 'w', encoding='utf-8') as f:
            json.dump(dict({"feedbacks": feedbacks_list}), f, ensure_ascii=False, indent=4)
        return True
    except:
        return False


def get_admins_and_cleaners_from_json():
    f = open("jsons_config/settings.json", "r", encoding="utf-8")
    buf = json.loads(f.read())
    f.close()
    return buf["admins"], buf["cleaners"]


def get_empy_order_from_order_0():
    f = open("orders/0.json", "r", encoding="utf-8")
    empty_order = json.loads(f.read())
    f.close()
    return empty_order
