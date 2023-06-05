import time 
from selenium import webdriver

from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager

def crawling(keyword, numImages, result_dir):
    #크롬 꺼짐 방지
    chrome_options = Options()
    chrome_options.add_experimental_option("detach",True)

    # 웹드라이버 실행
    service = Service(executable_path=ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service, options=chrome_options)

    # 이미지 검색 url
    url = 'https://pixabay.com/ko/photos/search/'

    # 이미지 검색하기
    driver.get(url + keyword)

    # 이미지 검색 영역의 xpath
    xpath = '//*[@id="app"]/div[1]/div/div[2]/div[3]/div'

# 100장 이하 이미지를 요구받은 경우
    if numImages <= 100:
        image_area = driver.find_element_by_xpath(xpath)
        image_elements = image_area.find_elements_by_tag_name("img")
        for i in range(numImages):
            image_elements[i].screenshot(result_dir + "/" + str(time.time()) + ".png")
    # 100장 이상을 요구받은 경우
    else:
        while numImages > 0:
            image_area = driver.find_element_by_xpath(xpath)
            image_elements = image_area.find_elements_by_tag_name("img")
            for i in range(len(image_elements)):
                image_elements[i].screenshot(result_dir + "/" + str(time.time()) + ".png")
                numImages -= 1
                if i == len(image_elements) - 1:
                    next_button = driver.find_element_by_partial_link_text("다음 페이지")
                    next_button.click()
                    time.sleep(3)