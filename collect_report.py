from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException
from bs4 import BeautifulSoup
import time

# 웹 드라이버 응답 로딩 대기 함수
def waitForLoad(driver, report_type):
    # 기존의 <iframe id="ifrm"> 태그를 저장
    element = driver.find_element_by_id('ifrm')
    count = 0 
    while True:
        count += 1
        # 10초 지연 시, 오류 메세지 출력 후 반환
        if count > 20:
            print('Error >> Time out during requsting report: %s' % report_type)
            return
        time.sleep(.5)
        try:
            # 버튼 클릭 시 변환되는 <iframe id="ifrm"> 태그가 변환됬는지 확인
            element == driver.find_element_by_id('ifrm')
        except NoSuchElementException:
            return

# 재무제표에서 수집한 레포트 html문서를 저장할 딕셔너리 생성
report_dict = {'재무상태표': None, '대차대조표': None, '손익계산서': None, '현금흐름표': None}
# 보고서 접수번호
rcpNo = '20120404001355'
# 보고서 url
report_url = 'http://dart.fss.or.kr/dsaf001/main.do?rcpNo=' + rcpNo
'''
# geckodriver(파이어폭스 버전) 설치경로를 할당하여, 웹드라이버 실행
executable_path = "C:\itStudy\Web\geckodriver-v0.21.0-win64\geckodriver.exe"
driver = webdriver.Firefox(executable_path = executable_path)
'''
# PhantomJS 설치경로를 할당하여, 웹 드라이버 실행
executable_path = "C:\itStudy\Web\phantomjs-2.1.1-windows\\bin\phantomjs.exe"
driver = webdriver.PhantomJS(executable_path)
# 웹 드라이버를 통해, 보고서 url로 html 요청
driver.get(report_url)
try:
    # 서버 응답 대기(타임아웃 10초)
    element = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located( (By.ID, 'ifrm') )
    )
    # 웹 드라이버의 현재 페이지 html 문서로 BeatifulSoup 객체 생성
    main_bsObj = BeautifulSoup(driver.page_source)
    # 첫 페이지에서 필요한 보고서로 이동하는 <a href="#"> 태그 수집
    anchorList = main_bsObj.find_all( 'a', {'href': '#'} )
    # 필요한 a 태그 index, text 저장 리스트(타겟 리스트) 생성
    targetAList = []
    # 목적에 적합한 a 태그 탐색
    for anchor in anchorList:
        # a 태그의 text 저장
        anchorText = anchor.get_text().replace(' ', '')
        # a 태그의 text가 재무제표 유형 리스트에 포함되면 해당 a 태그의 index 저장
        if anchorText in report_dict.keys():
            # checkpoint 1
            print( 'checkpoint 1 >> %d번째 a: %s' % (anchorList.index(anchor), anchorText) )
            # 적합한 a 태그 메타 데이터를 타겟 리스트에 저장
            targetAList.append([anchorList.index(anchor), anchorText])
    # 타겟 리스트를 순회하여, 각 보고서의 BeautifulSoup 객체 생성 및 저장
    for index, reportName in targetAList:
        driver.find_elements_by_xpath('//a[@href="#"]')[index].click()
        #waitForLoad(driver, reportName)
        driver.implicitly_wait(2)
        report_dict[reportName] = BeautifulSoup(driver.page_source)
finally:
    # 웹 드라이버 종료
    driver.close()
# 
for reportName, bsObj in report_dict.items():
    if bsObj == None:
        continue
    print(reportName, bsObj.find('iframe').find('a'))
