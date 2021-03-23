# kakaopay_test [서버사전과제1_결제시스템]

### 1. 개발내용
결제요청을 받아 카드사와 통신하는 인터페이스를 제공하는 결제시스템
- 주요기능 : 카드결제, 결제취소, 결제정보 조회

### 2. 개발환경
- Language : Python
- Client 
    - Windows 10 : OS
    - Chrome : Web Browser
- Open API 서버 환경
    - SQLite : DB
    - Flask : 웹개발프레임워크
- Dev. Tool
    - Visual Studio Code : 소스코드 작성, github 연동
    - github, git : 소스코드 관리 [vs 형상관리]
- Test Tool 
    - curl : 개발 API 테스트 지원
    - Json format : 테스트데이터 입출력 데이터 포맷 
- Local PC 설치 프로그램 및 버전
    - python-3.9.2-amd64.exe
    - ChromeSetup.exe
    - VSCodeUserSetup-x64-1.54.3.exe
    - Git-2.31.0-64-bit.exe
    - curl-7.75.0_4-win64-mingw.zip
   
### 3. 테이블 설계
TABLE NAME : PAYMENT
|COL_ID|DATA_TYPE|SIZE|KOR_NM|ADD_INFO|
|-|-|-|-|-|
|MGNT_NO|VARCHAR|20|관리번호|UNIQUE KEY|
|CARD_NO|NUMBER|16|카드번호|NOT NULL|
|EXP_YM|NUMBER|4|유효기간||
|CARD_CVC|NUMBER|3|CVC번호||
|CARD_INFO|VARCHAR|300|카드정보암호화||
|PAY_PRD|NUMBER|2|할부개월수||
|PAY_AMT|NUMBER|10|결제금액||
|VAT_AMT|NUMBER|10|부가세금액||
|CNCL_CD|VARCHAR|1|취소구분코드|0:결제,1:취소|
|ORGNL_MGNT_NO|VARCHAR|20|원거래관리번호||
|SEND_DATA|VARCHAR|450|카드사전송데이터||

### 4. 문제해결 전략:
##### 4-1. Python 을 개발언어로 선택한 이유  
보험시스템 개발을 담당하면서 최근까지 그리고 가장 오래 기간 사용하던 개발언어는 Java 였으나 사전과제 제출용으로 Java를 위한 개발환경을 개인용 PC에 구축하기에는 번거로움이 있어, 근래들어 관심을 갖기 시작한 Python을 선택하여 과제를 수행하였습니다.   

##### 4-2. 필수구현 API 개발 및 단위테스트   
또한, Python 이란 언어가 배우기 쉽고, 활용도가 높으며 IT 분야중 관심이 높아지고 있는 AI, 빅데이터, IoT, VR 등을 구현하는데 장점이 많아 각광 받는다고 하여, 얼마전부터 관심을 갖고 조금씩 공부를 하던 중이었습니다. 능숙하지 않은 개발언어와 개발환경으로 과제를 제출하기에는 마감시간이 넉넉하지 않아, 아쉽지만 필수구현 API 만을 구현하는 것으로 과제를 마무리 짓는 방향을 선택했습니다. 마감시간까지 과제는 제출하고 Python을 계속 공부중이므로 선택문제로 주어진 부분취소 API 기능은 개인적으로 구현해볼 예정입니다. Multi Thread 환경에 대한 부분 역시 Python을 더 학습하고 나면 쉬운 방법으로 구현이 가능하리라 예상됩니다. 

##### 4-3. 테이블설계 및 채번,암복호화 Utils 작성 기준 
테이블 설계 역시 실제 운영시스템인 경우 관리번호를 위한 채번테이블이나 카드사전송데이터를 관리하는 별도의 테이블을 만들었겠지만 과제를 위한 개발이라 1개의 테이블만으로 구성하였습니다. 기타 카드번호 암복호화나 관리번호 생성 등도 프로그램 내에서 간략하게만 구성하였습니다.     

### 5. 빌드 및 실행 방법

##### 5-1. 빌드방법

Python은 Java와 달리 별도의 컴파일이나 빌드과정 필요없이 실행되므로 github에 올려놓은 아래 3개 파일만 다운 받아서 api 서버를 실행시켜 개발한 api 기능테스트를 해볼수 있습니다.   

##### 5-2. 실행방법
``` 
#1. 소스 다운로드
c:\> git clone https://github.com/blueK2/kakaopay_test.git

[다운로드 결과파일: kakao.py, utils.py, README.md]

#2. API 서버 실행
c:\> cd kakaopay_test
c:\> python kakao.py 

#3. API 실행
#아래 단위테스트 방법 참고

* 윈도우 커맨드 창에서 UTF-8 코드를 보려면 다음을 실행합니다. 
c:\> chcp 65001
```
### 6. 단위테스트 방법
##### ※ 참고사항
```
curl 사용시 윈도우와 Linux에서 json 데이터의 표현 방식이 다릅니다. 

윈도우
c:\> curl -X POST http://localhost -d "{""key"": ""str"", ""key2"":number}"

Linux
$ curl -X POST http://localhost -d '{"key": "str", "key2":number}' 

※ 아래의 단위테스트는 윈도우에서 진행하였습니다.
```

##### 6-1. DB 초기화 [결제 테이블 생성]
```
c:\> curl -X GET http://localhost:5000/api/setup
```
##### 6-2. 결제 test [정상] 
```
c:\> curl -X POST http://localhost:5000/api/payment -H "Content-Type: application/json" -d "{""card_no"":1234567890123456, ""exp_ym"":1125, ""card_cvc"":777, ""pay_prd"":0, ""pay_amt"":110000, ""vat_amt"":10000}"
```
##### 6-3. 결제취소 test [정상]
``` 
c:\> curl -X POST http://localhost:5000/api/cancel -H "Content-Type: application/json" -d "{""mgnt_no"":""20210323133822314560"", ""pay_amt"":110000}"
```
##### 6-4. 결제정보 조회 test [정상]
```
c:\> curl -X POST http://localhost:5000/api/select -H "Content-Type: application/json" -d "{""mgnt_no"":""20210323133822314560""}"
```
##### 6-5. 결제 test [오류:결제금액]
```
c:\> curl -X POST http://localhost:5000/api/payment -H "Content-Type: application/json" -d "{""card_no"":1234567890123456, ""exp_ym"":1125, ""card_cvc"":777, ""pay_prd"":0, ""pay_amt"":10}"
```
##### 6-6. 결제취소 test [오류:결제취소금액]
``` 
c:\> curl -X POST http://localhost:5000/api/cancel -H "Content-Type: application/json" -d "{""mgnt_no"":"""", ""pay_amt"":10000}"
```
##### 6-7. 결제정보 조회 test [오류:관리번호]
```
c:\> curl -X POST http://localhost:5000/api/select -H "Content-Type: application/json" -d "{""mgnt_no"":""20210323061939358934""}"
```
##### 6-8. DB처리 오류 확인
```
DB 서버 종료후 결제/취소/조회 API 호출하여 에러메세지 확인
```
### 7. 에러응답  
```
- 카드번호가 잘못되었습니다.
- 카드유효기간이 잘못되었습니다.
- 카드cvc가 잘못되었습니다.
- 할부개월이 잘못되었습니다.
- 결제금액이 잘못되었습니다.
- 관리번호가 잘못되었습니다.
- 취소금액이 잘못되었습니다.
- 이미 결제취소 되었습니다.
- 결제정보 조회 결과가 없습니다.
- DB 오류가 발생했습니다.
```