from datetime import datetime, timedelta


def current_time():
    return (datetime.now() - timedelta(hours=3)).strftime("%H:%M")
