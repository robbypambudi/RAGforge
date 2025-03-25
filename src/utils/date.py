import datetime

class DateHelper:
    @staticmethod
    def get_current_date():
        return datetime.now().strftime("%Y-%m-%d")