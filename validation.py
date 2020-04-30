#!/usr/bin/python
# -*- coding: UTF-8 -*-
import json
import requests
import time
import logging

class FitnessValidation(object):
    # 处理情况：
    # 1）参数不一致；
    # 2）缺少必要参数
    LOG_FORMAT = "%(asctime)s %(name)s %(levelname)s %(pathname)s %(message)s "#配置输出日志格式
    DATE_FORMAT = '%Y-%m-%d  %H:%M:%S %a ' #配置输出时间的格式，注意月份和天数不要搞乱了
    logging.basicConfig(level=logging.INFO,
                        format=LOG_FORMAT,
                        datefmt = DATE_FORMAT ,
                        filename= './result.log' #有了filename参数就不会直接输出显示到控制台，而是直接写入文件
                        )
    # 此处的api_baseUrl是本地api部署址
    def __init__(self, standard=True, data='', api_baseUrl='http://localhost:5000', ):
        self.data = data
        self.standard = standard
        self.api_baseUrl = api_baseUrl

    def get_parameters(self, componentName):
        url = self.api_baseUrl + '/api/v1/parameters/search?componentName=%s' % componentName
        reponse = requests.get(url)
        reponse_dict = json.loads(reponse.text)
        return reponse_dict['data']

    def validate(self, interfaceName, parameter_dict):
        # 获取接口对应的请求参数、返回参数等信息
        parameters = parameter_dict[interfaceName]
        method = parameters['httpVerb'].upper()
        # 此处的url为被测云平台的部署地址
        url = 'http://20.3.4.68:8080' + parameters['url']
        standardResponse = parameters['response']
        query = parameters['query']

        result = {'code': 200, 'message': '', 'data': ''}

        try:
            if method == 'GET':
                if query:
                    url += '?'
                    for each in list(query.keys()):
                        url += each + '=' + query[each] + '&'
                    url = url[:-1]
                logging.info('请求URL：')
                logging.info(url)
                reponse = requests.get(url=url)
                reponse_dict = json.loads(reponse.text)
            elif method == 'POST':
                header = {"Content-Type": "application/json; charset=UTF-8"}
                logging.info('请求URL：')
                logging.info(url)
                logging.info('请求参数：')
                logging.info(query)
                reponse = requests.post(url=url, json=query, headers=header)
                reponse_dict = json.loads(reponse.text)
            elif method == 'DELETE':
                logging.info('请求URL：')
                logging.info(url)
                logging.info('请求参数：')
                logging.info(query)
                reponse = requests.delete(url=url,json=query)
                reponse_dict = json.loads(reponse.text)
            else:
                logging.info('Unknown method: ', method)
        except Exception as error:
            # 请求发生错误：1）视为不符合 2）记录error
            result['code'] = 201
            result['message'] = '无法得到正常响应'
            result['data'] = error

        else:
            if len(reponse_dict) < len(standardResponse):
                result['code'] = 202
                result['message'] = '缺少参数'
                result['data'] = reponse_dict
            else:
                # 判断返回参数是否正确
                reponseKey = reponse_dict.keys()

                flag = True
                for each in standardResponse:
                    if each in reponseKey:  # 参数名称都正确
                        pass
                        # if reponse_dict[each]:
                        #     pass
                        # else:  # 参数名称都正确 and 均在关键参数空值的返回
                        #     flag = False
                        #     result['code'] = 203
                        #     result['message'] = '关键参数值为空'
                        #     result['data'] = reponse_dict
                    else:  # 参数名称不正确
                        flag = False
                        result['code'] = 203
                        result['message'] = '返回参数名称不符'
                        result['data'] = reponse_dict

                if flag:
                    result['message'] = '符合'
                    result['data'] = reponse_dict
        logging.info('返回结果：')
        logging.info(result)
        return result
    # 异步操作的效果需要等待一段时间，尝试10次，共20秒，若一直失败则判定为不通过
    def re_exe(self,interfaceName,parameters):
        loop = True
        try_time=1
        while loop and try_time<=10:
            result=self.validate(interfaceName, parameters)
            logging.info('第%s次测试结果：' %try_time)
            logging.info(result)
            if result['code']!=200:
                loop=True
                try_time+=1
                time.sleep(2)

            else:
                break
        return result
