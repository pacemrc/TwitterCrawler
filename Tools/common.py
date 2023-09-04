import datetime


def timestamp_to_minutes(timestamp):
    dt = datetime.datetime.fromtimestamp(timestamp)
    total_minutes = dt.total_seconds() / 60
    return total_minutes

def timestamp_to_datetime(timestamp):
    dt = datetime.datetime.fromtimestamp(timestamp)
    formatted_datetime = dt.strftime('%Y-%m-%d %H:%M:%S')  # 格式化为 YYYY-MM-DD HH:MM:SS
    return formatted_datetime


def get_max_resolution_url(url_list):
    max_resolution = 0
    max_resolution_url = ""

    for url in url_list:
        resolution = int(url.split("/")[-2].split("x")[1])
        if resolution > max_resolution:
            max_resolution = resolution
            max_resolution_url = url

    return max_resolution_url

def convert_seconds(seconds):
    minutes = seconds // 60
    remaining_seconds = seconds % 60
    return minutes, remaining_seconds