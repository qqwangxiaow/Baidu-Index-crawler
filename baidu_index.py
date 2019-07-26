# !/usr/bin/python3.4
# -*- coding: utf-8 -*-

# 百度指数的抓取
import os
import time
import datetime
from selenium import webdriver
from selenium.webdriver.common.action_chains import ActionChains

import csv


# tesseract安装路径，及图片库，百度指数改版，暂时不需要图片识别了
# import pytesseract
# pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files (x86)\Tesseract-OCR\tesseract.exe"
# from PIL import Image

# 电影信息文件和保存指数的文件
MOVIE_INFO_FILE = 'movie_info.csv'
INDEX_FILE = 'movie_baidu_index.csv'

# 打开浏览器和登录
def open_browser():
    global browser

    # https://passport.baidu.com/v2/?login
    url = "https://passport.baidu.com/v2/?login&tpl=mn&u=http%3A%2F%2Fwww.baidu.com%2F"

    # 使用Chrome,需指明chromedriver的安装位置
    browser = webdriver.Chrome("C:/Users/yuanjc/chromedriver")
    browser.get(url)
    # 输入网址
    # 打开浏览器时间
    # print("等待10秒打开浏览器...")
    # time.sleep(10)
    browser.find_element_by_id("TANGRAM__PSP_3__footerULoginBtn").click()
    # 找到id="TANGRAM__PSP_3__userName"的对话框
    # 清空输入框
    browser.find_element_by_id("TANGRAM__PSP_3__userName").clear()
    browser.find_element_by_id("TANGRAM__PSP_3__password").clear()

    # 输入账号密码
    # 输入账号密码
    account = []
    try:
        fileaccount = open("baidu/account.txt", encoding='UTF-8')
        accounts = fileaccount.readlines()
        for acc in accounts:
            account.append(acc.strip())
        fileaccount.close()
    except Exception as err:
        print(err)
        input("请正确在account.txt里面写入账号密码")
        exit()
    browser.find_element_by_id("TANGRAM__PSP_3__userName").send_keys(account[0])
    browser.find_element_by_id("TANGRAM__PSP_3__password").send_keys(account[1])

    # 点击登陆登陆
    # id="TANGRAM__PSP_3__submit"
    browser.find_element_by_id("TANGRAM__PSP_3__submit").click()

    # 等待登陆10秒
    # print('等待登陆10秒...')
    # time.sleep(10)
    print("等待网址加载完毕...")

    select = input("请观察浏览器网站是否已经登陆(y/n)：")
    while True:
        if select == "y" or select == "Y":
            print("登陆成功！")
            print("准备打开新的窗口...")
            # time.sleep(1)
            # browser.quit()
            break

        elif select == "n" or select == "N":
            selectno = input("账号密码错误请按0，验证码出现请按1...")
            # 账号密码错误则重新输入
            if selectno == "0":

                # 找到id="TANGRAM__PSP_3__userName"的对话框
                # 清空输入框
                browser.find_element_by_id("TANGRAM__PSP_3__userName").clear()
                browser.find_element_by_id("TANGRAM__PSP_3__password").clear()

                # 输入账号密码
                account = []
                try:
                    fileaccount = open("baidu/account.txt", encoding='UTF-8')
                    accounts = fileaccount.readlines()
                    for acc in accounts:
                        account.append(acc.strip())
                    fileaccount.close()
                except Exception as err:
                    print(err)
                    input("请正确在account.txt里面写入账号密码")
                    exit()

                browser.find_element_by_id("TANGRAM__PSP_3__userName").send_keys(account[0])
                browser.find_element_by_id("TANGRAM__PSP_3__password").send_keys(account[1])
                # 点击登陆sign in
                # id="TANGRAM__PSP_3__submit"
                browser.find_element_by_id("TANGRAM__PSP_3__submit").click()

            elif selectno == "1":
                # 验证码的id为id="ap_captcha_guess"的对话框
                input("请在浏览器中输入验证码并登陆...")
                select = input("请观察浏览器网站是否已经登陆(y/n)：")

        else:
            print("请输入“y”或者“n”！")
            select = input("请观察浏览器网站是否已经登陆(y/n)：")


