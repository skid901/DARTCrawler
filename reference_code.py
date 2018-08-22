#최종 재무제표 url
url = "http://dart.fss.or.kr/report/viewer.do?rcpNo=20120404001355&dcmNo=3350848&eleId=3&offset=1293&length=1818&dtd=dart3.xsd"
url2 = "http://dart.fss.or.kr//report/viewer.do?rcpNo=20180430000927&dcmNo=6135394&eleId=3&offset=1511&length=2076&dtd=dart3.xsd"
# get_html함수를 통해 html을 얻음
html = requests.get(url2).text
# beautifulSoup을 이용하여 파싱객체 생성
soup = BeautifulSoup(html, 'html.parser')


                  
#dc_Revenue = soup.select("table")[3].select("td")[2].contents[0]
#dc_OperatingIncomeLoss = soup.select("table")[3].select("tr")[30].select("td")[2].contents[0]
#dc_ProfitLoss = soup.select("table")[3].select("tr")[46].select("td")[2].contents[0]#당기순이익
#dc_CashFlowsFromUsedInOperatingActivities = soup.select("table")[7].select("tr")[1].select("td")[2].contents[0] #영업활동현금흐름
#dc_CashFlowsFromUsedInInvestingActivities = soup.select("table")[7].select("tr")[34].select("td")[2].contents[0] #투자활동현금흐름
dc_CashFlowsFromUsedInFinancingActivities = "" #재무활동현금흐름
dc_TradeAndOtherCurrentReceivables = "" # 매출채권
dc_CostOfSales = "" # 매출원가
dc_Inventories = "" #재고자산
dc_Assets = "" #자산총계
dc_ShortTermBorrowings = "" #단기차입금
dc_LongTermBorrowingsGross = "" #장기차입금
dc_InterestExpenseFinanceExpense = "" #이자비용
dc_InterestIncomeFinanceIncom = "" #이자수익
dc_Liabilities = "" #부채총계
dc_Equity = "" #자본총계


default_company_result = pd.DataFrame();
temp=pd.DataFrame(([[dc_date, dc_Revenue,dc_OperatingIncomeLoss,dc_ProfitLoss,
                     dc_CashFlowsFromUsedInOperatingActivities, dc_CashFlowsFromUsedInInvestingActivities, dc_CashFlowsFromUsedInFinancingActivities,
                     dc_TradeAndOtherCurrentReceivables, dc_CostOfSales,
                     dc_Inventories, dc_Assets,
                     dc_ShortTermBorrowings, dc_LongTermBorrowingsGross,
                     dc_InterestExpenseFinanceExpense, dc_InterestIncomeFinanceIncom,
                     dc_Liabilities, dc_Equity]]),
         columns=["날짜","매출액","영업이익","당기순이익","영업활동현금흐름","투자활동현금흐름","재무활동현금흐름",
                  "매출채권","매출원가","재고자산","자산총계","단기차입금","장기차입금","이자비용","이자수익",
                 "부채총계","자본총계"])
print(temp)
#default_compnay_result = pd.concat([default_company_result,temp])