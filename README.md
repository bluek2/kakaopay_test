# kakaopay_test [서버사전과제1_결제시스템]

### 1. 개발내용
결제요청을 받아 카드사와 통신하는 인터페이스를 제공하는 결제시스템
- 주요기능 : 카드결제, 결제취소, 결제정보 조회

### 2. 개발환경
- Language : Python
- Client 
    - Windows 10 : OS
    - Chrome : Web Browser
- Open AIP 서버 환경 [vs REST API 서버 환경]
    - SQLite : DB
    - Flask : 웹개발프레임워크
    - requests : python http pacakage [vs 모듈]
- Dev. Tool
    - Visual Studio Code : 소스코드 작성, github 연동
    - github, git : 소스코드 관리 [vs 형상관리]
- Test Tool 
    - curl 7.75.0 for Windows : 개발 API 테스트 지원
    - Json format : 테스트데이터 입출력 데이터 포맷 
- Local PC 설치 프로그램명 및 버전
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
##### 4-1. 보험시스템 개발을 담당하면서 최근까지 그리고 가장 오래 주로 사용하던 개발언어는 Java 였으나 사전과제 제출용으로 Java를 위한 개발환경을 개인용 PC에 구축하기에는 번거로움이 있어, 근래들어 관심을 갖기 시작한 Python을 선택하여 과제를 수행하였습니다.   
##### 4-2. Python 이란 언어는 배우기 쉽고, 활용도가 높으며 최근 IT 트렌드를 말해주는 4차산업으로 분류되는 AI, 빅데이터, IoT, VR 등을 구현하는데 장점이 많아 각광 받는다고 하여 얼마전부터 관심을 갖고 조금씩 공부를 하던 중이었습니다. 능숙하지 않은 개발언어와 개발환경으로 과제를 제출하기에는 마감시간이 넉넉하지 않아, 아쉽지만 필수기능 API를 구현하는 것으로 과제를 마무리 짓는 방향을 선택했습니다. 마감시간까지 과제는 제출하고 Python을 계속 공부중이므로 선택문제로 주어진 부분취소 API 기능은 개인적으로 구현해볼 예정입니다.
##### 4-3. 테이블 설계 역시 실제 운영시스템인 경우 관리번호를 위한 채번테이블이나 카드사전송데이터를 관리하는 별도의 테이블을 만들었겠지만 과제를 위한 개발이라 1개의 테이블만으로 구성하였습니다.   

### 5. 실행 방법
``` 
#1. 소스 다운로드
$ git clone https://github.com/blueK2/kakaopay.git

#2. API 서버 실행
$ cd kakaopay
$ python src/kakao.py 

#3. API 실행
#아래 단위테스트 방법 참고
```
### 6. 단위테스트 방법
##### 참고사항
```
curl 사용시 윈도우와 Linux에서 json 데이터의 표현 방식이 다르다. 아래의 단위테스트는 윈도우에서 진행하였다.

윈도우
> curl -X POST http://localhost -d "{""key"": ""str"", ""key2"":number}"

Linux
$ curl -X POST http://localhost -d '{"key": "str", "key2":number}' 

* 윈도우 커맨드 창에서 UTF-8 코드를 보려면 다음을 실행한다.
c:\>chcp 65001
```
##### 6-1. DB 초기화 [결제 테이블 생성]
```
curl -X GET http://localhost:5000/api/setup 
```
##### 6-2. 결제요청 테스트[정상] 
```
curl -X POST http://localhost:5000/api/payment -H "Content-Type: application/json" -d "{""card_no"":1234567890123456, ""exp_ym"":1125, ""card_cvc"":777, ""pay_prd"":0, ""pay_amt"":2000}"
```
##### 6-3. 결제취소 테스트[정상]
``` 
curl -X POST http://localhost:5000/api/cancel -H "Content-Type: application/json" -d "{""mgnt_no"":""20210323061939358934"", ""pay_amt"":100000}"
```
##### 6-4. 결제/취소 데이터 조회 테스트
```
curl -X POST http://localhost:5000/api/select -H "Content-Type: application/json" -d "{""mgnt_no"":""20210323061939358934""}"
```
##### 6-5. 결제요청 입력 오류
```
curl -X POST http://localhost:5000/api/payment -H "Content-Type: application/json" -d "{""card_no"":""1234567890123456"", ""exp_ym"":1125, ""card_cvc"":777, ""pay_prd"":0, ""pay_amt"":100000}"
```
##### 6-6. 결제취소 입력 오류
```
```
##### 6-7. 데이터 조회 입력 오류
##### 6-8. DB처리 오류 확인

### 에러응답, 에러코드 정의
