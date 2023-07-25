from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
import time
import pandas as pd


def scrape_flight_data(driver, collect_url, date):
    print(collect_url)
    flight_data = []

    driver.get(collect_url)
    time.sleep(7)

    current_height = driver.execute_script("return document.body.scrollHeight")

    while True:
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(1)
        new_height = driver.execute_script("return document.body.scrollHeight")
        if new_height == current_height:
            break
        current_height = new_height
    time.sleep(2)

    result_elements = driver.find_elements(by=By.CLASS_NAME, value="result")
    for result_element in result_elements:
        flight_dict = {
            "airline": result_element.find_element(
                by=By.CSS_SELECTOR, value="div.airline > b.name"
            ).text,
            "date": date[0:4] + "-" + date[4:6] + "-" + date[6:8],
            "departure_time": result_element.find_elements(
                by=By.CLASS_NAME, value="route_time__-2Z1T"
            )[0].text,
            "arrival_time": result_element.find_elements(
                by=By.CLASS_NAME, value="route_time__-2Z1T"
            )[1].text,
            "departure_place": result_element.find_elements(
                by=By.CLASS_NAME, value="route_code__3WUFO"
            )[0].text,
            "arrival_place": result_element.find_elements(
                by=By.CLASS_NAME, value="route_code__3WUFO"
            )[1].text,
            "flight_time": sum(
                int(t) * 60**i
                for i, t in enumerate(
                    result_element.find_element(
                        by=By.CLASS_NAME, value="route_info__1RhUH"
                    )
                    .text[:-1]
                    .split("시간 ")[::-1]
                )
            ),
            "seat": result_element.find_element(
                by=By.CLASS_NAME, value="domestic_type__30RSq"
            ).text,
            "price": int(
                result_element.find_element(
                    by=By.CLASS_NAME, value="domestic_num__2roTW"
                ).text.replace(",", "")
            ),
        }
        flight_data.append(flight_dict)

    return flight_data


url = "https://m-flight.naver.com/flights/domestic/"
driver = webdriver.Chrome("./chromedriver")

departures = ["PUS", "CJJ", "GMP"]
date_list = pd.date_range(start="2023-10-01", end="2023-10-31")
date_list = date_list.strftime("%Y%m%d").tolist()
crawled_data = []

for date in date_list:
    for departure in departures:
        collect_urls = [
            url + departure + "-CJU-" + date + "?adult=1&fareType=YC",
            url + "CJU-" + departure + "-" + date + "?adult=1&fareType=YC",
        ]
        for collect_url in collect_urls:
            flight_data = scrape_flight_data(driver, collect_url, date)
            crawled_data.extend(flight_data)

# list to csv
df = pd.DataFrame(crawled_data)
df.to_csv("flight_data_10.csv", index=False, encoding="utf-8-sig")

driver.close()