import os
import math
import json

from flask import Flask, request, jsonify

import utils

#Flask 어플리케이션 생성
app = Flask(__name__)

#
# db 초기화
#
@app.route("/api/setup")
def setup():
    utils.db_setup()

    res = { "success" : "DB 테이블이 생성되었습니다." }
    #response
    return json.dumps(res, ensure_ascii=False)

#
# 결제 API 
#
@app.route("/api/payment", methods=['POST'])
def payment():
    #json
    json_data = request.get_json()

    card_no = None
    exp_ym = None
    card_cvc = None
    pay_prd = None
    pay_amt = None
    vat_amt = None

    try:
        card_no = json_data['card_no']
        exp_ym = json_data['exp_ym']
        card_cvc = json_data['card_cvc']
        pay_prd = json_data['pay_prd']
        pay_amt = json_data['pay_amt']
        vat_amt = json_data['vat_amt']
    except:
        pass

    orgnl_mgnt_no = ""
    #reserved
    reserv = " " * 47

    #check request args
    if card_no == None or type(card_no) != int or len(str(card_no)) < 10 or len(str(card_no)) > 16:
        res = { "error" : "카드번호가 잘못되었습니다." }
        #response
        return json.dumps(res, ensure_ascii=False)
    
    if exp_ym == None or type(exp_ym) != int:
        res = { "error" : "카드유효기간이 잘못되었습니다." }
        #response
        return json.dumps(res, ensure_ascii=False)
    
    if card_cvc == None or type(card_cvc) != int:
        res = { "error" : "카드cvc가 잘못되었습니다." }
        #response
        return json.dumps(res, ensure_ascii=False)

    if pay_prd == None or type(pay_prd) != int:
        res = { "error" : "할부개월이 잘못되었습니다." }
        #response
        return json.dumps(res, ensure_ascii=False)

    if pay_amt == None or type(pay_amt) != int or pay_amt < 100 or pay_amt > 1000000000:
        res = { "error" : "결제금액이 잘못되었습니다." }
        #response
        return json.dumps(res, ensure_ascii=False)

    if vat_amt == None or type(vat_amt) != int:
        vat_amt = math.floor(pay_amt/11+0.5)
     
    #get management-no
    mgnt_no = utils.db_getuid()

    #encrypt
    card_info = utils.encrypt(card_no, exp_ym, card_cvc)

    #make card request
    send_data = utils.make_card_request("PAYMENT", mgnt_no, card_no, pay_prd, exp_ym, card_cvc, pay_amt, vat_amt, orgnl_mgnt_no, card_info, reserv)

    #insert into db
    conn = utils.db_connect()

    cur = conn.cursor()

    sql = "insert into PAYMENT (MGNT_NO,CARD_NO,EXP_YM,CARD_CVC,CARD_INFO,PAY_PRD,PAY_AMT,VAT_AMT,CNCL_CD,SEND_DATA) values (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)"

    try:
        cur.execute(sql, (mgnt_no, card_no, exp_ym, card_cvc, card_info, pay_prd, pay_amt, vat_amt, 0, send_data))
    except:
        res = { "error" : "DB 오류가 발생했습니다." }
        #response
        return json.dumps(res, ensure_ascii=False)

    conn.commit()

    #response
    res = {}
    res['mgnt_no'] = mgnt_no
    res['send_data'] = send_data

    #return jsonify(res)
    return json.dumps(res, ensure_ascii=False)    

