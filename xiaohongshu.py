# coding:utf-8
import time

from appium import webdriver
from pymongo import MongoClient
import threading


# # 链接数据库
con = MongoClient('127.0.0.1', 27017)
db = con.xiaohongshu
cur = db.xhs


caps = {
    "platformName": "Android",
    "deviceName": "127.0.0.1:62025",
    "appPackage": "com.xingin.xhs",
    "platformVersion": "5.1.1",
    "appActivity": ".activity.SplashActivity",
    "noReset": True,  # 免登陆TRUE
    "unicodeKeyboard": True  # 解决不能输入中文的问题
    }


# 获得屏幕尺寸数据
def getSize():
    x = driver.get_window_size()['width']
    y = driver.get_window_size()['height']
    return (x, y)


# 屏幕向下滑动
def swipeUp():
    l = getSize()
    x1 = int(l[0] * 0.5)  # x坐标
    y1 = int(l[1] * 0.75)  # 起始y坐标
    y2 = int(l[1] * 0.25)  # 终点y坐标
    driver.swipe(x1, y1, x1, y2)


# 屏幕向上滑动
def swipeDown():
    l = getSize()
    x1 = int(l[0] * 0.5)  # x坐标
    y1 = int(l[1] * 0.25)  # 起始y坐标
    y2 = int(l[1] * 0.75)  # 终点y坐标
    driver.swipe(x1, y1, x1, y2)


# 获取想要的数据
def data():
    title = driver.find_element_by_id("com.xingin.xhs:id/bdb").text
    content = driver.find_element_by_id("com.xingin.xhs:id/bbo").text
    print("标题------>", title)
    print("内容------>", content)
    swipeUp()
    # swipeUp(3500)

    try:
        collect = driver.find_element_by_id("com.xingin.xhs:id/bcc").text
    except Exception as e:
        print(e)
        collect = '无收藏'

    try:
        like_num = driver.find_element_by_id("com.xingin.xhs:id/bd3").text
    except Exception as e:
        print(e)
        like_num = '无点赞'

    try:
        comments = driver.find_elements_by_id("com.xingin.xhs:id/bbo")[1].text
    except Exception as e:
        print(e)
        comments = '无评论'

    data = {'title': title, 'content': content, 'comments': comments, 'collect': collect, 'like_num': like_num}
    print('存入数据库前。。。。。。。。。。。。')
    cur.insert(data)
    print('存入成功。。。。。。。。。。')


if __name__ == '__main__':

    # 链接app
    driver = webdriver.Remote('http://127.0.0.1:4723/wd/hub', caps)
    time.sleep(2)
    # 首页输入框
    t = driver.find_element_by_id("com.xingin.xhs:id/we").click()
    time.sleep(2)
    # 真实输入框
    text = driver.find_element_by_id("com.xingin.xhs:id/aiw")
    time.sleep(2)
    text.send_keys(u'巴黎欧莱雅')
    time.sleep(2)
    # 搜索按键
    driver.find_element_by_id("com.xingin.xhs:id/aiz").click()
    time.sleep(2)
    # 向下滑动，刷新数据
    swipeDown()
    # swipeDown(500)
    time.sleep(2)

    while True:
        print("begin======-------=======")
        try:
            # 点击进入详情页面
            driver.find_element_by_id('com.xingin.xhs:id/ahd').click()
            time.sleep(3)
            data()
            swipeDown()
            # swipeDown(1000)
            time.sleep(2)
            # 返回上一页
            driver.find_element_by_class_name('android.widget.ImageButton').click()
            # time.sleep(2)
            swipeUp()
            # swipeUp(200)
            # 测试第二次进入
            driver.find_element_by_id('com.xingin.xhs:id/ahd').click()
            time.sleep(3)
            data()

            swipeDown()
            # swipeDown(1000)
            # 返回上一页
            driver.find_element_by_class_name('android.widget.ImageButton').click()
            swipeUp()
            # swipeUp(200)
            # time.sleep(2)
        except:
            driver.find_element_by_id('com.xingin.xhs:id/a4g').click()
            time.sleep(2)
            swipeUp()
            # swipeUp(350)
# com.xingin.xhs:id/d8
# com.xingin.xhs:id/a4g

# com.xingin.xhs:id/a4g