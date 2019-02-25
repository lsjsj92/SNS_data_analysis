from selenium import webdriver
from bs4 import BeautifulSoup

from datetime import datetime
import time
import sys, csv

no = []
title = []

# 맨 처음 시작. 브라우저를 띄어서 메디를 입력하고 이동.
def main():
    driver = webdriver.Chrome("../driver/chromedriver.exe")
    driver.get("https://coinpan.com/free")

    driver.find_elements_by_class_name("search_keyword")[0].send_keys("메디")
    driver.find_element_by_css_selector("#board_input > button").click()
    go(driver)


# 2. 메인 로직. 한 페이지에서 글 읽어오고 다음페이지로 넘어가서 또 읽어오고.. 반복
def go(driver):

    if len(no) > 10 :
        check_list(driver, no, title)

    soup = BeautifulSoup(driver.page_source, "lxml")
    b = soup.find('div',{'id':'board_list'}).findAll('tr')
    cnt = 0
    #이 for문에 있는 값들을 배열에 전부 넣고 다음 페이지로 넘어가서 다시 이거를 긁고. -> 이걸 반복한다.
    for i in b:
        #이상한게 맨 처음껀 아무것도 없는 값이 있음. 그래서 맨 처음껀 제외시킨다.
        if cnt <= 0 :
            cnt += 1
            continue
        #제외시키고 그 다음ㄴ꺼부터 출력
        bb = i.findAll('td')

        #print(bb[0].find('span').text)  #얘는 No값. 공지, AD면 크롤링하지 말아야할 값
        #print(bb[1].find('a').attrs['href'])  # 얘는 title. 제목이라서 그 안에 내용이 있다.
        no.append(bb[0].find('span').text.strip())
        title.append(bb[1].find('a').attrs['href'])

# 3. 가져온 url로 no_check가 공지,AD면 무시하고 나머지 글에 대해서 이제 게시물을 긁어와야한다.
def check_list(driver, no_check, title_check):
    for cnt, idx in enumerate(no_check):
        try:
            driver.get(title_check[cnt])
            soup = BeautifulSoup(driver.page_source, "lxml")
            title = soup.find('div',{'class':'read_header'}).find('h1').find('a').text
            date = soup.find('div', {'class': 'section_wrap section_bottom_0'}).find('ul', {'class':'wt_box gray_color'}).findAll('li')[-1].find('span').text.split("/")[0].strip()
        except:
            continue


if __name__ == "__main__":
    main()