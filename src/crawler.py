from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException, WebDriverException, ElementClickInterceptedException
from webdriver_manager.chrome import ChromeDriverManager
from time import sleep
import logging

import sys, os
sys.path.append(os.path.dirname(os.path.abspath(os.path.dirname(__file__))))
from src import jsonparser as jp


logging.basicConfig(filename='../info.log', filemode='w', level=logging.INFO, format='%(asctime)s - %(levelname)s [%(filename)s]: %(name)s %(funcName)20s - Message: %(message)s')
options = webdriver.ChromeOptions()
options.add_argument('window-size=1100,900')
options.add_argument('--headless')


class Crawler():

    def __init__(self, cinemaplace, moviename, checkdate):
        self.alive_ = True
        date = checkdate.split('.')
        self.year_ = int(date[0])
        self.month_ = int(date[1])
        self.day_ = int(date[2])
        self.moviename_ = moviename
        self.cinemaplace_ = cinemaplace
        self.driver_ = webdriver.Chrome(executable_path=ChromeDriverManager().install(), options=options)


    def open(self):
        try:
            url = jp.getJsonValue("url")
            self.driver_.get(url)
            cinemaplaces = self.driver_.find_elements(By.XPATH, '//*[@id="contents"]/div[2]/div[5]/div/div/div[1]/button') # 돌비시네마 장소
            index = 0
            for cinemaplace in cinemaplaces:
                index += 1
                if cinemaplace.text == self.cinemaplace_:
                    break
            self.driver_.find_element(By.XPATH, f'//*[@id="contents"]/div[2]/div[5]/div/div/div[1]/button[{index}]').click() # 돌비시네마 장소 클릭
            self.driver_.find_element(By.XPATH, '//*[@id="contents"]/div[2]/div[5]/div/div/div[4]/div/div[2]/button').click() # 달력 클릭
            calendarhead = self.getDate(self.driver_.find_element(By.XPATH, '//*[@id="ui-datepicker-div"]/div[1]/div').text) # 달력 년, 월 추출
            calendarhead = self.searchYearAndMonth(calendarhead)
            logging.info(f"set to finding year and month {calendarhead}")
            dayi, dayj = self.searchIndexDay()
            logging.info(f"dayi: {dayi}, dayj: {dayj}")
            
            logging.info("click for verify available status")
            self.driver_.find_element(By.XPATH, f'//*[@id="ui-datepicker-div"]/table/tbody/tr[{dayi}]/td[{dayj}]/a').click() # 달력 일 클릭
            self.driver_.find_element(By.XPATH, '/html/body/section/div/button').click() # 안내문 없애기
            while self.alive_:
                self.driver_.find_element(By.XPATH, '//*[@id="contents"]/div[2]/div[5]/div/div/div[4]/div/div[2]/button').click() # 달력 클릭
                self.driver_.find_element(By.XPATH, f'//*[@id="ui-datepicker-div"]/table/tbody/tr[{dayi}]/td[{dayj}]/a').click() # 달력 일 클릭
                self.driver_.find_element(By.XPATH, '/html/body/section/div/button').click() # 안내문 없애기
                self.driver_.implicitly_wait(5)
                logging.info("checking...")
            
        except NoSuchElementException:
            logging.info("It can reserve date!")
            pass
            
        except ElementClickInterceptedException:
            logging.info("There is no click Elements")
            raise KeyError("There is no click Elements")
            return


    def close(self):
        self.alive_ = False
        
    
    def getDate(self, calendarhead):
        calendarhead = calendarhead.split(' ')
        calendarhead[0] = int(calendarhead[0].replace("년", ""))
        calendarhead[1] = int(calendarhead[1].replace("월", ""))
        return calendarhead
    
    
    def searchYearAndMonth(self, calendarhead):
        while self.year_ != calendarhead[0]:
            if self.year_ < calendarhead[0]:
                self.driver_.find_element(By.XPATH, '//*[@id="ui-datepicker-div"]/div[1]/a[1]').click()
                calendarhead = self.getDate(self.driver_.find_element(By.XPATH, '//*[@id="ui-datepicker-div"]/div[1]/div').text)
            elif self.year_ > calendarhead[0]:
                self.driver_.find_element(By.XPATH, '//*[@id="ui-datepicker-div"]/div[1]/a[2]').click()
                calendarhead = self.getDate(self.driver_.find_element(By.XPATH, '//*[@id="ui-datepicker-div"]/div[1]/div').text)
        while self.month_ != calendarhead[1]:
            if self.month_ < calendarhead[1]:
                self.driver_.find_element(By.XPATH, '//*[@id="ui-datepicker-div"]/div[1]/a[1]').click()
                calendarhead = self.getDate(self.driver_.find_element(By.XPATH, '//*[@id="ui-datepicker-div"]/div[1]/div').text)
            elif self.month_ > calendarhead[1]:
                self.driver_.find_element(By.XPATH, '//*[@id="ui-datepicker-div"]/div[1]/a[2]').click()
                calendarhead = self.getDate(self.driver_.find_element(By.XPATH, '//*[@id="ui-datepicker-div"]/div[1]/div').text)
        return calendarhead
    
    
    def searchIndexDay(self):
        flag = True
        trs = self.driver_.find_elements(By.XPATH, '/html/body/div[5]/table/tbody/tr')
        for tr in trs:
            tds = tr.find_elements(By.XPATH, './/td')
            for td in tds:
                day = int(td.text)
                if day == 1 and flag:
                    flag = False
                    continue
                if day == self.day_ and not flag:
                    return trs.index(tr) + 1, tds.index(td) + 1


if __name__ == "__main__":
    crawler = Crawler("남양주현대아울렛 스페이스원", "(4K HDR HFR) 아바타: 물의 길", "2022.12.30")
    crawler.open()
    