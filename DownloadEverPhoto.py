#!/usr/bin/env python
# -*- coding:utf-8 -*-

import asyncio
import time
import os
# from pyppeteer import launch
import requests
import json


async def main():
    """使用pyppeteer库来登录时光相册、并获取cookie
    """
    browser = await launch(headless=False, dumpio=True, autoClose=False,
                           args=['--no-sandbox', '--window-size=1024,800', '--disable-infobars'])   # 进入有头模式
    context = await browser.createIncognitoBrowserContext() # 隐身模式
    page = await context.newPage()           # 打开新的标签页
    print('~~~~ 请在弹出的网页中登录账号~~~~')
    # 访问主页、增加超时解决Navigation Timeout Exceeded: 30000 ms exceeded报错
    await page.setViewport({'width': 1024, 'height': 800})      
    await page.goto('https://web.everphoto.cn/#signin',{'timeout': 1000*60})


    await page.waitFor(1000)
    # 通过判断用户头像是否存在来确定登录状态
    elm = await page.waitForXPath('//*[@id="navigatorDropdown"]',timeout=0)
    if elm:
        cookie = await page.cookies()
        # print(cookie)
        
        # 遍历列表，找到包含access_token的字典
        access_token = None
        for item in cookie:
            if item.get('name') == 'access_token':
                access_token = item.get('value')
                break
        print(f"Token", {access_token})
        get_download_url(access_token,cookie)
        # time.sleep(10)



def get_download_url(access_token,cookie):
    """获取时光相册的下载url地址
    """
    
    # 认证信息
    url = "https://web.everphoto.cn/api/media/archive"
    # access_token = ""

    # 添加请求头，并参数化
    headers = {
        "Referer": "https://web.everphoto.cn/",
        "Sec-Ch-Ua-Platform": "\"Windows\"",
        "Sec-Fetch-Site": "same-origin",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.0.0 Safari/537.36 Edg/115.0.1901.203",
        "x-bigint-support": "false",
        # "X-Uid": x_uid,
        "Cookie": f"{cookie}",
        "Authorization": f"Bearer {access_token}"
    }

    data = {
        "param1": "value1",
        "param2": "value2"
    }

    # 发送 POST 请求
    response = requests.post(url, headers=headers, data=data)

    # 检查响应状态码
    if response.status_code == 200:
        # print("请求成功")
        # print("返回内容:", response.text)  
        # 解析 JSON 响应
        response_json = json.loads(response.text)
        
        # 提取 URL 值
        download_url = response_json['data']['url']
        print(f"提取到的下载地址:", {download_url})
        download_EverPhoto(download_url, access_token,cookie)
    else:
        print(f"请求失败，状态码:", {response.status_code})


def download_EverPhoto(url,access_token,cookie):
    # 下载时光相册的照片
    # 下载文件的URL

    # 添加access_token和x_uid
    # access_token = ""

    # 添加请求头，并参数化
    headers = {
        "Referer": "https://web.everphoto.cn/",
        "Sec-Ch-Ua-Platform": "\"Windows\"",
        "Sec-Fetch-Site": "same-origin",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.0.0 Safari/537.36 Edg/115.0.1901.203",
        "x-bigint-support": "false",
        # "X-Uid": x_uid,
        "Cookie": f"{cookie}",
        "Authorization": f"Bearer {access_token}"
    }

    # 发送GET请求并获取响应
    print(f"下载地址", {url})
    print(f"Token", {access_token})
    response = requests.get(url, headers=headers, stream=True)

    if response.status_code == 200:
        # 解析响应头部信息获取文件名
        content_disposition = response.headers.get("content-disposition")
        filename = content_disposition.split("filename=")[-1].strip("\"'")

        # 保存文件的目录
        current_directory = os.getcwd()
        save_directory = os.path.join(current_directory, "download")

        # 检查目录是否存在，如果不存在则创建
        if not os.path.exists(save_directory):
            os.makedirs(save_directory)

        # 构建保存文件的完整路径
        file_path = os.path.join(save_directory, filename)

        # 保存文件并显示下载速度和已下载的文件大小
        with open(file_path, "wb") as file:
            start_time = time.time()
            downloaded_size = 0
            chunk_size = 1024
            for chunk in response.iter_content(chunk_size=chunk_size):
                if chunk:
                    file.write(chunk)
                    downloaded_size += len(chunk)
                    elapsed_time = time.time() - start_time
                    if elapsed_time > 0:  # 检查下载时间是否大于零
                        download_speed = downloaded_size / elapsed_time / (1024 * 1024)  # 将字节转换为兆字节
                        downloaded_size_mb = downloaded_size / (1024 * 1024)  # 将字节转换为兆字节
                    else:
                        download_speed = 0
                        downloaded_size_mb = 0
                    print(f"已下载: {downloaded_size_mb:.2f} MB, 下载速度: {download_speed:.2f} MB/s")

        print(f"文件已下载并保存为 {file_path}")
        os.system('pause')
    else:
        print(f"下载失败，错误代码: {response.status_code}")

if __name__== "__main__":
    exc = """
        1、将程序放到磁盘空间比较大的盘符中
        2、直接运行程序即可
        3、在弹出的网页中登录时光相册
        4、下载完成之后照片存放在当前目录的download中
        5、直接解压即可
    """
    print(exc)
    os.system('pause')
    print(f"~~~~~~~~~~ 开始准备环境  ~~~~~~~~~~")
    
    # 设置 Chromium的下载地址为淘宝的国内源，解决Google源下载失败的问题
    DEFAULT_DOWNLOAD_HOST = 'https://npm.taobao.org/mirrors'
    os.environ["PYPPETEER_DOWNLOAD_HOST"] = DEFAULT_DOWNLOAD_HOST
    from pyppeteer import launch
    asyncio.get_event_loop().run_until_complete(main()) #调用