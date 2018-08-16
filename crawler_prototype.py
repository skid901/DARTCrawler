from selenium import webdriver
from bs4 import BeautifulSoup as bs
import pandas as pd
import numpy as np

'''
# geckodriver(파이어폭스 버전) 설치경로 및 브라우저 실행
executable_path = "C:\itStudy\Web\geckodriver-v0.21.0-win64\geckodriver.exe"
browser = webdriver.Firefox(executable_path = executable_path)
'''
# PhantomJS 설치경로 및 브라우저 실행
executable_path = "C:\itStudy\Web\phantomjs-2.1.1-windows\\bin\phantomjs.exe"
browser = webdriver.PhantomJS(executable_path)

# 암묵적으로 웹 자원 로드를 위해 2초까지 대기
browser.implicitly_wait(2)
# dart url
dart_url = "https://dart.fss.or.kr/"
browser.get(dart_url)
# 검색 기업 명 입력
target_CrpNm = "미래씨앤씨"
browser.find_element_by_id("textCrpNm").send_keys(target_CrpNm)
# 전체(기간) 클릭
browser.find_element_by_id("date7").click()
# 정기공시, 외부감사관련 클릭
browser.find_element_by_id("publicTypeButton_01").click()
browser.find_element_by_id("publicTypeButton_06").click()
# 사업보고서, 감사보고서 클릭
browser.find_element_by_id("publicType1").click()
browser.find_element_by_id("publicType33").click()
# 검색 클릭
browser.find_element_by_xpath("//input[@class='ibtn']").click()

##### 페이지 이동 #####

# 암묵적으로 웹 자원 로드를 위해 2초까지 대기
browser.implicitly_wait(2)
# 검색 결과 테이블 추출
result_table = browser.find_elements_by_xpath("//table[@summary]/tbody/tr")
#사업보고서, 감사보고서 정보(url 포함) 수집
report_list = []
report_list.append(["CrpNm", "CrpNo", "rcpNm", "rcpNo", "submitting", "date"])
for table_row in result_table:
    data = table_row.find_elements_by_tag_name("td")
    CrpNm = data[1].text.strip()
    CrpNo = data[1].find_element_by_tag_name("a").get_property("href").split("=")[-1]
    rcpNm = data[2].text
    rcpNo = data[2].find_element_by_tag_name("a").get_property("id").lstrip("r_")
    submitting = data[3].text
    date = data[4].text
    report_list.append([CrpNm, CrpNo, rcpNm, rcpNo, submitting, date])
# 브라우저 종료
browser.quit()
# 수집 정보 csv 저장
with open("report_list.csv", 'w') as list_file:
    for report_info in report_list:
        record = ", ".join(report_info)
        list_file.write(record + "\n")
'''
##### 페이지 이동 #####
df = pd.read_csv("report_list.txt")
print(df)
'''