#
# 결제취소 API 
#
@app.route("/api/cancel", methods=['POST'])
def cancel():
    #json
    json_data = request.get_json()

    mgnt_no = None
    pay_amt = None
    vat_amt = None

    try:
        mgnt_no = json_data['mgnt_no']
        pay_amt = json_data['pay_amt']
        vat_amt = json_data['vat_amt']
    except:
        pass

    #check request args
    if mgnt_no == None or mgnt_no == "":
        res = { "error" : "관리번호가 잘못되었습니다." }
        #response
        return json.dumps(res, ensure_ascii=False)   
    
    if pay_amt == None or type(pay_amt) != int or pay_amt < 100 or pay_amt > 1000000000:
        res = { "error" : "취소금액이 잘못되었습니다." }
        #response
        return json.dumps(res, ensure_ascii=False)   

    #db query
    conn = utils.db_connect()

    cur = conn.cursor()

    #이미 취소된 건인지 확인
    sql = "select * from PAYMENT where ORGNL_MGNT_NO='{}'".format(mgnt_no)

    try:
        cur.execute(sql)
    except:
        res = { "error" : "DB 오류가 발생했습니다." }
        #response
        return json.dumps(res, ensure_ascii=False)

    rows = cur.fetchall()

    if len(rows) > 0:
        res = { "error" : "이미 결제취소 되었습니다." }
        #response
        return json.dumps(res, ensure_ascii=False)   

    #이전 거래 내역 조회
    sql = "select * from PAYMENT where MGNT_NO='{}'".format(mgnt_no)

    cur.execute(sql)

    rows = cur.fetchall()
    
    res = {}

    #error - not found
    if len(rows) == 0:
        res = { "error" : "결제정보 조회 결과가 없습니다." }
        #response
        return json.dumps(res, ensure_ascii=False)

    for row in rows:
        orgnl_mgnt_no = row[0]   
        card_no = row[1]
        exp_ym = row[2]
        card_cvc = row[3]
        pay_prd = row[5]
        org_pay_amt = row[6]
        org_vat_amt = row[7]         
        #reserved
        reserv = " " * 47

        #부가세 미입력        
        if vat_amt == None or vat_amt == "":
            vat_amt = org_vat_amt

        if int(pay_amt) > int(org_pay_amt):
            res = { "error" : "취소금액이 잘못되었습니다." }
            #response
            return json.dumps(res, ensure_ascii=False) 

        if int(vat_amt) > int(org_vat_amt):
            res = { "error" : "취소 부가세가 잘못되었습니다." }
            #response
            return json.dumps(res, ensure_ascii=False) 
        
        #get management-no
        mgnt_no = utils.db_getuid()

        #encrypt
        card_info = utils.encrypt(card_no, exp_ym, card_cvc)

        #make card request
        send_data = utils.make_card_request("CANCEL", mgnt_no, card_no, pay_prd, exp_ym, card_cvc, pay_amt, vat_amt, orgnl_mgnt_no, card_info, reserv)

        #거래취소 내역
        sql = "insert into PAYMENT (MGNT_NO,CARD_NO,EXP_YM,CARD_CVC,CARD_INFO,PAY_PRD,PAY_AMT,VAT_AMT,SEND_DATA,CNCL_CD,ORGNL_MGNT_NO) values (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)"

        try:
            cur.execute(sql, (mgnt_no, card_no, exp_ym, card_cvc, card_info, pay_prd, pay_amt, vat_amt, send_data, 1, orgnl_mgnt_no))
        except:
            res = { "error" : "DB 오류가 발생했습니다." }
            #response
            return json.dumps(res, ensure_ascii=False)

        conn.commit()

        #response
        res['mgnt_no'] = mgnt_no
        res['send_data'] = send_data

        break

    #response
    #return jsonify(res)    
    return json.dumps(res, ensure_ascii=False)    

#
#데이터조회 API
#
@app.route("/api/select", methods=['POST'])
def select():
    #json
    json_data = request.get_json()

    mgnt_no = None

    try:
        mgnt_no = json_data['mgnt_no']
    except:
        pass

    #check request args
    if mgnt_no == None or mgnt_no == "":
        res = { "error" : "관리 번호가 잘못되었습니다." }
        #response
        return json.dumps(res, ensure_ascii=False)

    #db query
    conn = utils.db_connect()

    cur = conn.cursor()

    sql = "select * from PAYMENT where MGNT_NO='{}'".format(mgnt_no)

    try:
        cur.execute(sql)
    except:
        res = { "error" : "DB 오류가 발생했습니다." }
        #response
        return json.dumps(res, ensure_ascii=False)

    rows = cur.fetchall()
    
    res = {}

    #error - not found
    if len(rows) == 0:
        res = { "error" : "검색결과가 없습니다." }
        #response
        return json.dumps(res, ensure_ascii=False)

    for row in rows:                
        res['mgnt_no'] = mgnt_no
        #card_info
        (card_no, exp_ym, card_cvc) = utils.decrypt(row[4])

        #카드번호 마스킹
        mask = "*" * (len(card_no) - 9)
        masked_card_no = card_no[0:6] + mask + card_no[-3:]

        #결제정보 데이터
        res['card'] = { 'card_no' : masked_card_no, 'exp_ym' : exp_ym, 'card_cvc' : card_cvc}
        res['cncl_cd'] = row[8]
        res['payment'] = { 'pay_amt' : row[6], 'vat_amt' : row[7]}
        break

    #response
    #return jsonify(res)
    return json.dumps(res, ensure_ascii=False)

#
# 서버실행
#
if __name__ == "__main__":
    app.run("0.0.0.0")

