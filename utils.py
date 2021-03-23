import os
import sqlite3
import datetime

DEFAULT_PATH = os.path.join(os.path.dirname(__file__), 'kakao.db')

#db 연결
def db_connect(db_path=DEFAULT_PATH):
    con = sqlite3.connect(db_path)
    return con

#테이블생성
def db_setup():
    conn = db_connect()

    cur = conn.cursor()

    customers_sql = """
    create table PAYMENT (
    MGNT_NO		    text(20) primary key,	--관리번호
    CARD_NO 	    integer(16) not null, 	--카드번호
    EXP_YM 	        integer(4), 		    --유효기간
    CARD_CVC 		integer(3), 		    --cvc
    CARD_INFO       text(300),              --암호화된 카드정보
    PAY_PRD	        integer(2) default '0', --할부개월수 installmentMonth
    PAY_AMT 	    integer(10),		    --결제금액
    VAT_AMT		    integer(10),		    --부가가치세
    CNCL_CD		    text(1), 		        --취소구분코드(0:결제, 1:결제취소)
    ORGNL_MGNT_NO	text(20),		        --원거래관리번호
    SEND_DATA       text(450)		        --카드사에 전달할 string 데이터
    )
    """

    cur.execute(customers_sql)

#Unique ID
def db_getuid():
    now = datetime.datetime.now()
    #
    #년,월,일,시,분,초,마이크로초 를 조합하여 20자리 uid 생성
    return now.strftime("%Y%m%d%H%M%S%f")

#암호화
def encrypt(card_no, exp_yn, card_cvc):
    #combine to one string
    plain_str  = "{}|".format(int(card_no))
    plain_str += "{}|".format(int(exp_yn))
    plain_str += "{}|".format(int(card_cvc))

    #make length 300
    plain_str = "{:300}".format(plain_str)

    #init
    cipher_str = ""

    #encrypting with XOR
    for c in plain_str:
        cipher_str += chr(ord(c) ^ 23)

    #encrypted str
    return cipher_str

#복호화
def decrypt(cipher_str):
    plain_str = ""
    #decrypting with XOR
    for c in cipher_str:
        plain_str += chr(ord(c) ^ 23)

    #split
    rets = plain_str.split("|")

    #extract info
    card_no = rets[0]
    exp_ym = rets[1]
    cvc = rets[2]

    return (card_no, exp_ym, cvc)

#
def make_card_request(func, mgnt_no, card_no, pay_prd, exp_ym, card_cvc, pay_amt, vat_amt, orgnl_mgnt_no, card_info, reserv):
    #common-header
    req_head  = "{:10}".format(func)
    req_head += "{:20}".format(mgnt_no)

    #data
    req_body  = "{:<20}".format(int(card_no))
    req_body += "{:02}".format(int(pay_prd))
    req_body += "{:4}".format(int(exp_ym))
    req_body += "{:<3}".format(int(card_cvc))
    req_body += "{:10}".format(int(pay_amt))
    req_body += "{:010}".format(int(vat_amt))
    req_body += "{:20}".format(orgnl_mgnt_no)
    req_body += "{:300}".format(card_info)
    req_body += "{:47}".format(reserv)

    send_data = "{:4}".format(len(req_head + req_body))

    send_data += req_head + req_body

    return send_data