# 有道云笔记自动登陆签到看广告获取空间，配合腾讯云函数python3.6
import requests
import calendar
import json
import time

# server酱开关，填0不开启(默认)，填1只开启cookie失效通知，填2同时开启cookie失效通知和签到成功通知
sever = '2'
# 填写server酱sckey,不开启server酱则不用填
sckey = 'SCU112354T5fc7fb20f5abb1b93de6692f52a0ced05f53c0e7729ab'



CookieS = [
    {
        'phone':'7761',
        'cookie':'Hm_lvt_daa6306fe91b10d0ed6b39c4b0a407cd=1626325667; OUTFOX_SEARCH_USER_ID_NCOO=598527512.3876541; OUTFOX_SEARCH_USER_ID="-874777582@10.108.160.17"; _ga=GA1.2.1833834981.1626325668; NTES_YD_SESS=prFDlq2TsMUIcN2HFOmJVxb2NructWCOS26ZMQNwM8YeGTk4G2l_fIfQ5b3aYb4findQ85fGC.Wt1uzMz77X3qzN9ITjGjuMzUGvYIi7_6coYoPWbNHmLEu7_8_EsnoGubBQbhjf5ePRFewTkaNkhBtmxCBWUv9e1LlZwqIyZDiIk68RLf0.EipRZc4HT_HK69FhYJVBNXDPsK.3.ptv6aEKB.2G71225.ixesfC6jhc0; S_INFO=1653530147|0|0&60##|17553047761; P_INFO=17553047761|1653530147|1|youdaonote|00&99|null&null&null#shd&370100#10#0|&0||17553047761'
    },
    {
        'phone':'6707',
        'cookie':'Hm_lvt_daa6306fe91b10d0ed6b39c4b0a407cd=1626325667; OUTFOX_SEARCH_USER_ID_NCOO=598527512.3876541; OUTFOX_SEARCH_USER_ID="-874777582@10.108.160.17"; _ga=GA1.2.1833834981.1626325668; NTES_YD_SESS=prFDlq2TsMUIcN2HFOmJVxb2NructWCOS26ZMQNwM8YeGTk4G2l_fIfQ5b3aYb4findQ85fGC.Wt1uzMz77X3qzN9ITjGjuMzUGvYIi7_6coYoPWbNHmLEu7_8_EsnoGubBQbhjf5ePRFewTkaNkhBtmxCBWUv9e1LlZwqIyZDiIk68RLf0.EipRZc4HT_HK69FhYJVBNXDPsK.3.ptv6aEKB.2G71225.ixesfC6jhc0; S_INFO=1653530147|0|0&60##|17553047761; P_INFO=17553047761|1653530147|1|youdaonote|00&99|null&null&null#shd&370100#10#0|&0||17553047761'
    },
    {
        'phone':'9920',
        'cookie':'Hm_lvt_daa6306fe91b10d0ed6b39c4b0a407cd=1626325667; OUTFOX_SEARCH_USER_ID_NCOO=598527512.3876541; OUTFOX_SEARCH_USER_ID="-874777582@10.108.160.17"; _ga=GA1.2.1833834981.1626325668; NTES_YD_SESS=ufWuOPEsG7VUs3FSNsyD781iZFlBc55TyL47G_bRG90QZ2qhZLps8NQd6OD85bbpFUrYKtGGtFSiQWl7Zt9tlcfSgT9opd1HEqayzPD42O4Poh8M3FuCvitts9s.cD6Z1rK_rE38lQwmdQR2qYbqEKUTJgK5AWzQBnRMUn9t5YqZyniCa_pkTzrUCdcCEXZsy_J4_CuCzdsGF5vBbtiDyBv3QKyB_0Us.DAxwsjbhtkti; S_INFO=1653725948|0|0&60##|15666969920; P_INFO=15666969920|1653725948|1|youdaonote|00&99|null&null&null#shd&370100#10#0|&0||15666969920'
    },
]



