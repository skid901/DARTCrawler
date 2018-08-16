from selenium import webdriver

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
# dart 기업개황 url
dart_opening_url = "https://dart.fss.or.kr/dsae001/main.do"
browser.get(dart_opening_url)

# 검색 기업 명 및 사업자등록번호 획득
'''
부도기업 명단으로부터 
기업 명 및 사업자 번호 
획득하는 코드 작성
'''
target_CrpNm = "삼성전자" # "신세계개발"
target_BusinessNo = "124-81-*****"
target_CrpNo = ""

# 검색창에 기업 명 입력
browser.find_element_by_id("textCrpNm").send_keys(target_CrpNm)
# 검색 클릭
browser.find_elements_by_xpath("//input[@class='ibtn']")[1].click()

##### 페이지 이동 #####

# 암묵적으로 웹 자원 로드를 위해 3초까지 대기
browser.implicitly_wait(3)
# 검색 결과에서 기업 명단 수집
searched_company_list = browser.find_elements_by_class_name("nobr")
# 기업 명단 순회
for company in searched_company_list:
    company_name = company.find_element_by_tag_name("a")
    # 해당 기업 명 수집
    CrpNm = company_name.text
    print("1 >>", CrpNm)
    # 기업 명이 검색어와 일치하지 않을 경우 skip
    if CrpNm != target_CrpNm:
        continue
    # 해당 기업 고유 번호 수집
    CrpNo = company_name.get_property("href")[-8:]
    print("2 >>", CrpNo)
    # 기업 명 클릭
    company_name.click()
    # 기업 개황 정보로부터 사업자등록번호 탐색 및 비교
    opening_info_list = browser.find_elements_by_xpath('//div[id="ext-comp-1006"]/tbody/tr')
    print("3 >>", opening_info_list, len(opening_info_list))
    BusinessNo = ""
    # 사업자등록번호 탐색
    for opening_info in opening_info_list:
        info_name = opening_info.find_element_by_tag_name("th").text
        if info_name == "사업자등록번호": 
            BusinessNo = opening_info.find_element_by_tag_name("td").text
            break
    # 사업자등록번호 비교
    print("4 >>", BusinessNo)
    if BusinessNo[0:6] != target_BusinessNo[0:6]:
        continue
    # 사업자등록번호가 일치할 경우 기업고유번호 저장
    target_CrpNo = CrpNo

# 기업고유번호 확인
print("4 >>", target_CrpNo)

# 브라우저 종료
browser.quit()