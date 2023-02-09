
def translate_month(short_month):
    month = dict({"Jan": "Янв", "Feb": "Фев", "Mar": "Мар", "Apr": "Апр", "May": "Май", "June": "Июн", "July": "Июл", "Aug": "Авг", "Sept": "Сен", "Oct": "Окт", "Nov": "Ноя", "Dec": "Дек"})
    return month[short_month]

def translate_day_of_the_week(short_day_of_the_week):
    week = dict({"Mon": "Пн", "Tue": "Вт", "Wed": "Ср", "Thu": "Чт", "Fri": "Пт", "Sat": "Сб", "Sun": "Вс"})
    return week[short_day_of_the_week]