def getcookie(ck):

    try:
        # 获取ck，这个ck是登录的，手机验证码登录之后的第一个或者第二个请求，这个请求就是请求ck的，这个请求的有效期是一个月

        # url ：https://note.youdao.com/login/acc/login?   这个包的cookie
        # NTES_YD_SESS后面的要删除

        # 有道云官网下载旧版本 抓http://note.youdao.com/login/acc/cellphone
        # 抓GET http://notify3.note.youdao.com/pushserver3/client
        # 删除最后的JSESSIONID
        # cookie全复制

        headers2 = {
            'Cookie': ck
        }
        fh1 = requests.request("POST",
                               "https://note.youdao.com/login/acc/login?product=YNOTE&app=client&ClientVer=61000000002&GUID=PC9605cff43b21f8535&client_ver=61000000002&device_id=PC9605cff43b21f8535&device_name=DESKTOP-4A3VFD7&device_type=PC&keyfrom=pc&os=Windows&os_ver=Windows%2010&vendor=website&vendornew=website&tp=cellphone&cf=7",
                               headers=headers2)
        ck = fh1.cookies
        # 拼接ck
        cookie = 'YNOTE_SESS=' + ck.get_dict()['YNOTE_SESS'] + '; domain=.note.youdao.com; path=/; HttpOnly,YNOTE_LOGIN=' + \
                 ck.get_dict()['YNOTE_LOGIN'] + '; domain=.note.youdao.com; path=/,JSESSIONID=' + ck.get_dict()[
                     'JSESSIONID'] + '; path=/;'
        return cookie
    except BaseException:
        # requests.get('https://sc.ftqq.com/' + sckey + '.send?text=有道云获取cookie失败')
        # settext("有道云cookie失效")
        print('失败')


def start():

    for ck in CookieS:

        ad = 0
        payload = 'yaohuo:id34976'
        headers = {'Cookie': getcookie(ck['cookie'])}
        re = requests.request("POST", "https://note.youdao.com/yws/api/daupromotion?method=sync", headers=headers,
                              data=payload)
        if 'error' not in re.text:  # not in  右侧的内容里是否不包含左侧的内容。不包含返回真，包含返回假。
            res = requests.request("POST", "https://note.youdao.com/yws/mapi/user?method=checkin", headers=headers,
                                   data=payload)
            for i in range(3):
                resp = requests.request("POST", "https://note.youdao.com/yws/mapi/user?method=adRandomPrompt",
                                        headers=headers, data=payload)
                ad += resp.json()['space'] // 1048576
            # print(re.text, res.text, resp.text)
            if sever == '2':
                if 'reward' in re.text:
                    sync = re.json()['rewardSpace'] // 1048576  # 除
                    checkin = res.json()['space'] // 1048576    # 除
                    # requests.get(
                    #     'https://sc.ftqq.com/' + sckey + '.send?text=有道云笔记签到成功共获得空间' + str(sync + checkin + ad) + 'M')
                    s = str(ck['phone'])+'：有道云笔记签到成功共获得空间' + str(sync + checkin + ad) + 'M'
                    settext(str(ck['phone'])+"：有道云笔记签到成功："+ str(sync + checkin + ad) + 'M')
                    print(s)


                    # return s
        else:
            if sever != '0':
                # requests.get('https://sc.ftqq.com/' + sckey + '.send?text=有道云签到cookie失效')
                settext(ck['phone']+"：有道云cookie失效")
                print('有道云签到cookie失效')



def main_handler():
    global ts
    ts = 0
    global token
    global ID
    global secret
    global yyid

    ID = "wwb6ae6e6e7424f50c"  # 企业ID
    secret = "QQ4fECz6QofG90F2xHAegC02ddnJUKjDI__s7_Nmyjo"  # 应用的Secret
    yyid = 1000003  # 应用的AgentId，发送消息时使用

    return start()


# 获取token
def gettoken():
    global ts
    global token
    global ID
    global secret

    # tokens是否第一次获取或者是超时
    if ts == 0 or (calendar.timegm(time.gmtime()) - ts) > 7200:
        try:
            print("----获取微信APItoken----")
            fh = requests.get(
                "https://qyapi.weixin.qq.com/cgi-bin/gettoken?corpid=" + ID + "&corpsecret=" + secret).json()

            if fh["errcode"] == 0:
                ts = calendar.timegm(time.gmtime())
                token = fh["access_token"]
                return token
            else:
                ts = 0
                print("token获取失败")
                return 0
        except Exception as c:
            print("----出现异常----")
            print(c)
            return 0
    else:
        print("----token未过期----")
        return token
    # print("耗时：" + str(calendar.timegm(time.gmtime()) - ts) + "秒")

# 发送文本消息
def settext(text):
    global yyid
    try:

        data = {
            "touser": "@all",
            "msgtype": "text",
            "agentid": yyid,
            "text": {
                "content": text
            }
        }

        fh = requests.post("https://qyapi.weixin.qq.com/cgi-bin/message/send?access_token=" + gettoken(),
                           data=json.dumps(data)).json()
        if fh["errcode"] == 0:
            print("----发送文字消息成功----")
        else:
            print("----发送文字消息失败！！！----")
    except Exception as e:
        print("----发送文字消息出现异常----")
        print(e)



if __name__ == '__main__':
    main_handler()
