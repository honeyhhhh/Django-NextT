#_*_ coding:utf-8 _*_

from aliyunsdkcore.client import AcsClient
from aliyunsdkcore.request import CommonRequest

def send_sms(template, phone):
    client = AcsClient('LTAI4GBHPXxAh3F8AHvdXccf', 'gV8zWKjX3lnGVkPfKHp68FO2qdOKrj', 'cn-hangzhou')

    request = CommonRequest()
    request.set_accept_format('json')
    request.set_domain('dysmsapi.aliyuncs.com')
    request.set_method('POST')
    request.set_protocol_type('https') # https | http
    request.set_version('2017-05-25')
    #调用的接口的名称
    request.set_action_name('SendSms')

    request.add_query_param('RegionId', "cn-hangzhou")
    request.add_query_param('PhoneNumbers',phone)
    request.add_query_param('SignName', "xiyounet2020")  # 签名
    request.add_query_param('TemplateCode', "SMS_202815770")  # 模板编号
    request.add_query_param('TemplateParam', f"{template}")  # 发送验证码内容

    response = client.do_action(request)
    print(str(response, encoding = 'utf-8'))
    return response


if __name__ == '__main__':
    template = {
        'code': '556634',
    }
    send_sms(template, 18859581887)