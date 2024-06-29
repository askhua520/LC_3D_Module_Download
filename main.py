import os
import codecs
import requests
import json

# 获取用户的主目录路径
user_home = os.path.expanduser("~")

# 构建桌面路径
path = os.path.join(user_home, 'desktop')

while True:
    code = input("请输入立创商城器件编号：")
    #---------------------------------------------------------------#
    has_url = 'https://pro.lceda.cn/api/eda/product/search'  # 根据编号搜索hasDevice
    has_formdata = {
        'keyword': code,
        'needAggs': 'true',
        'url': '/api/eda/product/list',
        'currPage': '1',
        'pageSize': '10'
    }
    r0 = requests.post(has_url, data=has_formdata)
    json_data = json.loads(r0.text)
    Data_ls = json_data['result']
    Data_ls2 = Data_ls['productList']
    Datas = Data_ls2[0]
    hasDevice = Datas['hasDevice']
    print(json_data)

    #---------------------------------------------------------------#
    url = 'https://pro.lceda.cn/api/devices/searchByIds'
    formdata = {
        'uuids[]': hasDevice,
        'path': path
    }
    r1 = requests.post(url, data=formdata)
    json1_data = json.loads(r1.text)
    Data1_ls = json1_data['result']
    Data1_ls2 = Data1_ls[0]
    Data1_ls3 = Data1_ls2['attributes']
    Model_id = Data1_ls3['3D Model']
    foot_name = Data1_ls3['Supplier Footprint']
    print(foot_name)

    #---------------------------------------------------------------#
    url2 = 'https://pro.lceda.cn/api/components/searchByIds?forceOnline=1'  # 请求3d封装名称
    formdata2 = {
        'uuids[]': Model_id,
        'dataStr': 'yes',
        'path': path
    }
    r2 = requests.post(url2, data=formdata2)
    json1_data = json.loads(r2.text)
    Data2_ls = json1_data['result']
    Data2_ls2 = Data2_ls[0]
    Data2_ls3 = Data2_ls2['dataStr']
    Data2_ls4 = json.loads(Data2_ls3)
    Model_id0 = Data2_ls4['model']
    print(json1_data)

    #---------------------------------------------------------------#
    # 获取step封装
    download_url = "https://modules.lceda.cn/qAxj6KHrDKw4blvCG8QJPs7Y/" + Model_id0
    r3 = requests.get(download_url)
    demo = r3.text
    filename = os.path.join(path, foot_name + '.step')
    with codecs.open(filename, 'w', 'utf-8') as f:
        f.write(demo)
    print(f"3D模型下载成功: {filename}")
