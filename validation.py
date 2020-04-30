#!/usr/bin/python
# -*- coding: UTF-8 -*-
import json
import requests

class FitnessValidation(object):
    # 处理情况：
    # 1）参数不一致；
    # 2）缺少必要参数

    # 此处的api_baseUrl是前后端接口服务服务地址
    def __init__(self, standard=True, data='', api_baseUrl = 'http://172.16.103.71:5000'):
        self.data = data
        self.standard = standard
        self.api_baseUrl = api_baseUrl

    def get_parameters(self, component_name):
        url = self.api_baseUrl + '/api/v1/parameters/search?componentName=%s' % component_name
        reponse = requests.get(url)
        reponse_dict = json.loads(reponse.text)
        return reponse_dict['data']

    def validate(self, interface_name, parameter_dict):
        # 便于代码阅读，添加interface_name
        # 获取接口对应的请求参数、返回参数等信息
        parameters = parameter_dict[interface_name]
        method = parameters['httpVerb'].upper()
        # 此处的url为被测云平台的部署地址
        url = 'http://20.3.4.68:8080' + parameters['url']
        standard_response = parameters['response']
        query = parameters['query']
        print('query:', query)
        result = {'code': 200, 'message': '', 'data': ''}
        try:
            if method == 'GET':
                # query.pop('accessToken')
                if query:
                    url += '?'
                    for each in list(query.keys()):
                        url += each + '=' + query[each] + '&'
                    url = url[:-1]
                reponse = requests.get(url=url)
                reponse_dict = json.loads(reponse.text)
            elif method == 'POST':
                header = {"Content-Type": "application/json; charset=UTF-8"}
                reponse = requests.post(url=url, json=query, headers=header)
                reponse_dict = json.loads(reponse.text)
                print('1 url: ', url)
                print('2 query: ', query)
                print('3 reponse_dict: ', reponse_dict)
            else:
                print('Unknown method: ', method)
        except Exception as error:
            # 请求发生错误：1）视为不符合 2）记录error
            result['code'] = 201
            result['message'] = '无法得到正常响应'
            result['data'] = error

        else:
            if len(reponse_dict) < len(standard_response):
                result['code'] = 202
                result['message'] = '缺少参数'
                result['data'] = reponse_dict
            else:
                # 判断返回参数是否正确
                reponseKey = reponse_dict.keys()

                flag = True
                for each in standard_response:
                    if each in reponseKey:
                        pass
                    else:  # 参数名称不正确
                        flag = False
                        result['code'] = 203
                        result['message'] = '返回参数名称不符'
                        result['data'] = reponse_dict
                if flag:
                    result['message'] = '符合'
                    result['data'] = reponse_dict
        print('result', result)
        return result

