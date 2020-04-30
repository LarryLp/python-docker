#!/usr/bin/python
# -*- coding: UTF-8 -*-
from validation import FitnessValidation
import logging
import time
def main():
    print('OBS')
    LOG_FORMAT = "%(asctime)s %(name)s %(levelname)s %(pathname)s %(message)s "
    DATE_FORMAT = '%Y-%m-%d  %H:%M:%S %a '
    logging.basicConfig(level=logging.INFO,
                        format=LOG_FORMAT,
                        datefmt = DATE_FORMAT ,
                        filename = './result.log')
    # 1.测试准备，对“存储桶”相关接口的测试需在“创建存储桶”、“获取存储桶信息”测试通过!的前提下进行
    # 为后续接口的功能验证做准备，创建2个存储桶，“gass-bucket1”、“gass-bucket2”
    logging.info("'对象存储'模块测试开始！")
    logging.info("备注：创建2个存储桶，供后续接口测试使用")
    Object_parameters = FitnessValidation().get_parameters('objectStorage')
    flag = True
    logging.info('1.创建存储桶')
    logging.info('1.1 创建存储桶gass-bucket1')
    createBucket_result1=FitnessValidation().validate('createBucket', Object_parameters)
    logging.info('1.2 创建存储桶gass-bucket2')
    Object_parameters['createBucket']['query']['iaasBucketName']="gass-bucket2"
    createBucket_result2=FitnessValidation().validate('createBucket', Object_parameters)
    if createBucket_result1['code'] == 200 and createBucket_result2['code'] == 200:
        logging.info('测试结果:')
        logging.info('接口%s的符合性测试通过！' % 'createBucket')
        time.sleep(10)
        logging.info('通过查询接口验证是否创建成功：')
        logging.info('2.获取存储桶信息')
        logging.info('2.1 查询存储桶gass-bucket1')
        Object_parameters['queryBucket']['query']['iaasBucketName']="gass-bucket1"
        queryBucket_result1=FitnessValidation().validate('queryBucket', Object_parameters)
        logging.info('2.2 查询存储桶gass-bucket2')
        Object_parameters['queryBucket']['query']['iaasBucketName']="gass-bucket2"
        queryBucket_result2=FitnessValidation().validate('queryBucket', Object_parameters)
        if queryBucket_result1['code'] == 200 and queryBucket_result2['code'] == 200:
            logging.info('测试结果:')
            logging.info('接口%s的符合性测试通过!' % 'queryBucket')
             # 若查询到的存储桶信息与创建时的一致，则证明功能验证通过
            # 创建存储桶、获取存储桶信息的功能测试均通过
            time.sleep(10)
            logging.info("createBucket和queryBucket的功能验证：")
            if queryBucket_result1['data']['iaasBucketName']==createBucket_result1['data']['iaasBucketName'] and queryBucket_result2['data']['iaasBucketName']==createBucket_result2['data']['iaasBucketName']:
                logging.info('查询到的存储桶信息与创建时的信息一致')
                logging.info('测试结果:')
                logging.info('接口%s的功能测试通过!' % 'createBucket 和 queryBucket')
            else:
                logging.info('测试结果:')
                logging.info('‘获取存储桶信息’查询到的信息与创建的不一致，功能测试不通过！！')
                logging.info('请确保在此接口通过的前提下，进行后续接口的测试')
                flag = False
        else:
            logging.info('测试结果:')
            logging.info('接口%s的符合性测试不通过！' % 'queryBucket')
            logging.info('请确保在此接口通过的前提下，进行后续接口的测试')
            flag = False
    else:
        logging.info('测试结果:')
        logging.info('接口%s的符合性测试不通过！' % 'createBucket')
        logging.info('请确保在此接口通过的前提下，进行后续接口的测试')
        flag = False
    # 若上述2个关键接口的符合性及功能测试均通过，则进行下一步测试
    time.sleep(10)
    if flag:
        logging.info('3.更新存储桶')
        Object_parameters['updateBucket']['query']['iaasBucketPermission']=2
        updateBucket_result=FitnessValidation().validate('updateBucket', Object_parameters)
        if updateBucket_result['code'] == 200:
            logging.info('测试结果:')
            logging.info('接口%s的符合性测试通过!' % 'updateBucket')
            time.sleep(10)
            logging.info("updateBucket的功能验证：")
            #调用 “获取存储桶信息”接口，查询gass-bucket1的信息是否更新成功
            logging.info('通过查询接口验证更新是否成功：')
            Object_parameters['queryBucket']['query']['iaasBucketName']="gass-bucket1"
            queryBucket_result=FitnessValidation().validate('queryBucket', Object_parameters)
            if queryBucket_result['data']['iaasBucketPermission']==Object_parameters['updateBucket']['query']['iaasBucketPermission']:
                logging.info('查询到的存储桶信息与更新的信息一致')
                logging.info('测试结果:')
                logging.info('接口%s的功能测试通过!' % 'updateBucket')
            else:
                logging.info('测试结果:')
                logging.info('更新后查询的结果与更新的请求参数不符，更新失败')
        else:
            logging.info('测试结果:')
            logging.info('接口%s的符合性测试不通过！' % 'updateBucket')
        time.sleep(10)
        logging.info('4.列举存储桶')
        listBucket_result=FitnessValidation().validate('listBucket', Object_parameters)
        if listBucket_result['code'] == 200:
            logging.info('接口%s的符合性测试通过!' % 'listBucket')
            time.sleep(10)
            logging.info("listBucket的功能验证：")
            if Object_parameters['createBucket']['query']['iaasBucketName'] in listBucket_result['data']['iaasBucketName']:
                logging.info('列举已创建的存储桶成功')
                logging.info('测试结果:')
                logging.info('接口%s的功能测试通过!' % 'listBucket')
            else:
                logging.info('测试结果:')
                logging.info('接口%s的功能测试不通过！，已创建的存储桶列举失败' % 'listBucket')
        else:
            logging.info('测试结果:')
            logging.info('接口%s的符合性测试不通过！' % 'listBucket')
        #需保证“创建对象”和“查询对象信息”2个接口通过的前提下进行“对象”相关的测试
        flag1=True
        time.sleep(10)
        logging.info("5.创建对象")
        createObject_result=FitnessValidation().validate('createObject', Object_parameters)
        if createObject_result['code'] == 200:
            logging.info('测试结果:')
            logging.info('接口%s的符合性测试通过!' % 'createObject')
            time.sleep(10)
            logging.info("通过查询对象信息来判断是否创建成功:")
            #调用“查询对象信息”接口来判断是否创建成功
            logging.info("6.对象信息查询")
            queryObject_result=FitnessValidation().validate('queryObject', Object_parameters)
            if queryObject_result['code'] == 200:
                logging.info('测试结果:')
                logging.info('接口%s的符合性测试通过!' % 'queryObject')
                time.sleep(10)
                logging.info("createObject 和 queryObject的功能验证：")
                if queryObject_result['data']['iaasObjectName'] == Object_parameters['createObject']['query']['iaasObjectName']:
                    logging.info('‘查询对象信息’查询到的信息与创建的一致')
                    logging.info('测试结果:')
                    logging.info('接口%s的功能测试通过!' % 'createObject 和 queryObject')
                else:
                    logging.info('测试结果:')
                    logging.info('‘查询对象信息’查询到的信息与创建的不一致，功能测试不通过！！')
                    logging.info('请确保在此接口通过的前提下，进行后续接口的测试')
                    flag1 = False
            else:
                logging.info('测试结果:')
                logging.info('接口%s的符合性测试不通过！' % 'queryObject')
                logging.info('请确保在此接口通过的前提下，进行后续接口的测试')
                flag1 = False
        else:
            logging.info('测试结果:')
            logging.info('接口%s的符合性测试不通过！' % 'createObject')
            logging.info('请确保在此接口通过的前提下，进行后续接口的测试')
            flag1 = False
        time.sleep(10)
        if flag1:
            logging.info("7.列举对象")
            listObject_result=FitnessValidation().validate('listObject', Object_parameters)
            if listObject_result['code'] == 200:
                logging.info('测试结果:')
                logging.info('接口%s的符合性测试通过!' % 'listObject')
                time.sleep(10)
                logging.info("listObject的功能验证：")
                if listObject_result['data']['iaasObjectInfo'][0]['iaasObjectName']==Object_parameters['createObject']['query']['iaasObjectName']:
                    logging.info('已创建的对象列举成功')
                    logging.info('测试结果:')
                    logging.info('列举的信息包括了创建的对象，“列举对象”功能验证通过！')
                else:
                    logging.info('测试结果:')
                    logging.info('列举的结果不包含已创建的对象，接口%s的功能测试不通过！' % 'listObject')
            else:
                logging.info('接口%s的符合性测试不通过！' % 'listObject')
            time.sleep(10)
            logging.info("8.复制对象")
            copyObject_result=FitnessValidation().validate('copyObject', Object_parameters)
            if copyObject_result['code'] == 200:
                logging.info('测试结果:')
                logging.info('接口%s的符合性测试通过!' % 'copyObject')
                time.sleep(10)
                logging.info("copyObject的功能验证：")
                logging.info("通过查询复制的对象，验证是否复制成功：")
                Object_parameters['queryObject']['query']['iaasBucketName']=copyObject_result['data']['iaasDestinationBucketName']
                Object_parameters['queryObject']['query']['iaasObjectName']=copyObject_result['data']['iaasDestinationObjectName']
                queryObject_result=FitnessValidation().validate('queryObject', Object_parameters)
                if queryObject_result['data']['iaasObjectName']==copyObject_result['data']['iaasDestinationObjectName']:
                    logging.info('复制的对象查询成功')
                    logging.info('测试结果:')
                    logging.info('接口%s的功能测试通过!' % 'copyObject')
                else:
                    logging.info('测试结果:')
                    logging.info('未查询到复制的对象，功能测试不通过！！')
            else:
                logging.info('测试结果:')
                logging.info('接口%s的符合性测试不通过！' % 'copyObject')
            time.sleep(10)
            logging.info("9.权限管理")
            setObjectPermission_result=FitnessValidation().validate('setObjectPermission', Object_parameters)
            if setObjectPermission_result['code'] == 200:
                logging.info('测试结果:')
                logging.info('接口%s的符合性测试通过!' % 'setObjectPermission')
                time.sleep(10)
                logging.info("setObjectPermission的功能验证：")
                logging.info("通过查询对象的权限信息，验证修改权限是否成功：")
                Object_parameters['queryObject']['query']['iaasBucketName']=setObjectPermission_result['data']['iaasBucketName']
                Object_parameters['queryObject']['query']['iaasObjectName']=setObjectPermission_result['data']['iaasObjectName']
                queryObject_result=FitnessValidation().validate('queryObject', Object_parameters)
                if queryObject_result['data']['iaasObjectPermission']==Object_parameters['setObjectPermission']['query']['iaasObjectPermission']:
                    logging.info('‘查询对象信息’查询到的权限信息与设置的一致')
                    logging.info('测试结果:')
                    logging.info('接口%s的功能测试通过!' % 'setObjectPermission')
                else:
                    logging.info('测试结果:')
                    logging.info('‘查询对象信息’查询到的权限信息与设置的不一致，功能测试不通过！！')
            else:
                logging.info('测试结果:')
                logging.info('接口%s的符合性测试不通过！' % 'setObjectPermission')
            time.sleep(10)
            logging.info("10.下载对象")
            getObjectContent_result=FitnessValidation().validate('getObjectContent', Object_parameters)
            if getObjectContent_result['code'] == 200:
                logging.info('测试结果:')
                logging.info('接口%s的符合性测试通过!' % 'getObjectContent')
            else:
                logging.info('测试结果:')
                logging.info('接口%s的符合性测试不通过！' % 'getObjectContent')
            time.sleep(10)
            logging.info("11.删除对象")
            Object_parameters['deleteObject']['query']['iaasBucketName']=createObject_result['data']['iaasBucketName']
            Object_parameters['deleteObject']['query']['iaasObjectName']=[createObject_result['data']['iaasObjectName']]
            deleteObject_result=FitnessValidation().validate('deleteObject', Object_parameters)
            if deleteObject_result['code'] == 200:
                logging.info('测试结果:')
                logging.info('接口%s的符合性测试通过!' % 'deleteObject_result')
                time.sleep(10)
                logging.info('deleteObject的功能验证：')
                logging.info('通过查询该对象，验证是否删除成功：')
                Object_parameters['queryObject']['query']['iaasBucketName']=createObject_result['data']['iaasBucketName']
                Object_parameters['queryObject']['query']['iaasObjectName']=createObject_result['data']['iaasObjectName']
                queryObject_result=FitnessValidation().validate('queryObject', Object_parameters)
                if queryObject_result['data']['iaasObjectName']=='':
                    logging.info('已查询不到被删除的对象')
                    logging.info('测试结果:')
                    logging.info('接口%s的功能测试通过!' % 'deleteObject')
                else:
                    logging.info('测试结果:')
                    logging.info('删除object失败，接口%s的功能测试不通过！' % 'deleteObject')
            else:
                logging.info('测试结果:')
                logging.info('接口%s的符合性测试不通过！' % 'deleteObject')
        time.sleep(10)
        logging.info("12.删除存储桶")
        Object_parameters['deleteBucket']['iaasBucketName']=createBucket_result1['data']['iaasBucketName']
        deleteBucket_result=FitnessValidation().validate('deleteBucket', Object_parameters)
        if deleteBucket_result['code'] == 200:
            logging.info('测试结果:')
            logging.info('接口%s的符合性测试通过!' % 'deleteBucket')
            time.sleep(10)
            logging.info('deleteBucket的功能验证：')
            logging.info('通过查询该存储桶，验证是否删除成功：')
            queryBucket_result=FitnessValidation().validate('queryBucket', Object_parameters)
            if queryBucket_result['data']['iaasBucketName']=='':
                logging.info('已查询不到被删除的存储桶')
                logging.info('测试结果:')
                logging.info('接口%s的功能测试通过!' % 'deleteBucket')
            else:
                logging.info('测试结果:')
                logging.info('删除bucket失败，接口%s的功能测试不通过！' % 'deleteBucket')
        else:
            logging.info('测试结果:')
            logging.info('接口%s的符合性测试不通过！' % 'deleteBucket')
if __name__ == '__main__':
    main()
