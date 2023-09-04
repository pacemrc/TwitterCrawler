import os
import time

class Config:

    def __init__(self):

        # 媒体json数据源的个数
        rawfile_numbers = 0
        start_time = time.time()
        #每次请求获取的媒体的个数
        count = 50
        # 目录创建
        project_dir = os.path.abspath(os.path.curdir)
        data_dir = project_dir + "\\data"
        tmp_dir = data_dir + "\\tmp"
        rawfiles_dir = tmp_dir + "\\rawfiles"
        userinfo_file = tmp_dir + "\\userinfo.txt"

        os.makedirs(data_dir, exist_ok=True)
        os.makedirs(tmp_dir, exist_ok=True)
        os.makedirs(rawfiles_dir, exist_ok=True)


        invalid_task_list = list()
        unkown_tweet_list = list()
        unknow_media_list = list()

        video_success_number, photo_success_number, \
        video_fail_number, photo_fail_number, \
        video_number, photo_number, \
        photo_task_number, video_task_nummber, \
        invalid_task_number, unkown_media_task_number, \
        total_task_number = 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0

        userId = userName = \
            userAccount = userDescription = \
            followingCount = followersCount = \
            statusesCount = mediaCount = \
            favouritesCount = userDataDir = None

        proxy = {
            "http": "http://127.0.0.1:7890",
            "https": "http://127.0.0.1:7890"
        }
        twitter_headers = {
            "Accept": "*/*",
            "Accept-Encoding": "gzip, deflate, br",
            "Accept-Language": "zh-CN,zh;q=0.9,en;q=0.8",
            "Authorization": "Bearer AAAAAAAAAAAAAAAAAAAAANRILgAAAAAAnNwIzUejRCOuH5E6I8xnZz4puTs%3D1Zv7ttfk8LF81IUq16cHjhLTvJu4FA33AGWWjCpTnA",
            "Content-Type": "application/json",
            "Cookie": "g_state={\"i_l\":0}; kdt=3sXNS1DdqrHfaqEbIhXrqnqrJihu5RidDiPYiw3h; _gid=GA1.2.1781708517.1688173889; _ga_BYKEBDM7DS=GS1.1.1688283625.1.1.1688284145.0.0.0; des_opt_in=Y; _gcl_au=1.1.2059649976.1688284250; mbox=session#0136b8c5c2644f3e86d0e002bcb4d21f#1688286454|PC#0136b8c5c2644f3e86d0e002bcb4d21f.32_0#1751529394; _ga_34PHSZMC42=GS1.1.1688284252.1.1.1688284783.0.0.0; lang=zh-cn; _ga=GA1.2.1396655875.1686386799; ads_prefs=\"HBERAAA=\"; auth_multi=\"1483103124390821898:12e3c8b106b1656fb89e7a0f96af4654b63cdc10\"; auth_token=1327450bb025f09c7c7e417caa189fb767f91bb5; guest_id=v1%3A168829441028733029; ct0=c0fa49c419a67a8d8224ca09575b5b5caee3600ed4b60def62e076087a8ff8b4a8ac664caca565d3ab830ca60dd879b6ecd0ef944f0ab2867ca9fb958e8dd939c9f83a5a719a95677307890f1ab8e821; twid=u%3D1611959677910409216; guest_id_marketing=v1%3A168829441028733029; guest_id_ads=v1%3A168829441028733029; personalization_id=\"v1_/W2JQNgtM5OAA/jKYrwH7A==\"",
            "Referer": "https://twitter.com/AceTaiwan/",
            "Sec-Ch-Ua": "\"Not.A/Brand\";v=\"8\", \"Chromium\";v=\"114\", \"Google Chrome\";v=\"114\"",
            "Sec-Ch-Ua-Mobile": "?0",
            "Sec-Ch-Ua-Platform": "\"Windows\"",
            "Sec-Fetch-Dest": "empty",
            "Sec-Fetch-Mode": "cors",
            "Sec-Fetch-Site": "same-origin",
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36",
            "X-Csrf-Token": "c0fa49c419a67a8d8224ca09575b5b5caee3600ed4b60def62e076087a8ff8b4a8ac664caca565d3ab830ca60dd879b6ecd0ef944f0ab2867ca9fb958e8dd939c9f83a5a719a95677307890f1ab8e821",
            "X-Twitter-Active-User": "yes",
            "X-Twitter-Auth-Type": "OAuth2Session",
            "X-Twitter-Client-Language": "zh-cn",
        }

        twimg_http_headers = {
            'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
            'accept-encoding': 'gzip, deflate, br',
            'accept-language': 'zh-CN,zh;q=0.9',
            'cache-control': 'no-cache',
            'pragma': 'no-cache',
            'sec-ch-ua': '" Not A;Brand";v="99", "Chromium";v="101", "Google Chrome";v="101"',
            'sec-ch-ua-mobile': '?0',
            'sec-ch-ua-platform': '"Windows"',
            'sec-fetch-dest': 'document',
            'sec-fetch-mode': 'navigate',
            'sec-fetch-site': 'none',
            'sec-fetch-user': '?1',
            'upgrade-insecure-requests': '1',
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/101.0.4951.67 Safari/537.36'
        }

        self.__dict__.update(locals())

    def getRawfileName(self, i):
        rawfile = self.rawfiles_dir + f'\\rawfile-{i}.txt'
        return rawfile

    #用户主页信息的URL
    def getUserInfoUrl(self,user_account):
        userInfoUrl = 'https://twitter.com/i/api/graphql/SAMkL5y_N9pmahSw8yy6gw/UserByScreenName?variables={"screen_name":"' + user_account + '","withSafetyModeUserFields":true}&features={"hidden_profile_likes_enabled":false,"hidden_profile_subscriptions_enabled":true,"responsive_web_graphql_exclude_directive_enabled":true,"verified_phone_label_enabled":false,"subscriptions_verification_info_is_identity_verified_enabled":false,"subscriptions_verification_info_verified_since_enabled":true,"highlights_tweets_tab_ui_enabled":true,"creator_subscriptions_tweet_preview_api_enabled":true,"responsive_web_graphql_skip_user_profile_image_extensions_enabled":false,"responsive_web_graphql_timeline_navigation_enabled":true}&fieldToggles={"withAuxiliaryUserLabels":false}'
        return userInfoUrl

    #媒体数据的URL
    def getMediaInfoUrl(self,cursor_index,user_id,count,cursor_id):

        if cursor_index == 1:
            mediaInfoUrl = 'https://twitter.com/i/api/graphql/fswZGPS7zuksnISWCMvz3Q/UserMedia?variables={"userId":"' + user_id + '","count":' + count + ',"includePromotedContent":false,"withClientEventToken":false,"withBirdwatchNotes":false,"withVoice":true,"withV2Timeline":true}&features={"rweb_lists_timeline_redesign_enabled":true,"responsive_web_graphql_exclude_directive_enabled":true,"verified_phone_label_enabled":false,"creator_subscriptions_tweet_preview_api_enabled":true,"responsive_web_graphql_timeline_navigation_enabled":true,"responsive_web_graphql_skip_user_profile_image_extensions_enabled":false,"tweetypie_unmention_optimization_enabled":true,"responsive_web_edit_tweet_api_enabled":true,"graphql_is_translatable_rweb_tweet_is_translatable_enabled":true,"view_counts_everywhere_api_enabled":true,"longform_notetweets_consumption_enabled":true,"responsive_web_twitter_article_tweet_consumption_enabled":false,"tweet_awards_web_tipping_enabled":false,"freedom_of_speech_not_reach_fetch_enabled":true,"standardized_nudges_misinfo":true,"tweet_with_visibility_results_prefer_gql_limited_actions_policy_enabled":true,"longform_notetweets_rich_text_read_enabled":true,"longform_notetweets_inline_media_enabled":true,"responsive_web_media_download_video_enabled":false,"responsive_web_enhance_cards_enabled":false}'
        else:
            mediaInfoUrl = 'https://twitter.com/i/api/graphql/fswZGPS7zuksnISWCMvz3Q/UserMedia?variables={"userId":"' + user_id + '","count":' + count + ',"cursor":"' + cursor_id + '","includePromotedContent":false,"withClientEventToken":false,"withBirdwatchNotes":false,"withVoice":true,"withV2Timeline":true}&features={"rweb_lists_timeline_redesign_enabled":true,"responsive_web_graphql_exclude_directive_enabled":true,"verified_phone_label_enabled":false,"creator_subscriptions_tweet_preview_api_enabled":true,"responsive_web_graphql_timeline_navigation_enabled":true,"responsive_web_graphql_skip_user_profile_image_extensions_enabled":false,"tweetypie_unmention_optimization_enabled":true,"responsive_web_edit_tweet_api_enabled":true,"graphql_is_translatable_rweb_tweet_is_translatable_enabled":true,"view_counts_everywhere_api_enabled":true,"longform_notetweets_consumption_enabled":true,"responsive_web_twitter_article_tweet_consumption_enabled":false,"tweet_awards_web_tipping_enabled":false,"freedom_of_speech_not_reach_fetch_enabled":true,"standardized_nudges_misinfo":true,"tweet_with_visibility_results_prefer_gql_limited_actions_policy_enabled":true,"longform_notetweets_rich_text_read_enabled":true,"longform_notetweets_inline_media_enabled":true,"responsive_web_media_download_video_enabled":false,"responsive_web_enhance_cards_enabled":false}'
        return mediaInfoUrl




    # jsonpath---------->Req_UserInfo

    def getJsonPaths1(self):
        user_id_path = '$.data.user.result.rest_id'
        user_name_path = '$.data.user.result.legacy.name'
        user_account_path = '$.data.user.result.legacy.screen_name'
        user_description_path = '$.data.user.result.legacy.description'
        following_count_path = '$.data.user.result.legacy.friends_count'
        followers_count_path = '$.data.user.result.legacy.followers_count'
        statuses_count_path = '$.data.user.result.legacy.statuses_count'
        media_count_path = '$.data.user.result.legacy.media_count'
        favourites_count_path = '$.data.user.result.legacy.favourites_count'

        return user_id_path,user_name_path,user_account_path,user_description_path,following_count_path,followers_count_path,statuses_count_path,media_count_path,favourites_count_path


    #jsonpath---------->File_MediaDataToCsv

    def getJsonPaths2(self,i):
        tweet_id_path1 = f'$.data.user.result.timeline_v2.timeline.instructions[0].entries[{i}].content.itemContent.tweet_results.result.legacy.id_str'
        tweet_id_path2 = f'$.data.user.result.timeline_v2.timeline.instructions[0].entries[{i}].content.itemContent.tweet_results.result.tweet.legacy.id_str'
        tweet_time_path1 = f'$.data.user.result.timeline_v2.timeline.instructions[0].entries[{i}].content.itemContent.tweet_results.result.legacy.created_at'
        tweet_time_path2= f'$.data.user.result.timeline_v2.timeline.instructions[0].entries[{i}].content.itemContent.tweet_results.result.tweet.legacy.created_at'
        tweet_content_path1 = f'$.data.user.result.timeline_v2.timeline.instructions[0].entries[{i}].content.itemContent.tweet_results.result.legacy.full_text'
        tweet_content_path2 = f'$.data.user.result.timeline_v2.timeline.instructions[0].entries[{i}].content.itemContent.tweet_results.result.tweet.legacy.full_text'
        media_type_path = f'$.data.user.result.timeline_v2.timeline.instructions[0].entries[{i}].content.itemContent.tweet_results.result.legacy.extended_entities.media[0].type'
        favorite_count_path1 = f'$.data.user.result.timeline_v2.timeline.instructions[0].entries[{i}].content.itemContent.tweet_results.result.legacy.favorite_count'
        favorite_count_path2= f'$.data.user.result.timeline_v2.timeline.instructions[0].entries[{i}].content.itemContent.tweet_results.result.tweet.legacy.favorite_count'
        reply_count_path1 = f'$.data.user.result.timeline_v2.timeline.instructions[0].entries[{i}].content.itemContent.tweet_results.result.legacy.reply_count'
        reply_count_path2 = f'$.data.user.result.timeline_v2.timeline.instructions[0].entries[{i}].content.itemContent.tweet_results.result.tweet.legacy.reply_count'

        retweet_count_path1 = f'$.data.user.result.timeline_v2.timeline.instructions[0].entries[{i}].content.itemContent.tweet_results.result.legacy.retweet_count'
        retweet_count_path2 = f'$.data.user.result.timeline_v2.timeline.instructions[0].entries[{i}].content.itemContent.tweet_results.result.tweet.legacy.retweet_count'
        end_flag_path = f'$.data.user.result.timeline_v2.timeline.instructions[0].entries[{i}].content.cursorType'
        return tweet_id_path1, tweet_id_path2,tweet_time_path1,tweet_time_path2,tweet_content_path1,tweet_content_path2,media_type_path,favorite_count_path1,favorite_count_path2,reply_count_path1,reply_count_path2,retweet_count_path1,retweet_count_path2,end_flag_path

    #jsonpath----------->Req_DownloadMedia

    def getJsonPaths3(self,i):
        tweet_id_path1 = f'$.data.user.result.timeline_v2.timeline.instructions[0].entries[{i}].content.itemContent.tweet_results.result.legacy.id_str'
        tweet_id_path2 = f'$.data.user.result.timeline_v2.timeline.instructions[0].entries[{i}].content.itemContent.tweet_results.result.tweet.legacy.id_str'
        media_path1 = f'$.data.user.result.timeline_v2.timeline.instructions[0].entries[{i}].content.itemContent.tweet_results.result.legacy.extended_entities.media'
        media_path2 = f'$.data.user.result.timeline_v2.timeline.instructions[0].entries[{i}].content.itemContent.tweet_results.result.tweet.legacy.extended_entities.media'
        media_type1 = f'$.data.user.result.timeline_v2.timeline.instructions[0].entries[{i}].content.itemContent.tweet_results.result.legacy.extended_entities.media[0].type'
        media_type2 = f'$.data.user.result.timeline_v2.timeline.instructions[0].entries[{i}].content.itemContent.tweet_results.result.tweet.legacy.extended_entities.media[0].type'

        end_flag_path = f'$.data.user.result.timeline_v2.timeline.instructions[0].entries[{i}].content.cursorType'

        return tweet_id_path1,tweet_id_path2,media_path1,media_path2,end_flag_path,media_type1,media_type2


    def getInvalidTweetID(self,i):
        invalid_task_id_path = f'$.data.user.result.timeline_v2.timeline.instructions[0].entries[{i}].entryId'
        return invalid_task_id_path

    # jsonpath----------->SaveMediaToExcel

    def getJsonPath4(self,i):
        cursor_id_path = f'$.data.user.result.timeline_v2.timeline.instructions[0].entries[{i}].content.value'
        cursorType_path = f'$.data.user.result.timeline_v2.timeline.instructions[0].entries[{i}].content.cursorType'
        return cursor_id_path, cursorType_path

config = Config()
