# -*- coding: utf-8 -*-
from urllib.request import urlopen

# 보고서 첫페이지 url
init_url = "http://dart.fss.or.kr/dsaf001/main.do?rcpNo=20031229000062"
init_html = urlopen(init_url).read().decode('utf-8')
print(init_html)
html_file = open("init_html.txt", 'w')
html_file.write(init_html)
html_file.close()

# 첫 페이지로부터 재무제표 url 획득 후,

# domain
domain = "http://dart.fss.or.kr"
# 재무제표 url 반환 함수 결과값
src="/report/viewer.do?rcpNo=20180402005019&dcmNo=6060273&eleId=11&offset=620482&length=1474238&dtd=dart3.xsd"

target_html = urlopen(domain + src).read().decode('utf-8')
print(target_html)
html_file = open("report_html.txt", 'w')
html_file.write(target_html)
html_file.close()

'''
첫 페이지 html로부터 제무제표 url 반환 함수 및 반환함수를 호출하는 함수를 탐색
(탐색 키워드: 재무제표 -> viewDoc)

# 재무제표 url 반환 함수를 호출하는 javaScript code
treeNode1 = new Tree.TreeNode({
    text: "재 무 제 표",
    id: "133",
    cls: "text",
    listeners: {
        click: function() {viewDoc('20031229000062', '725619', '133', '13654', '111649', 'dart2.dtd');}
    }
});
cnt++;

# 첫 페이지에서 '재무제표' 항목을 클릭하면, 재무제표 url을 반환하는 함수
function viewDoc(rcpNo, dcmNo, eleId, offset, length, dtd) {
    currentDocValues.rcpNo = rcpNo;
    currentDocValues.dcmNo = dcmNo;
    currentDocValues.eleId = eleId;
    currentDocValues.offset = offset;
    currentDocValues.length = length;
    currentDocValues.dtd = dtd;
    var params = "";
    params += "?rcpNo=" + rcpNo;
    params += "&dcmNo=" + dcmNo;
    if (eleId != null)
        params += "&eleId=" + eleId;
    if (offset != null)
        params += "&offset=" + offset;
    if (length != null)
        params += "&length=" + length;
    params += "&dtd=" + dtd;
    document.getElementById("ifrm").src = "/report/viewer.do" + params;
}

# 재무제표 url 반환 함수 리턴값으로, domain + 리턴값을 하면 재무제표 url 완성
src="/report/viewer.do?rcpNo=20031229000062&dcmNo=725619&eleId=133&offset=13654&length=111649&dtd=dart2.dtd"
'''