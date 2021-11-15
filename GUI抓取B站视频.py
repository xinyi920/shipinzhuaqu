# coding:utf-8
# Time:2021-11-14    23:19
# Version:3.9.1
# Title:GUI抓取B站视频.py
# Author:歆逸
import tkinter as tk
import requests
import re
import json
import time
import os
import subprocess


headers = {
    'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/95.0.4638.69 Safari/537.36',
    'referer': 'https://www.bilibili.com/',
}


def send_request(html_url):
    response = requests.get(url=html_url, headers=headers)
    return response


def get_url(info_data):
    title = re.findall(r'<title data-vue-meta="true">(.*?)_哔哩哔哩_bilibili</title>', info_data, re.S)[0]
    info = json.loads(re.findall(r'<script>window.__playinfo__=(.*?)</script>', info_data, re.S)[0])
    audio_url = info['data']['dash']['audio'][0]['backupUrl'][0]
    video_url = info['data']['dash']['video'][0]['backupUrl'][0]
    video_ = [title, audio_url, video_url]
    return video_


def save_data(title, audio_url, video_url):
    # 音频保存
    audio_data = send_request(audio_url).content
    with open(title + '.mp3', 'wb') as f:
        f.write(audio_data)
    # 视频保存
    video_data = send_request(video_url).content
    with open(title + '.mp4', 'wb') as f:
        f.write(video_data)


def merge_video(video_name):
    command = f'ffmpeg -i {video_name}.mp4 -i {video_name}.mp3 -c:v copy -c:a aac -strict experimental {video_name + "-new"}.mp4'
    subprocess.Popen(command, shell=True)


def rename(name):
    if os.path.isfile(name + '.mp3'):
        os.remove(name + '.mp3')
    if os.path.isfile(name + '.mp4'):
        os.remove(name + '.mp4')
    os.rename(name + '-new.mp4', name + '.mp4')


def click():
    url = E1.get()
    data = send_request(url).text
    info_data = get_url(data)
    save_data(info_data[0], info_data[1], info_data[2])
    merge_video(info_data[0])
    time.sleep(5)
    rename(info_data[0])


window = tk.Tk(className='B站视频抓取')
window.geometry('700x450')
# 标签
L1 = tk.Label(window, text='请输入视频网址', font=('宋体', 15))
L1.place(x=250, y=80)
# 输入文本
E1 = tk.Entry(window, font=('宋体', 15), show=None, width=18)
E1.place(x=350, y=80)
# 查询按钮
button = tk.Button(window, text='确定', font=('宋体', 15), width=10, height=1, command=click)
button.place(x=300, y=180)

window.mainloop()