def get_index(infolist, searched_list):

    # 保存百度指数的文件
    csvheaders = ['movie_name', 'date']
    for i in range(1, 30):
        csvheaders.append(i)
    if not os.path.exists(INDEX_FILE):
        index_csvfile = open(INDEX_FILE, 'w', encoding='utf-8-sig', newline='')
        writer = csv.DictWriter(index_csvfile, fieldnames=csvheaders)
        writer.writeheader()
    else:
        index_csvfile = open(INDEX_FILE, 'a', encoding='utf-8-sig', newline='')
        writer = csv.DictWriter(index_csvfile, fieldnames=csvheaders)

    open_browser()
    time.sleep(2)
    # 最大化窗口
    browser.maximize_window()
    time.sleep(2)
    for detail_info in infolist:
        date = detail_info[1]
        if not check_date(date):
            continue
        else:
            date = date[0:10]
        movie_name = detail_info[0]
        if movie_name in searched_list:
            continue
        # 有些关键词中英混合，去掉后面的英文
        keyword = detail_info[2].split(' ')[0]
        row = {}
        row['movie_name'] = movie_name
        row['date'] = '{}(中国)'.format(date)
        # 这里开始进入百度指数
        # 要不这里就不要关闭了，新打开一个窗口
        # http://blog.csdn.net/DongGeGe214/article/details/52169761
        # 新开一个窗口，通过执行js来新开一个窗口
        js = 'window.open("http://index.baidu.com");'
        browser.execute_script(js)
        # 新窗口句柄切换，进入百度指数
        # 获得当前打开所有窗口的句柄handles
        # handles为一个数组
        handles = browser.window_handles
        # print(handles)
        # 切换到当前最新打开的窗口
        browser.switch_to.window(handles[-1])
        # 在新窗口里面输入网址百度指数
        # 清空输入框
        time.sleep(2)
        # class_name随时可能更改，需要查看网页代码获取，下同
        browser.find_element_by_class_name("search-input").clear()
        # 写入需要搜索的关键词
        browser.find_element_by_class_name("search-input").send_keys(keyword)
        # 点击搜索
        # <input type="submit" value="" id="searchWords" onclick="searchDemoWords()">
        browser.find_element_by_class_name("search-input-cancle").click()
        time.sleep(3)
        # 滑动思路：http://blog.sina.com.cn/s/blog_620987bf0102v2r8.html
        # 滑动思路：http://blog.csdn.net/zhouxuan623/article/details/39338511
        # 该控件为百度指数的图像模块
        if browser.find_elements_by_css_selector(".index-trend-chart"):
            xoyelement = browser.find_elements_by_css_selector(".index-trend-chart")[0]
            # 获得坐标长宽
            x1 = xoyelement.location['x']
            y1 = xoyelement.location['y']
            width1 = xoyelement.size['width']
            height1 = xoyelement.size['height']
            # print(x1, y1, width1, height1)
            # 选择日期,这个日期是有一定误差的
            x_offset = calculate_offset(date)
            time.sleep(1)
            ActionChains(browser).move_to_element_with_offset(xoyelement, x_offset, height1 + 20).perform()
            time.sleep(1)
            ActionChains(browser).click().perform()
            time.sleep(1)
            # 搜索词：selenium JavaScript模拟鼠标悬浮
            # x_0 y_0初始值为鼠标位置相对指数显示模的坐标，不要初始化为0，0，不然显示不出指数
            # 水平移动 y_0在移动过程中不需要变化
            x_0 = 6
            y_0 = 100
            days = 29
            flag = True
            try:
                for i in range(1, days + 1):
                    # 最后一次需要在坐标轴里，所以需要在x=30的左边，需要减去一个大于6的数
                    if i == 29:
                        x_0 = x_0 - 8
                    # 每次鼠标悬空右移一段距离，使其能显示出百度指数的小黑框
                    ActionChains(browser).move_to_element_with_offset(xoyelement, x_0, y_0).perform()
                    # 需要停顿一段时间实现数据的加载,第一个数据多停留一会儿
                    if i == 1:
                        time.sleep(2.0)
                    time.sleep(1.0)
                    # 每次移动28分之1的距离 指数框大小1256/28 = 44.86
                    x_0 = x_0 + 44.86
                    # 小黑框的绝对路径 /html/body/div[1]/div[2]/div[2]/div/div[2]/div[1]/div[3]/div[1]/div[1]/div/div[2]/div[2]/div[2]
                    # TODO: 了解Xpath语法，改为相对路径
                    imgelement = browser.find_element_by_xpath(
                        '/html/body/div[1]/div[2]/div[2]/div/div[2]/div[1]/div[3]/div[1]/div[1]/div/div[2]/div[2]/div[2]')

                    index = str(imgelement.text)
                    row[i] = index
            except Exception as err:
                print(err)
                print('该百度指数不存在')
                flag = False
            if flag:
                searched_list.append(row['movie_name'])
                writer.writerow(row)
        else:
            print('该百度指数不存在')
        browser.close()
        browser.switch_to.window(handles[0])
    index_csvfile.close()


# 参数为字符串'xxxx-xx-xx'
def calculate_offset(date):
    today = datetime.date.today()
    start_day = datetime.date(2011, 1, 1)
    total_diff = (today - start_day).days
    day2 = datetime.datetime.strptime(date, '%Y-%m-%d').date()
    diff = (today - day2).days
    # 起始日期修正,进度条精度问题有误差，暂时加20
    # 1256是日期调整的进度条长度
    diff += 20
    offset = 1256 - (diff / total_diff) * 1256
    return offset


# 获得已经查询过的电影名/关键词,防止重复数据
def get_searched_list():
    searched_list = []
    if os.path.exists(INDEX_FILE):
        f = open(INDEX_FILE, 'r', encoding='utf-8-sig')
        reader = csv.DictReader(f)
        for row in reader:
            searched_list.append(row['movie_name'])
    return searched_list


def get_info_list():
    info_list = []
    f = open(MOVIE_INFO_FILE, 'r', encoding='utf-8-sig')
    reader = csv.DictReader(f)
    for row in reader:
        movie_detail = []
        movie_detail.append(row['电影名称'])
        movie_detail.append(row['上映日期'])
        movie_detail.append(row['电影名称'])
        info_list.append(movie_detail)
    return info_list


def check_date(date):
    if (not date[0].isdigit()) or len(date) < 10:
        return False
    year = date[0:4]
    month = date[5:7]
    day = date[8:10]
    if (not year.isdigit()) or (not month.isdigit()) or (not day.isdigit()):
        return False
    return int(year) >= 2013


def main():
    searched_list = get_searched_list()
    info_list = get_info_list()
    info_list = info_list[0:5]
    get_index(info_list, searched_list)


if __name__ == '__main__':
    main()
