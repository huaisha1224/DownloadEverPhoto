#!/usr/bin/env python
# -*- coding:utf-8 -*-

import os
import datetime
from pymediainfo import MediaInfo
from PIL import Image
from PIL.ExifTags import TAGS

SUPPORTED_FORMATS = [".mov", ".mp4", ".avi", ".mkv", ".jpg", ".jpeg", ".png"]

def rename_media_files(directory):
    """
    重命名给定目录中的视频和照片文件。

    参数：
    - directory：视频和照片文件所在的目录路径
    """
    try:
        for filename in os.listdir(directory):
            # 检查文件是否为支持的视频或照片格式
            if any(filename.endswith(format) for format in SUPPORTED_FORMATS):
                file_path = os.path.join(directory, filename)
                try:
                    # 获取文件的创建日期
                    creation_date = get_creation_date(file_path)
                    if creation_date:
                        # 生成新的文件名
                        new_filename = generate_new_filename(directory, filename, creation_date)
                        new_file_path = os.path.join(directory, new_filename)
                        # 重命名文件
                        os.rename(file_path, new_file_path)
                        print(f"重命名 {filename} 为 {new_filename}")
                    else:
                        print(f"没有获取到拍摄日期 {filename}")
                except Exception as e:
                    print(f"报错啦 {file_path}: {e}")
    except FileNotFoundError:
        print(f"目录不存在: {directory}")
    except PermissionError:
        print(f"没有权限: {directory}")

def get_creation_date(file_path):
    """
    获取文件的创建日期。

    参数：
    - file_path：文件的路径

    返回：
    - 创建日期（datetime对象）或None（如果无法获取创建日期）
    """
    try:
        # 检查文件是否为视频文件
        if file_path.endswith((".mov", ".mp4", ".avi", ".mkv")):
            # 使用 pymediainfo 解析视频文件的元数据
            media_info = MediaInfo.parse(file_path)
            for track in media_info.tracks:
                # 检查是否是视频轨道
                if track.track_type == "Video":
                    creation_date_str = track.encoded_date
                    if creation_date_str:
                        # 将字符串形式的日期转换为 datetime 对象
                        creation_date = datetime.datetime.strptime(creation_date_str, "%Z %Y-%m-%d %H:%M:%S")
                        return creation_date
        # 检查文件是否为照片文件
        elif file_path.endswith((".jpg", ".jpeg", ".png")):
            # 使用 PIL 解析照片文件的 Exif 数据
            with Image.open(file_path) as image:
                exif_data = image._getexif()
                if exif_data:
                    # 获取 Exif 数据中的拍摄日期
                    for tag_id, value in exif_data.items():
                        tag = TAGS.get(tag_id, tag_id)
                        if tag == "DateTimeOriginal":
                            creation_date_str = value
                            # 将字符串形式的日期转换为 datetime 对象
                            creation_date = datetime.datetime.strptime(creation_date_str, "%Y:%m:%d %H:%M:%S")
                            return creation_date
        return None
    except Exception as e:
        print(f"获取拍摄日期时出错 {file_path}: {e}")
        return None

def generate_new_filename(directory, filename, creation_date):
    """
    生成新的文件名。

    参数：
    - directory：视频和照片文件所在的目录路径
    - filename：文件的原始文件名
    - creation_date：文件的创建日期（datetime对象）

    返回：
    - 新的文件名（字符串）
    """
    try:
        base_filename = creation_date.strftime("%Y%m%d_%H%M")
        extension = os.path.splitext(filename)[1]
        new_filename = base_filename + extension
        count = 1
        # 如果新文件名已存在，则添加数字后缀
        while os.path.exists(os.path.join(directory, new_filename)):
            new_filename = base_filename + "_" + str(count).zfill(2) + extension
            count += 1
        return new_filename
    except Exception as e:
        print(f"生成新文件名时出错 {filename}: {e}")
        return filename

if __name__== "__main__":
    exc = """
                            　　 へ　　　　　／|
                        　　/＼7　　　 ∠＿/
                        　 /　│　　 ／　／
                        　│　Z ＿,＜　／　　 /`ヽ
                        　│　　　　　ヽ　　 /　　〉
                        　 Y　　　　　`　 /　　/
                        　●　　●　　〈　　/
                        　()　 へ　　　　|　＼〈
                        　　> _　 ィ　 │ ／／
                        　 / へ　　 /　＜| ＼＼
                        　 ヽ_　　(_／　 │／／
                        　　7　　　　　　　|／
                        　　＞―r￣￣`―＿
            1、直接运行程序
            2、输入需要处理的照片和视频的目录
            3、回车后开始处理，按照照片和视频的拍摄时间修改原文件名
            4、如果时间重复会自增编号
            5、没有获取到拍摄时间的文件不处理
        """
    # 调用函数并传入视频文件所在的目录
    # rename_media_files(r"D:\Python_Code\DownloadEverPhoto\mov")
    print(exc)
    directory = input("请输入视频和照片文件所在的目录路径：")
    rename_media_files(directory)
    os.system('pause')