import pandas


def get_date_and_time(timestamp: pandas.Timestamp):
    return timestamp.date(), timestamp.time()
