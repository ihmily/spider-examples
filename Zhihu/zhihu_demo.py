"""
Author: Hmily
Date: 2023-03-29 17:18:20
Copyright (c) 2023 by Hmily, All Rights Reserved.
Function:Download the nomark zhihu video
"""


import json
import re
import requests
from datetime import datetime


headers = {
    'User-Agent': 'Mozilla/5.0 (Linux; Android 11; SAMSUNG SM-G973U) AppleWebKit/537.36 (KHTML, like Gecko) SamsungBrowser/14.2 Chrome/87.0.4280.141 Mobile Safari/537.36',
    'Referer': 'https://www.zhihu.com/zvideo/1590490812885905409?utm_source=pc_tab&utm_id=0',
    'content-type': 'application/json',
    'vod-authorization': 'V1-424ff0a50c34f5f188dc8a7ee1ef2117-0-4b87899ace2a11ed8260ce04b7535add-1680091656947-1680113256947-f3d346b9eb04709e928db995b465cf732940439c8cf8f27e0bb901aaa6877106',
    'Origin': 'https://www.zhihu.com',
}


def get_zvid(url) -> str:
    match_zvid = re.search("zvideo\/(.*?)(?:\?|$)", url)
    zvid = match_zvid.group(1)
    return zvid

def get_base_msg(zvid):
    # 能获取到视频的基本信息，但视频链接都是有水印的
    url = f"https://lens.zhihu.com/api/zvideos/{zvid}/recommendations"
    response = requests.get(url)
    json_data = response.json()
    print(json_data)

def get_sub_video_id(zvid) -> str:
    url = f'https://www.zhihu.com/api/v4/zvideo-contribute/zvideos/{zvid}/contributions?scene=view'
    response = requests.get(url, headers=headers)
    json_data = response.json()
    # print(json_data)
    sub_video_id = json_data[0]["sub_video_id"]
    return sub_video_id


def get_video_url(sub_video_id,auth_token):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Linux; Android 11; SAMSUNG SM-G973U) AppleWebKit/537.36 (KHTML, like Gecko) SamsungBrowser/14.2 Chrome/87.0.4280.141 Mobile Safari/537.36',
        'vod-authorization': auth_token,
        'Origin': 'https://www.zhihu.com',
    }
    url = f'https://lens.zhihu.com/api/v4/videos/{sub_video_id}'
    response = requests.get(url, headers=headers)
    print(response.json())


# 不必那么麻烦，直接从HTML中就可以获取视频所有信息
def get_video_msg(url, zvid):
    response = requests.get(url, headers=headers)
    html_str = response.text
    json_str = re.search('<script id="js-initialData" type="text/json">(.*?)</script><script crossorigin=', html_str)
    json_str = json_str.groups(1)[0]
    json_data = json.loads(json_str)
    zvideos = json_data["initialState"]["entities"]["zvideos"][zvid]
    title = zvideos["title"]
    description = zvideos["description"]
    author_name = zvideos["video"]["components"][0]["content"]["user"]["name"]
    author_id = zvideos["author"]
    publishedAt=datetime.fromtimestamp(zvideos["publishedAt"])
    published_time = publishedAt.strftime("%Y-%m-%d %H:%M:%S")
    updatedAt = datetime.fromtimestamp(zvideos["updatedAt"])
    updated_time = updatedAt.strftime("%Y-%m-%d %H:%M:%S")

    playCount = zvideos["playCount"]
    voteupCount = zvideos["voteupCount"]
    likedCount = zvideos["likedCount"]
    commentCount = zvideos["commentCount"]
    shareCount = zvideos["shareCount"]
    ipInfo = zvideos["ipInfo"]
    linkUrl = zvideos["linkUrl"]
    playAuthToken = zvideos["video"]["playAuthToken"]
    cover_url = zvideos["imageUrl"]
    video_url = zvideos["video"]["playlist"]["fhd"]["playUrl"]

    print("标题:", title)
    print("描述:", description)
    print("作者:", author_name)
    print("作者id:", author_id)
    print("发布时间:", published_time)
    print("更新时间:", updated_time)
    print("播放数量:", playCount)
    print("赞同数量:", voteupCount)
    print("喜欢数量:", likedCount)
    print("评论数量:", commentCount)
    print("转发数量:", shareCount)
    print("ip归属:", ipInfo)
    print("视频页面地址:", linkUrl)
    print("请求token:", playAuthToken)
    print("封面下载地址:", cover_url)
    print("视频下载地址:", video_url)
    return playAuthToken



if __name__ == '__main__':

    url = "https://www.zhihu.com/zvideo/1590490812885905409?utm_source=pc_tab&utm_id=0"
    zvid = get_zvid(url)
    sub_video_id = get_sub_video_id(zvid)
    auth_token=get_video_msg(url, zvid)
    get_video_url(sub_video_id,auth_token)
