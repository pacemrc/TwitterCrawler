import csv
import json
import os
import re
from datetime import datetime
from jsonpath import jsonpath

from Config.InitConfig import config


def parseUserInfo():


    with open(config.userinfo_file, "r", encoding='utf8') as f:
        content = json.load(f)
    user_id_path,\
    user_name_path,\
    user_account_path,\
    user_description_path,\
    following_count_path,\
    followers_count_path,\
    statuses_count_path,\
    media_count_path,\
    favourites_count_path = config.getJsonPaths1()
    # 字段
    config.userId = jsonpath(content, user_id_path)[0]
    config.userName = jsonpath(content, user_name_path)[0]
    config.userAccount = jsonpath(content, user_account_path)[0]
    config.userDescription = jsonpath(content, user_description_path)[0]
    config.userDescription = str(config.userDescription).replace("\n","")
    config.followingCount = jsonpath(content, following_count_path)[0]
    config.followersCount = jsonpath(content, followers_count_path)[0]
    config.statusesCount = jsonpath(content, statuses_count_path)[0]
    config.mediaCount = jsonpath(content, media_count_path)[0]
    config.favouritesCount = jsonpath(content, favourites_count_path)[0]

    config.userDataDir = config.data_dir + "\\" + config.userName
    os.makedirs(config.userDataDir, exist_ok=True)

def getCursorID(rawfile, request_count, count):


    with open(rawfile, "r", encoding='utf8') as f:
        content = json.load(f)
    request_count += 1

    for n in range(count+5):
        cursor_id_path, cursorType_path = config.getJsonPath4(n)
        cursor_id = jsonpath(content, cursor_id_path)
        cursorType = jsonpath(content, cursorType_path)
        if (cursor_id == False) and (cursorType == False):
            continue
        elif (cursorType[0] != "Bottom"):
            continue
        else:
            cursor_id_path, cursorType_path = config.getJsonPath4(n)
            cursor_id = jsonpath(content, cursor_id_path)[0]
            break
    return cursor_id,content,request_count

def doMediaDataToCsv(csv_file, content, count):


    for i in range(count):
        # try:

            # PATH
            tweet_id_path1, tweet_id_path2, \
            tweet_time_path1, tweet_time_path2,\
            tweet_content_path1, tweet_content_path2,\
            media_type_path,favorite_count_path1,\
            favorite_count_path2,reply_count_path1,\
            reply_count_path2,retweet_count_path1, \
            retweet_count_path2, end_flag_path = config.getJsonPaths2(i)

            if type(jsonpath(content, end_flag_path)) != bool: break
            #tweet_id出现的位置会有偏差，此处对tweet_id不同出现的位置进行处理
            if type(jsonpath(content, tweet_id_path1)) != bool:
                tweet_id_path = tweet_id_path1
            elif type(jsonpath(content, tweet_id_path2)) != bool:
                tweet_id_path = tweet_id_path2
            else:
                continue

            # 字段
            tweet_link = f'https://twitter.com/{config.userAccount}/status/' + jsonpath(content, tweet_id_path)[0]

            try:
                jsonpath(content, tweet_time_path1)[0]
                jsonpath(content, tweet_content_path1)[0].replace('\n', '')
                jsonpath(content, favorite_count_path1)[0]
                jsonpath(content, reply_count_path1)[0]
                jsonpath(content, retweet_count_path1)[0]
                tweet_time_path = tweet_time_path1
                tweet_content_path = tweet_content_path1
                favorite_count_path = favorite_count_path1
                reply_count_path = reply_count_path1
                retweet_count_path =retweet_count_path1

            except:
                tweet_time_path = tweet_time_path2
                tweet_content_path = tweet_content_path2
                favorite_count_path = favorite_count_path2
                reply_count_path = reply_count_path2
                retweet_count_path =retweet_count_path2
            tweet_time = jsonpath(content, tweet_time_path)[0]
            GMT_FORMAT = '%a %b %d %H:%M:%S +0000 %Y'
            tweet_time = str(datetime.strptime(tweet_time, GMT_FORMAT))[0:10]

            # content
            tweet_content = jsonpath(content, tweet_content_path)[0].replace('\n', '')
            tweet_content = re.sub('@[a-zA-Z0-9_]+', '', tweet_content)
            tweet_content = re.sub('https(.*) ?', '', tweet_content)
            tweet_type = jsonpath(content, media_type_path)
            if tweet_type == False:
                tweet_type = 'share'
            else:
                tweet_type = jsonpath(content, media_type_path)[0]
            favorite_count = jsonpath(content, favorite_count_path)[0]
            reply_count = jsonpath(content, reply_count_path)[0]
            retweet_count = jsonpath(content, retweet_count_path)[0]
            with open(csv_file, mode='a+', encoding='utf-8-sig', newline='') as f:
                csv_writer = csv.writer(f)
                csv_writer.writerow(
                    [config.userName, config.userAccount, tweet_time, tweet_content, favorite_count, reply_count, retweet_count,
                     tweet_type, tweet_link])
        # except:
        #     # print("[ERROR File_MediaDataToCsv异常]")
        #     pass
