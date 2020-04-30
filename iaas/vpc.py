#!/usr/bin/python
# -*- coding: UTF-8 -*-
import time
import logging

from validation import FitnessValidation

def main():
    print('vpc')
    LOG_FORMAT = "%(asctime)s %(name)s %(levelname)s %(pathname)s %(message)s "#配置输出日志格式
    DATE_FORMAT = '%Y-%m-%d  %H:%M:%S %a ' #配置输出时间的格式，注意月份和天数不要搞乱了
    logging.basicConfig(level=logging.INFO,
                        format=LOG_FORMAT,
                        datefmt = DATE_FORMAT ,
                        filename= './result.log' #有了filename参数就不会直接输出显示到控制台，而是直接写入文件
                        )
    logging.info('开始VPC测试')
    vpc = FitnessValidation()
    vpc_parameters = vpc.get_parameters('vpc')
    logging.info('开始初始化')
    # set value
    vpc_parameters['createVpc']['query']['iaasVpcName'] = 'gass_initial'
    vpc_parameters['createVpc']['query']['iaasVpcDescription'] = 'gass_VpcDescription'
    vpc_parameters['createVpc']['query']['iaasVpcSubnetIp'] = '192.168.8.0/24'
    vpc_parameters['createVpc']['query']['accessToken'] = 'gass_token'

    initialize = vpc.validate('createVpc', vpc_parameters)
    if initialize['code'] == 200:
        logging.info('初始化完成')
        try:
            logging.info('开始数据准备')
            vpc_info = []
            #  数据准备 vpc1
            vpc_parameters['createVpc']['query']['iaasVpcName'] = 'gass_vpc1'
            vpc_parameters['createVpc']['query']['iaasVpcDescription'] = 'gass_Vpc1_Description'
            vpc_parameters['createVpc']['query']['iaasVpcSubnetIp'] = '192.168.9.0/24'
            vpc_parameters['createVpc']['query']['accessToken'] = 'gass_token'
            vpc1 = vpc.validate('createVpc', vpc_parameters)
            vpc_info.append(vpc1['data']['iaasVpcId'])

            #  数据准备 vpc2
            vpc_parameters['createVpc']['query']['iaasVpcName'] = 'gass_vpc2'
            vpc_parameters['createVpc']['query']['iaasVpcDescription'] = 'gass_Vpc2_Description'
            vpc_parameters['createVpc']['query']['iaasVpcSubnetIp'] = '192.168.10.0/24'
            vpc_parameters['createVpc']['query']['accessToken'] = 'gass_token'
            vpc2 = vpc.validate('createVpc', vpc_parameters)
            vpc_info.append(vpc2['data']['iaasVpcId'])

        except Exception as error:
            logging.info(error)
        else:
            # 测试执行
            if vpc1['code'] == 200 and vpc2['code'] == 200:
                logging.info('完成数据准备')
                time.sleep(10)
                logging.info('============================================创建VPC测试开始============================================')
                list_vpc = vpc.validate('listVpc', vpc_parameters)
                if list_vpc['code'] == 200:
                    logging.info('listVpc接口符合')
                    for eachId in [vpc1['data']['iaasVpcId'], vpc2['data']['iaasVpcId']]:
                        if eachId in list_vpc['data']['iaasVpcId']:
                            pass
                        else:
                            logging.info('listVpc 不符合：', eachId)
                            break
                        logging.info('listVpc功能符合')
                else:
                    logging.info('listVpc接口不符合')
                    logging.info('listVpc功能不符合')
                logging.info('============================================创建VPC测试完成============================================')

                # 更新VPC
                logging.info('============================================更新VPC测试开始============================================')
                vpc_parameters['updateVpc']['query']['iaasVpcId'] = vpc1['data']['iaasVpcId']
                vpc_parameters['updateVpc']['query']['iaasVpcName'] = 'gass_vpc1_update'
                vpc_parameters['updateVpc']['query']['iaasVpcDescription'] = 'gass_Vpc1_Description_update'
                vpc_parameters['queryVpc']['query']['iaasVpcId'] = vpc1['data']['iaasVpcId']
                update_vpc = vpc.validate('updateVpc', vpc_parameters)
                if update_vpc['code'] == 200:
                    logging.info('updateVpc 接口符合')
                    # 使用查询VPC来【验证】
                    time.sleep(10)
                    query_vpc = vpc.validate('queryVpc', vpc_parameters)
                    if query_vpc['code'] == 200:
                        logging.info('queryVpc 接口符合')
                        if query_vpc['data']['iaasVpcName'] == vpc_parameters['updateVpc']['query']['iaasVpcName'] and query_vpc['data']['iaasVpcDescription'] == vpc_parameters['updateVpc']['query']['iaasVpcDescription']:
                            logging.info('updateVpc 功能符合')
                            logging.info('queryVpc 功能符合')
                        else:
                            logging.info('queryVpc功能不符合:', update_vpc)
                            logging.info('updateVpc功能不符合:', update_vpc)
                    else:
                        logging.info('queryVpc接口不符合:', update_vpc)
                        logging.info('queryVpc功能不符合:', update_vpc)
                        logging.info('updateVpc功能不符合:', update_vpc)
                else:
                    logging.info('updateVpc接口不符合:', update_vpc)
                    logging.info('updateVpc功能不符合:', update_vpc)
                logging.info('============================================更新VPC测试完成============================================')

                logging.info('============================================创建子网测试开始============================================')
                # 创建子网1
                subnet_info = []
                vpc_parameters['createSubnet']['query']['iaasVpcId'] = vpc2['data']['iaasVpcId']
                vpc_parameters['createSubnet']['query']['iaasVpcSubnetName'] = 'gass_subnet1'
                vpc_parameters['createSubnet']['query']['iaasVpcSubnetIpDescription'] = 'gass_subnet_description'
                vpc_parameters['createSubnet']['query']['iaasVpcSubnetIp'] = '192.168.12.0/24'
                vpc_parameters['createSubnet']['query']['iaasVpcSubnetIpVersion'] = 1
                vpc_parameters['createSubnet']['query']['iaasVpcSubnetGatewayIp'] = '192.168.12.1'
                subnet1 = vpc.validate('createSubnet', vpc_parameters)
                subnet_info.append({'iaasVpcSubnetId': subnet1['data']['iaasVpcSubnetId'], 'iaasVpcSubnetName': vpc_parameters['createSubnet']['query']['iaasVpcSubnetName']})

                # 创建子网2
                vpc_parameters['createSubnet']['query']['iaasVpcId'] = vpc2['data']['iaasVpcId']
                vpc_parameters['createSubnet']['query']['iaasVpcSubnetName'] = 'gass_subnet2'
                vpc_parameters['createSubnet']['query']['iaasVpcSubnetIpDescription'] = 'gass_subnet_description'
                vpc_parameters['createSubnet']['query']['iaasVpcSubnetIp'] = '192.168.13.0/24'
                vpc_parameters['createSubnet']['query']['iaasVpcSubnetIpVersion'] = 1
                vpc_parameters['createSubnet']['query']['iaasVpcSubnetGatewayIp'] = '192.168.13.1'
                subnet2 = vpc.validate('createSubnet', vpc_parameters)
                subnet_info.append({'iaasVpcSubnetId': subnet2['data']['iaasVpcSubnetId'], 'iaasVpcSubnetName': vpc_parameters['createSubnet']['query']['iaasVpcSubnetName']})

                vpc_parameters['listSubnet']['query']['iaasVpcId'] = vpc2['data']['iaasVpcId']

                if subnet1['code'] == 200 and subnet2['code'] == 200:
                    logging.info('createSubnet 接口符合')
                    # 查询子网列表
                    time.sleep(10)
                    list_subnet = vpc.validate('listSubnet', vpc_parameters)
                    if list_subnet['code'] == 200:
                        logging.info('listSubnet 接口符合')
                        list_flag = True
                        for each_subnet in subnet_info:
                            if each_subnet in list_subnet['data']['iaasVpcSubnetInfo']:
                                pass
                            else:
                                list_flag = False
                        if not list_flag:
                            logging.info('listSubnet 功能不符合，列举不全')
                        else:
                            logging.info('createSubnet 功能符合')
                            logging.info('listSubnet 功能符合')
                    else:
                        logging.info('listSubnet 接口不符合')
                        logging.info('listSubnet 功能不符合')
                logging.info('============================================创建子网测试完成============================================')


                # 更新子网
                logging.info('============================================更新子网测试开始============================================')
                vpc_parameters['updateSubnet']['query']['iaasVpcSubnetId'] = subnet2['data']['iaasVpcSubnetId']
                vpc_parameters['updateSubnet']['query']['iaasVpcSubnetName'] = 'gass_subet_name_uapdate'
                vpc_parameters['updateSubnet']['query']['iaasVpcSubnetIpDescription'] = 'gass_subnet_description_update'

                update_subnet = vpc.validate('updateSubnet', vpc_parameters)
                if update_subnet['code'] == 200:
                    logging.info('updateSubnet 接口符合')
                    # 通过【查询子网】来验证【更新子网】
                    time.sleep(10)
                    vpc_parameters['querySubnet']['query']['iaasVpcSubnetId'] = subnet2['data']['iaasVpcSubnetId']
                    query_subnet = vpc.validate('querySubnet', vpc_parameters)
                    if query_subnet['code'] == 200:
                        logging.info('query_subnet 接口符合')
                        if query_subnet['data']['iaasVpcSubnetName'] == vpc_parameters['updateSubnet']['query']["iaasVpcSubnetName"] and \
                                query_subnet['data']['iaasVpcSubnetGatewayIp'] == vpc_parameters['createSubnet']['query']['iaasVpcSubnetGatewayIp'] and \
                                query_subnet['data']['iaasVpcSubnetIpVersion'] == vpc_parameters['createSubnet']['query']["iaasVpcSubnetIpVersion"] and \
                                query_subnet['data']['iaasVpcSubnetIpc'] == vpc_parameters['createSubnet']['query']["iaasVpcSubnetIp"]:
                                    logging.info('updateSubnet 功能符合')
                                    logging.info('querySubnet 功能符合')
                    else:
                        logging.info('querySubnet 接口不符合')
                        logging.info('updateSubnet 功能不符合')

                else:
                    logging.info('updateSubnet 接口不符合')
                    logging.info('updateSubnet 功能不符合')
                logging.info('============================================更新子网测试完成============================================')

                # 删除子网
                logging.info('============================================删除子网测试开始============================================')
                for each in subnet_info:
                    vpc_parameters['deleteSubnet']['query']['iaasVpcSubnetId'] = each['iaasVpcSubnetId']
                    delete_subnet = vpc.validate('deleteSubnet', vpc_parameters)
                    if delete_subnet['code'] == 200:
                        # 通过【查询子网】验证【删除子网】
                        time.sleep(10)
                        vpc_parameters['querySubnet']['query']['iaasVpcSubnetId'] = each['iaasVpcSubnetId']
                        query_subnet = vpc.validate('querySubnet', vpc_parameters)
                        if query_subnet['code'] == 200 and query_subnet['data']['iaasVpcId'] == '':
                            logging.info('deleteSubnet 功能符合')
                        else:
                            logging.info('deleteSubnet 功能不符合')
                    else:
                        logging.info('deleteSubnet 接口不符合')
                        logging.info('deleteSubnet 功能不符合')
                        logging.info('VPC数据清理无法完成：无法通过接口删除子网')
                        logging.info('测试完成')
                        break
                logging.info('============================================删除子网测试完成============================================')

                # 删除VPC 准备
                vpc_parameters['listSubnet']['query']['iaasVpcId'] = vpc2['data']['iaasVpcId']
                list_subnet = vpc.validate('listSubnet', vpc_parameters)
                vpc_parameters['deleteSubnet']['query']['iaasVpcSubnetId'] = list_subnet['data']['iaasVpcSubnetInfo'][0]['iaasVpcSubnetId']
                delete_subnet = vpc.validate('deleteSubnet', vpc_parameters)

                logging.info('============================================删除VPC测试开始============================================')
                vpc_parameters['deleteVpc']['query']['iaasVpcId'] = vpc2['data']['iaasVpcId']
                delete_vpc = vpc.validate('deleteVpc', vpc_parameters)
                if delete_vpc['code'] == 200:
                    logging.info('deleteVpc 接口符合')
                    # 使用【查询VPC】验证【删除VPC】
                    time.sleep(10)
                    vpc_parameters['queryVpc']['query']['iaasVpcId'] = vpc2['data']['iaasVpcId']
                    query_vpc = vpc.validate('queryVpc', vpc_parameters)
                    if query_vpc['code'] == 200 and not query_vpc['data']['iaasVpcId']:
                        logging.info('deleteVpc 功能符合')
                    else:
                        logging.info('deleteVpc 功能不符合')
                        logging.info('无法清理数据')
                else:
                    logging.info('deleteVpc 接口不符合')
                    logging.info('deleteVpc 功能不符合')
                    logging.info('无法清理数据')
                logging.info('============================================删除VPC测试完成============================================')

                # 数据清理
                logging.info('============================================数据清理开始============================================')
                vpc_list = [initialize, vpc1]
                for each in vpc_list:
                    vpc_parameters['listSubnet']['query']['iaasVpcId'] = each['data']['iaasVpcId']
                    vpc_parameters['deleteVpc']['query']['iaasVpcId'] = each['data']['iaasVpcId']
                    list_subnet = vpc.validate('listSubnet', vpc_parameters)
                    time.sleep(5)
                    for subnet in list_subnet['data']['iaasVpcSubnetInfo']:
                        vpc_parameters['deleteSubnet']['query']['iaasVpcSubnetId'] = subnet['iaasVpcSubnetId']
                        time.sleep(5)
                        vpc.validate('deleteSubnet', vpc_parameters)
                    time.sleep(5)
                    vpc.validate('deleteVpc', vpc_parameters)
                logging.info('============================================数据清理完成============================================')
                logging.info('VPC测试完成')
    else:
        logging.info('无法执行检测，创建VPC失败', initialize)
        logging.info('VPC测试完成')


if __name__ == '__main__':
    main()
