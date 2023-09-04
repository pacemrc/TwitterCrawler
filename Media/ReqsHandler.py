import json
import os
import re
import sys
import time
import requests
from requests.exceptions import ProxyError
import logging

logging.basicConfig(level=logging.INFO,format='%(asctime)s %(filename)s[line:%(lineno)d] %(message)s',datefmt='%Y-%m-%d')

from Tools.common import *
requests.packages.urllib3.disable_warnings()
from jsonpath import jsonpath
from Config.InitConfig import config

def getUserInfo(user_account):

    try:
        userInfoUrl = config.getUserInfoUrl(user_account)
        req = requests.get(url=userInfoUrl, headers=config.twitter_headers, verify=False, proxies=config.proxy)
        if req.status_code != 200:
            raise Exception
        with open(config.userinfo_file, 'w', encoding='utf8') as f:
            f.write(req.text)
    except requests.exceptions.ProxyError:
        logging.error("连接代理失败。")
        sys.exit(1)
    except Exception:
        logging.error("userInfoUrl链接可能过期，请检查。")
        sys.exit(1)


def downloadRawFile(rawfile, cursor_index, count, cursor_id, user_id):

    try:
        mediaInfoUrl = config.getMediaInfoUrl(cursor_index, user_id, count, cursor_id)
        req = requests.get(url=mediaInfoUrl, headers=config.twitter_headers, verify=False, proxies=config.proxy)
        if req.status_code != 200:
            raise Exception
        with open(rawfile, 'w', encoding='utf8') as f:
            f.write(req.text)

    except requests.exceptions.ProxyError:
        logging.error("连接代理失败。")
        sys.exit(1)
    except Exception:
        logging.error("网络连接不稳定。")
        sys.exit(1)

def downloadMedia(api_file):

    with open(api_file, "r", encoding='utf8') as f:
        rawfile_content = json.load(f)
    # 创建目录
    video_file_dir = config.userDataDir + "\\video"
    photo_file_dir = config.userDataDir + "\\photo"
    os.makedirs(video_file_dir, exist_ok=True)
    os.makedirs(photo_file_dir, exist_ok=True)


    for i in range(int(config.count)):
        # try:
        tweet_id_path1,tweet_id_path2,media_path1,\
        media_path2,end_flag_path,\
        media_type1,media_type2 = config.getJsonPaths3(i)

        if type(jsonpath(rawfile_content, end_flag_path)) != bool: break

        #当tweet_id匹配路径在不同位置及tweet为隐私推文时的处理
        if type(jsonpath(rawfile_content, tweet_id_path1)) != bool:
            tweet_id_path = tweet_id_path1
        elif type(jsonpath(rawfile_content, tweet_id_path2)) != bool:
            tweet_id_path = tweet_id_path2
        else:
            config.invalid_task_number += 1

            invalid_task_id_path = config.getInvalidTweetID(i)
            invalid_task_id = str(jsonpath(rawfile_content,invalid_task_id_path)[0]).replace("tweet-","")
            config.invalid_task_list.append(invalid_task_id)
            continue
        config.total_task_number+=1
        tweet_id = jsonpath(rawfile_content, tweet_id_path)[0]

        if type(jsonpath(rawfile_content,media_path1)) is bool and type(jsonpath(rawfile_content,media_path2)) is bool:

            config.unkown_tweet_list.append(tweet_id)
            continue
        
        if type(jsonpath(rawfile_content,media_path1)) is bool:
            media_content = jsonpath(rawfile_content,media_path2)[0]
        else:
            media_content = jsonpath(rawfile_content,media_path1)[0]

        media_type = jsonpath(rawfile_content, media_type1)
        if type(media_type) is bool:
            media_type = jsonpath(rawfile_content, media_type2)
        media_type = media_type[0]

        if media_type == "video" or media_type == "animated_gif":

            url_list = list()
            for n in range(4):

                url_path = f'$[0].video_info.variants[{n}].url'
                url = jsonpath(media_content, url_path)
                if type(url) is bool:
                    break
                else:
                    url = url[0]

                if "m3u8" not in url:
                    url_list.append(url)
                if media_type == "animated_gif":
                    max_resolution_url = url
                else:
                    max_resolution_url = get_max_resolution_url(url_list)
            sys.stdout.write(f"\r视频任务：正在下载第{i + 1}个推文...")
            sys.stdout.flush()
            try:
                req = requests.get(url=max_resolution_url, headers=config.twimg_http_headers, proxies=config.proxy, verify=False, timeout=10)
                time.sleep(1.55)
                with open(f'{video_file_dir}\\{tweet_id}.mp4', 'wb') as f:
                    f.write(req.content)
            except ProxyError:
                logging.info("因网络不稳定，新增一个视频下载失败。")
                config.video_fail_number += 1
            else:
                if req.status_code == 200:
                    config.video_success_number += 1

            finally:
                config.video_number += 1

            config.video_task_nummber += 1


        elif media_type == "photo":

            photo_link_list = re.findall("media_url_https': '(.*?)', 'type': 'photo", str(media_content))
            sys.stdout.write(f"\r图片任务：正在下载第{i + 1}个推文...")
            sys.stdout.flush()
            for i in range(len(photo_link_list)):
                try:
                    req = requests.get(url=photo_link_list[i], headers=config.twimg_http_headers, proxies=config.proxy, verify=False, timeout=10)
                    time.sleep(0.5)
                    with open(f'{photo_file_dir}\\{tweet_id}-{i+1}.jpg', 'wb') as f:
                        f.write(req.content)
                except ProxyError:
                    logging.info("因网络不稳定，新增一个图片下载失败。")
                    config.photo_fail_number += 1
                else:
                    if req.status_code == 200:
                        config.photo_success_number += 1
                finally:
                    config.photo_number+=1

            config.photo_task_number += 1

        else:
            config.unknow_media_list.append(tweet_id)
            continue



