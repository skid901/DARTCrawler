from urllib.request import urlopen
import json

# 기업 고유번호(인자 값)와 인증키를 포함한 URL로 보고서 접수번호를 검색하는 함수
# 동명의 기업을 구분하기 위해 사업자 등록번호 사용
def search_rcpNo(businsessNo, crpNo):
    # 요청 url 변수 설정
    auth_key = "4b8d4bcfe25fe4edafafad828787e5139fe6943b" # DART OPEN API 인증키
    crp_cd = crpNo  # crp_cd: 기업 고유번호
    start_dt = "20000101"  # start_dt: 검색시작 접수일자(YYYYMMDD)
    fin_rpt = "Y"  # 최종보고서만 검색여부(Y or N)
    bsn_tp = "F001"  # bsn_tp: 보고서 유형, 본 코드에서는 감사보고서 요청
    page_set = "100"  # 페이지당 건수(1~100)
    # 요청 url
    request_url = "http://dart.fss.or.kr/api/search.json" + \
                "?auth=" + auth_key + \
                "&crp_cd=" + crp_cd + \
                "&start_dt=" + start_dt + \
                "&fin_rpt=" + fin_rpt + \
                "&bsn_tp=" + bsn_tp + \
                "&page_set=" + page_set
    # 테스트 2
    print("2 >>", request_url)
    # 응답 결과(JSON 형식) 저장
    response = urlopen(request_url).read().decode('utf-8')
    # JSON 파싱 라이브러리를 사용하여, 보고서 메타 데이터 수집
    # 테스트 3
    print("3 >>", response)
    response_json = json.loads(response)
    for report_info in response_json.get("list"):
        '''
        JSON으로 부터 획득되는 보고서 메타데이터 형식
        JSON 객체지만, 파이썬에서는 dict 타입 데이터로 취급 가능
        {
            'crp_cls': '법인구분',
            'crp_nm': '법인 명', 
            'crp_cd': '고유번호', 
            'rpt_nm': '보고서 명', 
            'rcp_no': '접수번호', 
            'flr_nm': '공시 제출인명', 
            'rcp_dt': '공시 접수일자', 
            'rmk': '보고서 소관(관리 기관) 명시 정보'
        }
        '''
        # 테스트 4
        print("4 >>", report_info)
        # 보고서 접수번호 리스트 파일 열기
        with open("rcpNo_list.csv", 'a') as crpNo_list:
            # 보고서 접수번호 리스트 파일에 레코드 작성
            rcpNo_info = []
            rcpNo_info.append(report_info['crp_nm'])  # 법인 명
            rcpNo_info.append(businsessNo)  # 사업자 등록번호
            rcpNo_info.append(report_info['rpt_nm'])  # 보고서 명
            rcpNo_info.append(report_info['rcp_no'])  # 보고서 접수번호
            rcpNo_info.append(report_info['rcp_dt'])  # 공시 접수일자
            # 법인명,사업자번호,보고서명,접수번호,접수일자 작성
            crpNo_list.write(",".join(rcpNo_info) + "\n")

# 기업 고유번호(CrpNm)와 DART OPEN API를 사용하여 보고서 접수번호(RcpNm)를 수집하는 함수 
def collect_rcpNo():
    # crpNo_list.csv(부도기업 고유번호 리스트)의 데이터 호출
    with open("crpNo_list.csv", 'r') as crpNo_list:
        for crpNo_info in crpNo_list.readlines()[1:]:
            # 기업 고유번호가 수집된 record만 호출
            record = crpNo_info.split(",")
            if len(record[3]) <= 2:
                continue
            # 테스트 1
            print("1 >>", record[2], record[3].replace('\n',''))
            # crpNo_list에 기업 명, 사업자 등록번호, 기업 고유번호 저장
            search_rcpNo(record[2], record[3].replace('\n',''))

# collect_rcpNo 함수를 작업이 완료될 때 까지 반복적으로 호출하는 코드
if __name__=="__main__":
    collect_rcpNo()