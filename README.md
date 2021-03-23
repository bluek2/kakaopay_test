# kakaopay
# 서버사전과제1_결제시스템

### 1. 개발내용
결제요청을 받아 카드사와 통신하는 인터페이스를 제공하는 결제시스템

### 2. 개발환경
- OS: Windows 10
- DB: SQLite 
- Languages: Python 3.9.2
- Devlp Tool: Visual Studio Code
- Flask: 웹 어플리케이션 프레임워크
- requests: python http pacakage(모듈) 
- Json format 
- curl 7.75.0 for Windows
- github 

### 3. 테이블 설계
- TABLE_NAME: PAYMENT

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

### 5. 빌드 및 실행 방법:
빌드방법

실행방법:
``` 
#소스다운로드
$ git clone https://github.com/blueK2/kakaopay.git

#API 서버 실행
$ cd kakaopay
$ python src/kakao.py 
```


### 단위테스트 방법
참고사항
```
curl 사용시 윈도우와 Linux에서 json 데이터의 표현 방식이 다르다. 아래의 단위테스트는 윈도우에서 진행하였다.

윈도우
> curl -X POST http://localhost -d "{""key"": ""str"", ""key2"":number}"

Linux
$ curl -X POST http://localhost -d '{"key": "str", "key2":number}' 

* 윈도우 커맨드 창에서 UTF-8 코드를 보려면 다음을 실행한다.
c:\>chcp 65001
```

1. DB 초기화 [결제시스템 테이블 생성]
```
curl -X GET http://localhost:5000/api/setup 
```

2. 결제요청 테스트[정상] 
```
curl -X POST http://localhost:5000/api/payment -H "Content-Type: application/json" -d "{""card_no"":1234567890123456, ""exp_ym"":1125, ""card_cvc"":777, ""pay_prd"":0, ""pay_amt"":2000}"

```
3. 결제취소 테스트[정상]
``` 
curl -X POST http://localhost:5000/api/cancel -H "Content-Type: application/json" -d "{""mgnt_no"":""20210323061939358934"", ""pay_amt"":100000}"
```

4. 결제/취소 데이터 조회 테스트
```
curl -X POST http://localhost:5000/api/select -H "Content-Type: application/json" -d "{""mgnt_no"":""20210323061939358934""}"
```
5. 결제요청 입력 오류
```
curl -X POST http://localhost:5000/api/payment -H "Content-Type: application/json" -d "{""card_no"":""1234567890123456"", ""exp_ym"":1125, ""card_cvc"":777, ""pay_prd"":0, ""pay_amt"":100000}"

```

6. 결제취소 입력 오류
```
```

7. 데이터 조회 입력 오류
8. DB처리 오류 확인


### 6. 필수 구현 API 기능
#### 6-1. 결제 API
#### 6-2. 결제취소 API
#### 6-3. 결제정보 조회 API