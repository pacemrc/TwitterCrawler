import csv
import json
import multiprocessing
import os
import shutil
import sys
import concurrent.futures
import time

from Media import ReqsHandler
from Media import FileHandler
from Tools.common import *
from Config.InitConfig import config

def Initialize():

    print("开始执行init函数")
    user_account = input("请输入用户账号：")

    print("{}开始获取用户数据{}".format("="*5,"="*5))
    # 获取用户公共数据
    ReqsHandler.getUserInfo(user_account)
    FileHandler.parseUserInfo()

    if not config.userId: exit()

    profile_url = 'https://twitter.com/' + user_account
    print("-" * 110)
    print("{:^15s}|{:^15s}|{:^15s}|{:^15s}|{:^15s}|{:^15s}|{:^15s}".format("UserName","UserAccount","FolloingCount","FollowerCount","TweetCount","MediaCount","LikesCount"))
    print("{:^15s}|{:^15s}|{:^15d}|{:^15d}|{:^15d}|{:^15d}|{:^15d}".format(config.userName,config.userAccount,config.followingCount,config.followersCount,config.statusesCount,config.mediaCount,config.favouritesCount))
    print("-" * 110)
    print("{:^15s}|   {:<100s}".format("Description",config.userDescription))
    print("{:^15s}|   {:<100s}".format("ProfileAddr", profile_url))
    print("-" * 110)


def parseRawFile():

    request_count = 1
    cursor_id = ''
    count =config.count

    if config.mediaCount < count:
        config.rawfile_numbers = 1
    else:
        config.rawfile_numbers = int(config.mediaCount / count) * 3
    print("{}开始下载数据文件{}".format("=" * 5, "=" * 5))
    for i in range(config.rawfile_numbers):
        # try:
        sys.stdout.write(f"\r[INFO] 正在下载第{i + 1}个数据文件...")
        sys.stdout.flush()
        rawfile = config.getRawfileName(i + 1)
        ReqsHandler.downloadRawFile(rawfile, request_count, str(count), cursor_id, config.userId)
        time.sleep(1)
        if os.path.getsize(rawfile) < 1000:
            config.rawfile_numbers=i
            break

        cursor_id,content,request_count= FileHandler.getCursorID(rawfile, request_count, count)
    print(f"\n[INFO] 解析完成！获取到{config.rawfile_numbers}个数据文件...")


def SaveMediaToExcel():

    count = config.count

    print("{}开始解析数据至CSV文件{}".format("="*5,"="*5))
    csv_file = config.userDataDir + f'\\{config.userAccount}-media.csv'

    try:
        with open(csv_file, mode='a+', encoding='utf-8-sig', newline='') as f:
            csv_writer = csv.writer(f)
            csv_writer.writerow(
                ['推特用户', '推特账号', '推文日期', '推文内容', '点赞数', '评论数', '转发数', '推文类型', '推文链接'])

        for i in range(config.rawfile_numbers):
            rawfile = config.getRawfileName(i + 1)
            sys.stdout.write(f"\r[INFO] 正在解析第{i+1}个数据文件...")
            sys.stdout.flush()
            time.sleep(1)
            with open(rawfile, "r", encoding='utf8') as f:
                content = json.load(f)
            FileHandler.doMediaDataToCsv(csv_file, content, count)
        print("\n[INFO] 解析完成！")
    except PermissionError:
        print("请把excel文件关闭后重试")
        exit(0)


def SavaMediaData():


    print("{}开始下载媒体数据{}".format("="*5,"="*5))
    max_thread = multiprocessing.cpu_count()
    with concurrent.futures.ThreadPoolExecutor(max_workers=max_thread) as executor:
        for i in range(config.rawfile_numbers):
            sys.stdout.write(f"\r[INFO] 正在下载第{i+1}个数据文件...")
            sys.stdout.flush()
            rawfile = config.getRawfileName(i + 1)
            executor.submit(ReqsHandler.downloadMedia,rawfile)

    executor.shutdown()

    print("\n[INFO] 下载完成！")


def getReport():

    print("{}开始生成下载报告{}".format("="*5,"="*5))
    print("-" * 35)
    print("{:<9s} {:<9s} {:<9s}".format("任务总数", "有效任务数", "无效任务数"))
    print("{:<10d} {:^12d} {:^10d}".format(config.total_task_number, config.total_task_number -config.invalid_task_number, config.invalid_task_number))
    print("-" * 35)
    print("[*] 有效任务详情：")
    print("-" * 60)
    print("{:<9s} {:^9s} {:^9s} {:^9s} {:^9s}".format("任务类型", "任务数量","媒体数量", "成功数", "失败数"))
    print("{:<11s} {:^11d} {:^11d} {:^11d} {:^11d}".format("视频任务",config.video_task_nummber,config.video_number, config.video_success_number, config.video_fail_number))
    print("{:<11s} {:^11d} {:^11d} {:^11d} {:^11d}".format("图片任务",config.photo_task_number, config.photo_number, config.photo_success_number, config.photo_fail_number))
    print("{:<13s} {:<10d}".format("未知推文数量",len(config.unkown_tweet_list)))
    print("{:<13s} {:<10d}".format("未知媒体数量", len(config.unknow_media_list)))
    print("-" * 60)

    print("[*] 无效任务详情：")
    print("-" * 60)
    print("无效推文链接：")
    for i in range(len(config.invalid_task_list)):
        print("https://twitter.com/{}/status/{}".format(config.userAccount, config.invalid_task_list[i]))
    print("未知推文链接：")
    for i in range(len(config.unkown_tweet_list)):
        print("https://twitter.com/{}/status/{}".format(config.userAccount, config.unkown_tweet_list[i]))
    print("未知媒体链接：")
    for i in range(len(config.unknow_media_list)):
        print("https://twitter.com/{}/status/{}".format(config.userAccount, config.unknow_media_list[i]))
    print("-" * 60)
    print("{:<10s} {:<40}".format("数据路径",config.userDataDir))

    end_time = time.time()
    runtime= datetime.timedelta(seconds=end_time - config.start_time).total_seconds()
    minutes, remaining_seconds = convert_seconds(int(runtime))
    print("{:<16s} {:<40s}".format("程序运行时间",timestamp_to_datetime(config.start_time)))
    print("{:<16s} {:<40s}".format("程序结束时间",timestamp_to_datetime(end_time)))
    print("{:<16s} {:>2d}分钟{:^2d}秒".format("程序运行时长",minutes,remaining_seconds))

    # shutil.rmtree(config.tmp_dir)
