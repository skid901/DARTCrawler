from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException
from bs4 import BeautifulSoup
from urllib.request import urlopen
import re
from collections import OrderedDict
import json
import pandas as pd
from pandas.io.json import json_normalize

# index : 오류를 발생시키는 기업 데이터를 확인하기 위한 변수
def collect_report(rcp_info, index):
    # 에러 메세지 관련 변수 선언
    error_mesg = str(index)
    error_status = 0
    # 재무제표 재무 데이터를 저장하는 JSON(파이썬 딕셔너리) 변수 생성
    report_json = OrderedDict()
    # 재무제표 메타 데이터를 저장
    report_json['회사명'] = rcp_info[0]
    report_json['년도'] = int(rcp_info_list[4][:4]) - 1
    # 레포트 html문서로 부터, 필요한 세부 레포트 url을 저장할 딕셔너리 생성
    report_dict = {'재무상태표': None, '대차대조표': None, '손익계산서': None, '현금흐름표': None}
    # 보고서 접수번호
    rcpNo = rcp_info[3]  # '20120404001355'
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
        # 첫 페이지에서 필요한 보고서로 이동하는 <a href="#"> 태그 리스트 저장
        # *주의: geckodriver(파이어폭스 버전)을 사용하는 경우, <a> 태그 의 href 속성값을 ""로 설정
        anchorList = main_bsObj.find_all( 'a', {'href': '#'} )
        # checkpoint 1
        #print( 'checkpoint 1 >>', anchorList )
        # 필요한 <a> 태그 index, text 저장 리스트(타겟 리스트) 생성
        targetAList = []
        # 목적에 적합한 <a> 태그 탐색
        for anchor in anchorList:
            # a 태그의 text를 공백 제거 후 저장
            anchorText = anchor.get_text().replace(' ', '')
            # a 태그의 text가 재무제표 유형 리스트에 포함되면 해당 <a> 태그의 index 저장
            if anchorText in report_dict.keys():
                # checkpoint 2
                #print( 'checkpoint 2 >> %d번째 <a href="#">: %s' % (anchorList.index(anchor), anchorText) )
                # 적합한 <a> 태그 메타 데이터(보고서 유형)를 타겟 리스트에 저장
                targetAList.append([anchorList.index(anchor), anchorText])
        # 타겟 리스트를 순회하여, 각 보고서 url 저장
        for index, reportName in targetAList:
            # 보고서에서 각 항목 데이터에 접근하는 <a> 태그에서 필요한 항목이 저장된  index만 접근 
            driver.find_elements_by_xpath('//a[@href="#"]')[index].click()
            # 로딩 대기(2초)
            driver.implicitly_wait(2)
            # 각 보고서 화면으로 부터 재무 데이터 url을 포함한 <iframe> 태그에서 scr 속성값 획득
            target_url = BeautifulSoup(driver.page_source).find('iframe')['src']
            # 속성값에서 불필요한 부분 문자열 제거
            report_dict[reportName] = target_url.replace('amp;', '')
    finally:
        # 웹 드라이버 종료
        driver.close()
    # 세부 제무 보고서 BeautifulSoup 객체를 저장하는 변수 선언
    finance_position_bsObj = None  # 재무상태표(구 대차대조표)
    income_statement_bsObj = None  # 손익계산서
    cash_flow_bsObj = None  # 현금흐름표
    # 각 세부 보고서 url에서 재무 데이터 추출
    for reportName, reportURL in report_dict.items():
        # 세부 보고서 url을 수집하지 못했다면 데이터 추출 skip
        if reportURL == None:
            continue
        # checkpoint 3
        #print('checkpoint 3 >>', reportName, reportURL)
        # DART domain url
        domain = 'https://dart.fss.or.kr/'
        # 재무상태표(대차대조표)에서 재무 데이터 추출
        if reportName in ('재무상태표', '대차대조표'):
            reportHTML = urlopen(domain + reportURL)
            finance_position_bsObj = BeautifulSoup(reportHTML, 'html.parser')
        elif reportName == '손익계산서':
            reportHTML = urlopen(domain + reportURL)
            income_statement_bsObj = BeautifulSoup(reportHTML, 'html.parser')
        elif reportName == '현금흐름표':
            reportHTML = urlopen(domain + reportURL)
            cash_flow_bsObj = BeautifulSoup(reportHTML, 'html.parser')
    '''
    테스트 url 목록
    재무상태표: https://dart.fss.or.kr/report/viewer.do?rcpNo=20120404001355&dcmNo=3350848&eleId=4&offset=8479&length=35728&dtd=dart3.xsd
    손익계산서: https://dart.fss.or.kr/report/viewer.do?rcpNo=20120404001355&dcmNo=3350848&eleId=5&offset=44207&length=25851&dtd=dart3.xsd
    현금흐름표: https://dart.fss.or.kr/report/viewer.do?rcpNo=20120404001355&dcmNo=3350848&eleId=7&offset=77198&length=35071&dtd=dart3.xsd

    수집 대상 컬럼 명
    매출채권 : ifrs_TradeAndOtherCurrentReceivables
    재고자산 : ifrs_Inventories
    단기차입금 : dart_ShortTermBorrowings
    장기차입금 : dart_LongTermBorrowingsGross
    자산총계 : ifrs_Assets
    부채총계 : ifrs_Liabilities
    자본총계 : ifrs_Equity
    매출액 : ifrs_Revenue
    영업이익 : dart_OperatingIncomeLoss
    당기순이익 : ifrs_ProfitLoss
    매출원가 : ifrs_CostOfSales
    금융비용(손익) : ifrs_FinanceCosts
    영업활동현금흐름 : ifrs_CashFlowsFromUsedInOperatingActivities
    투자활동현금흐름 : ifrs_CashFlowsFromUsedInInvestingActivities
    재무활동현금흐름 : ifrs_CashFlowsFromUsedInFinancingActivities
    '''
    # 수집할 컬럼 명 리스트
    column_list_1 = ['매출채권', '재고자산', '자산총계', '자본총계', '부채총계']
    column_list_2 = ['매출액', '영업이익', '영업손실', '영업이익손실', '당기순이익', '당기순손실', '당기순이익순손실', '매출원가', '이자수익', '이자비용', '금융비용', '금융손실', '금융이익']
    column_list_3 = ['영업활동으로인한현금흐름', '투자활동으로인한현금흐름', '재무활동으로인한현금흐름']
    # 재무상태표(대차대조표) 재무 데이터를 저장하는 JSON(파이썬 딕셔너리) 변수 생성
    finance_position_json = OrderedDict()
    try:
        # checkpoint 4
        #print('checkpoint 4 >>', finance_position_bsObj)
        # 재무상태표(대차대조표)에서 재무 데이터가 포함된 <tr> 태그 리스트 추출
        finance_position_trObjList = finance_position_bsObj.find_all('tbody')[1].find_all('tr')
        # 차입금 누적 변수 선언
        loan = 0
        # 컬럼 명을 확인해서, 수집 대상이면 수집 리스트에 저장
        for trObj in finance_position_trObjList:
            # 컬럼 명 수집 및 전처리
            column = trObj.find('td').get_text()
            column = re.sub('[' + chr(32) + chr(160) + ']', '', column)  # 유령문자 제거
            column = re.sub('[\t\n\r\f\v-=.,#/?:$\{\}a-zA-Z0-9Ⅰ-Ↄㄱ-ㅣ]', '', column)
            column = column.replace('주', '')
            #print(1, column, column.find('차입금'))
            # 컬럼 명 필터링
            if column not in column_list_1 and column.find('차입금') < 0:
                continue
            # 컬럼 값 수집 및 전처리
            value = 0
            for td in trObj.find_all('td')[1:3]:
                td_text = td.get_text()
                column = re.sub('[' + chr(32) + chr(160) + ']', '', column)  # 유령문자 제거
                td_text = re.sub('[\t\n\r\f\v,]', '', td_text)  # 공백 및 쉼표(,) 제거
                if td_text in ['', '-']:
                    continue
                if td_text.find('(') > -1:
                    td_text = '-' + td_text.replace('(', '').replace(')', '')
                value = int(td_text)
            # checkpoint 4-1
            #print('checkpoint 4-1 >>', column, '|', value)
            # 차입금 누적
            if column.find('차입금') > 0:
                loan += value
                continue
            # 재무상태표(대차대조표) JSON에 데이터 저장
            finance_position_json[column] = value
        # checkpoint 4-1-1
        #print('checkpoint 4-1-1 >> 총차입금 |', loan)
        finance_position_json['총차입금'] = loan
        # checkpoint 4-2
        #jsonString_4_2 = json.dumps(finance_position_json, indent='\t')  # JSON 문자열 생성
        #print('checkpoint 4-2 >>', jsonString_4_2, json.loads(jsonString_4_2))  # JSON 문자열로 생성산 JSON 객체 출력
    except:
        error_mesg += ', 재무상태표'
        error_status = 1

    # 손익계산서 재무 데이터를 저장하는 JSON(파이썬 딕셔너리) 변수 생성
    income_statement_json = OrderedDict()
    try:
        # checkpoint 5
        #print('checkpoint 5 >>', income_statement_bsObj)
        # 손익계산서에서 재무 데이터가 포함된 <tr> 태그 리스트 추출
        income_statement_trObjList = income_statement_bsObj.find_all('tbody')[1].find_all('tr')
        # 컬럼 명을 확인해서, 수집 대상이면 수집 리스트에 저장
        for trObj in income_statement_trObjList:
            # 컬럼 명 수집 및 전처리
            column = trObj.find('td').get_text()
            column = re.sub('[' + chr(32) + chr(160) + ']', '', column)  # 유령문자 제거
            column = re.sub('[\t\n\r\f\v-=.,#/?:$\{\}a-zA-Z0-9Ⅰ-Ↄ]', '', column)
            column = re.sub('주', '', column)
            #print('2', column, column not in column_list_2)
            # 컬럼 명 필터링
            if column not in column_list_2:
                continue
            # 컬럼 값 수집 및 전처리
            value = 0
            for td in trObj.find_all('td')[1:3]:
                td_text = td.get_text()
                column = re.sub('[' + chr(32) + chr(160) + ']', '', column)  # 유령문자 제거
                td_text = re.sub('[\t\n\r\f\v,]', '', td_text)  # 공백 및 쉼표(,) 제거
                if td_text in ['', '-']:
                    continue
                if td_text.find('(') > -1:
                    td_text = '-' + td_text.replace('(', '').replace(')', '')
                value = int(td_text)
            # checkpoint 5-1
            #print('checkpoint 5-1 >>', column, '|', value)
            income_statement_json[column] = value
        # checkpoint 5-2
        #jsonString_5_2 = json.dumps(income_statement_json, indent='\t')  # JSON 문자열 생성
        #print('checkpoint 5-2 >>', jsonString_5_2, json.loads(jsonString_5_2))  # JSON 문자열로 생성산 JSON 객체 출력
    except:
        error_mesg += ', 손익계산서'
        error_status = 1

    # 현금흐름표 재무 데이터를 저장하는 JSON(파이썬 딕셔너리) 변수 생성
    cash_flow_json = OrderedDict()
    try:
        # checkpoint 6
        #print('checkpoint 6 >>', cash_flow_bsObj)
        # 현금흐름표에서 재무 데이터가 포함된 <tr> 태그 리스트 추출
        cash_flow_trObjList = cash_flow_bsObj.find_all('tbody')[1].find_all('tr')
        # 컬럼 명을 확인해서, 수집 대상이면 수집 리스트에 저장
        for trObj in cash_flow_trObjList:
            # 컬럼 명 수집 및 전처리
            column = trObj.find('td').get_text()
            column = re.sub('[' + chr(32) + chr(160) + ']', '', column)  # 유령문자 제거
            column = re.sub('[가-힣]\.', '', column)
            column = re.sub('[\t\n\r\f\v-=.,#/?:$\{\}a-zA-Z0-9Ⅰ-Ↄ]', '', column)
            column = re.sub('주석', '', column)
            #print(3, column)
            # 컬럼 명 필터링
            if column not in column_list_3:
                continue
            # 컬럼 값 수집 및 전처리
            value = 0
            for td in trObj.find_all('td')[1:3]:
                td_text = td.get_text()
                column = re.sub('[' + chr(32) + chr(160) + ']', '', column)  # 유령문자 제거
                td_text = re.sub('[\t\n\r\f\v,]', '', td_text)  # 공백 및 쉼표(,) 제거
                if td_text in ['', '-']:
                    continue
                if td_text.find('(') > -1:
                    td_text = '-' + td_text.replace('(', '').replace(')', '')
                value = int(td_text)
            # checkpoint 6-1
            #print('checkpoint 6-1 >>', column, '|', value)
            cash_flow_json[column] = value
        # checkpoint 6-2
        #jsonString_6_2 = json.dumps(cash_flow_json, indent='\t')  # JSON 문자열 생성
        #print('checkpoint 6-2 >>', jsonString_6_2, json.loads(jsonString_6_2))  # JSON 문자열로 생성산 JSON 객체 출력
    except:
        error_mesg += ', 현금흐름표'
        error_status = 1

    # checkpoint 7
    #jsonString_7 = json.dumps(report_json, indent='\t')  # JSON 문자열 생성
    #print('checkpoint 7 >>', jsonString_7, json.loads(jsonString_7))  # JSON 문자열로 생성산 JSON 객체 출력
    #test_json = json.loads(jsonString_7)
    #json_normalize(test_json['재무상태표(대차대조표)'])
    #json_normalize(test_json['손익계산서'])
    #print(json_normalize(test_json['현금흐름표']))
    # 모든 보고서 데이터가 저장된 JSON 객체 반환
    report_json['재무상태표'] = finance_position_json
    report_json['손익계산서'] = income_statement_json
    report_json['현금흐름표'] = cash_flow_json
    if error_status == 1:
        with open('fail_index.csv', 'a') as fail_index:
            fail_index.write(error_mesg + '\n')
    return report_json

if __name__=="__main__":
    count = 1
    with open("report_list.json", 'r') as report_list:
        count = len( report_list.readlines() )
    while count < 455:
        with open("rcpNo_list.csv", 'r') as rcpNo_list:
            for rcp_info in rcpNo_list.readlines()[ count : ]:
                rcp_info_list = rcp_info.split(",")
                report_json = OrderedDict()
                # 재무제표 메타 데이터를 저장
                report_json['회사명'] = rcp_info_list[0]
                report_json['년도'] = int(rcp_info_list[4][:4]) - 1
                #print(report_json)
                
                try:
                    report_json = collect_report(rcp_info_list, count + 1)
                    print('Success >> current count : %d' % (count + 1))
                except:
                    with open('fail_index.csv', 'a') as fail_index:
                        fail_index.write('%d, non_expected_error\n' % (count + 1))
                    print('Fail >> main exception executes at count : %d' % (count + 1))
                finally:
                    report_json_string = json.dumps(report_json)
                    with open('report_list.json', 'a') as report_list:
                        report_list.write(report_json_string + ',\n')
                    count += 1
        with open("report_list.json", 'r') as report_list:
            count = len( report_list.readlines() )
