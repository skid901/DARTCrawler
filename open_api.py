from urllib.request import urlopen
import pandas as pd
from bs4 import BeautifulSoup
import webbrowser

'''
# 인증키
auth_key = "4b8d4bcfe25fe4edafafad828787e5139fe6943b"
# 기업 고유 번호
CrpNo = ""
# 요청 url
request_url = "http://dart.fss.or.kr/api/search.xml?auth=" + auth_key + \
            "&crp_cd=" + CrpNo + \
            "&start_dt=" + "19990101" + \
            "&bsn_tp=" + "A001&bsn_tp=A002&bsn_tp=A003"

resultXML = urlopen(request_url)
result = resultXML.read()
print(result)
'''

