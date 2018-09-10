from selenium import webdriver

# 셀레니움을 사용하여, 기업 고유 번호를 탐색하는 함수
def search_crpNo(target_BusinessNo, target_CrpNm):
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

    # 부도 기업 명단으로부터, 검색할 기업 명 및 사업자등록번호 획득
    # -> 직접 입력하는 대신, 함수 파라미터로 전달
    #target_BusinessNo = "218-81-*****"
    #target_CrpNm = "삼성전자"
    target_BusinessNo_NonFiltering = ""
    target_CrpNo = ""

    # 검색창에 기업 명 입력
    browser.find_element_by_id("textCrpNm").send_keys(target_CrpNm)
    # 검색 클릭
    browser.find_elements_by_xpath("//input[@class='ibtn']")[1].click()

    ##### 페이지 이동 #####

    # 암묵적으로 웹 자원 로드를 위해 2초까지 대기
    browser.implicitly_wait(2)
    # 검색 결과에서 기업 명단 수집
    searched_company_list = browser.find_elements_by_class_name("nobr")
    # 기업 명단 순회
    for company in searched_company_list:
        company_name = company.find_element_by_tag_name("a")
        # 해당 기업 명 수집
        CrpNm = company_name.text
        # 테스트 1
        # print("1 >>", CrpNm)
        # 기업 명이 검색어와 일치하지 않을 경우 skip
        if CrpNm != target_CrpNm:
            continue
        # 해당 기업 고유 번호 수집
        CrpNo = company_name.get_property("href")[-8:]
        # 테스트 2
        #print("2 >>", CrpNo)
        # 기업 명 클릭
        company_name.click()
        # 암묵적으로 웹 자원 로드를 위해 2초까지 대기
        browser.implicitly_wait(2)
        # 기업 개황 정보로부터 사업자등록번호 탐색 및 비교
        opening_info_list = browser.find_elements_by_xpath("//div[@id='ext-comp-1006']//tbody//tr")
        # 테스트 3
        #print("3 >>", opening_info_list, len(opening_info_list))
        BusinessNo = ""
        # 사업자등록번호 탐색
        BusinessNo = opening_info_list[7].find_element_by_tag_name("td").text
        # 테스트 4
        #print("4 >>", BusinessNo)
        # 사업자등록번호 비교
        if BusinessNo[0:6] != target_BusinessNo[0:6]:
            continue
        # 사업자등록번호가 일치할 경우 사업자등록번호(필터링X) 저장
        target_BusinessNo_NonFiltering = BusinessNo
        # 사업자등록번호가 일치할 경우 기업고유번호 저장
        target_CrpNo = CrpNo
        print('target_CrpNo', target_CrpNo)

    # 브라우저 종료
    browser.quit()
    # 기업고유번호 확인(테스트 5)
    #print("5 >>", target_CrpNo)
    # 기업 명, 사업자등록번호, 사업자등록번호(필터링X), 기업고유번호 반환
    return [target_CrpNm, target_BusinessNo, target_BusinessNo_NonFiltering, target_CrpNo]

# search_CrpNo 함수를 수행하여, 기업 고유 번호를 수집하는 함수
def collect_crpNo():
    # 부도 기업 리스트 파일 열기
    with open("bankrupt_company_list.csv", 'r') as bankrupt_company_list:
        # 리스트에서 한 줄씩 호출
        bankrupt_companies = bankrupt_company_list.readlines()
        # 부도 기업 리스트 파일의 시작 레코드 인덱스 설정 변수 선언
        start_index = 0
        # 부도 기업 리스트 파일의 마지막 레코드 인덱스 설정 변수 선언
        end_index = len( bankrupt_companies )
        # 이전 작업을 확인하기 위해, 기업 고유 번호 리스트 파일 열기
        with open("crpNo_list.csv", 'a') as crpNo_list:
            # 이전 작업 산출물이 있다면, 마지막 작업 레코드의 인덱스를 시작 레코드 인덱스로 설정
            try:
                start_index = len( crpNo_list.readlines() )
            # 이전 작업 산출물이 없다면, 컬럼 명 추가 및 시작 레코드 인덱스를 1로 설정
            except:
                crpNo_list.write("법인명,사업자번호,사업자번호(필터링X),기업고유번호\n")
                start_index = 1
        # 시작 레코드 인덱스와 마지막 레코드 인덱스가 같다면 함수 종료
        if start_index == end_index:
            return
        # 설정한 레코드로부터 고유 기업 번호 탐색 시작
        for bankrupt_company in bankrupt_companies[ start_index : ]:
            # 호출된 정보를 배열로 저장
            bankrupt_company_info = bankrupt_company.split(",")
            # 테스트 bankrupt_company_info
            print("bankrupt_company_info >>", bankrupt_company_info)
            # 사업자 번호 추출
            target_BusinessNo = bankrupt_company_info[0]
            # 기업 명 추출
            target_CrpNm = bankrupt_company_info[1]
            # 테스트 target_BusinessNo, target_CrpNm
            print("target_BusinessNo | target_CrpNm >>", target_BusinessNo, "|", target_CrpNm)
            # search_CrpNo 함수 호출
            crpNo_info = search_crpNo(target_BusinessNo, target_CrpNm)
            # 테스트 CrpNo_info
            print("crpNo_info >>", crpNo_info)
            # 기업 고유 번호 리스트 파일 열기
            with open("crpNo_list.csv", 'a') as crpNo_list:
                # 리스트 파일에 기업 고유 번호 정보 입력(csv)
                crpNo_list.write(",".join(crpNo_info) + "\n")

# collect_CrpNo 함수를 작업이 완료될 때 까지 반복적으로 호출하는 코드
if __name__ == "__main__":
    # 수집된 기업 고유 번호 수를 확인하는 변수 선언
    count = 0
    # 부도 기업 리스트의 모든 기업에 대해, 고유 번호를 수집할 때 까지 고유 번호 수집 함수 반복 호출 
    while(count < 780):
        try:
            # 기업 고유 번호 수집 함수 호출
            collect_crpNo()
        except:
            # 예회 발생 시, 이를 무시
            None
        finally:
            # 기업 고유 번호 리스트 파일 열기
            with open("crpNo_list.csv", 'r') as crpNo_list:
                # 수집 정보 레코드 수 확인
                count = len( crpNo_list.readlines() )
    # 기업 고유 번호를 획득한 레코드 수 확인
    collected_count = 0
    with open("crpNo_list.csv", 'r+') as crpNo_list:
        for crpNo in crpNo_list.readlines():
            if len(crpNo.split(",")[3]) > 2:
                collected_count += 1
    print("collected_count >>", collected_count)
