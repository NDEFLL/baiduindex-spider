from datetime import datetime, timedelta

import requests
import json
import csv

# 网页中的解密函数
# decrypt: function(t, e) {
#             if (!t)
#                 return "";
#             for (var i = t.split(""), n = e.split(""), a = {}, r = [], A = 0; A < i.length / 2; A++)
#                 a[i[A]] = i[i.length / 2 + A];
#             for (var o = 0; o < e.length; o++)
#                 r.push(a[n[o]]);
#             return r.join("")
#         },

# 解密函数
def decrypt(t, e):
    n = len(t)//2

    a = dict(zip(t[:n], t[n:]))   #将ptbk分成前后两半部分，前半部分为键，后半部分为值
    # 遍历每个字符,并在字典中查找对应的解密字符
    return "".join([a[o] for o in e])

# 生成日期列表
def generate_date_list(start_date, end_date):
    start_date_obj = datetime.strptime(start_date, "%Y-%m-%d")
    end_date_obj = datetime.strptime(end_date, "%Y-%m-%d")
    delta = (end_date_obj - start_date_obj).days + 1  # 计算全年天数
    return [start_date_obj + timedelta(days=i) for i in range(delta)]

# 填充缺失数据
def pad_data(data, target_length):
    if len(data) < target_length:
        data.extend([0] * (target_length - len(data)))
    return data

keys = ["广东旅游"]
startDate = 2020
endDate = 2024
# 请求头配置
headers = {
        "Connection": "keep-alive",
        "Accept": "application/json, text/plain, */*",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.198 Safari/537.36",
        "Sec-Fetch-Site": "same-origin",
        "Sec-Fetch-Mode": "cors",
        "Sec-Fetch-Dest": "empty",
        "Cipher-Text": "1698156005330_1698238860769_ZPrC2QTaXriysBT+5sgXcnbTX3/lW65av4zgu9uR1usPy82bArEg4m9deebXm7/O5g6QWhRxEd9/r/hqHad2WnVFVVWybHPFg3YZUUCKMTIYFeSUIn23C6HdTT1SI8mxsG5mhO4X9nnD6NGI8hF8L5/G+a5cxq+b21PADOpt/XB5eu/pWxNdwfa12krVNuYI1E8uHQ7TFIYjCzLX9MoJzPU6prjkgJtbi3v0X7WGKDJw9hwnd5Op4muW0vWKMuo7pbxUNfEW8wPRmSQjIgW0z5p7GjNpsg98rc3FtHpuhG5JFU0kZ6tHgU8+j6ekZW7+JljdyHUMwEoBOh131bGl+oIHR8vw8Ijtg8UXr0xZqcZbMEagEBzWiiKkEAfibCui59hltAgW5LG8IOtBDqp8RJkbK+IL5GcFkNaXaZfNMpI=",
        "Referer": "https://index.baidu.com/v2/main/index.html",
        "Accept-Language": "zh-CN,zh;q=0.9",
        'Cookie': 'BIDUPSID=73A02B29604FEA7390D8DC911F2F3182; PSTM=1714975449; BAIDUID=73A02B29604FEA73F003D771070ACA58:FG=1; H_WISE_SIDS_BFESS=61027_61054_61098_60853_61114_61141_61155_61218_61207_61210_61208_61214_61234; H_WISE_SIDS=61027_61674_62169_62184_62187_62183_62283_62325_62341; BAIDUID_BFESS=73A02B29604FEA73F003D771070ACA58:FG=1; Hm_lvt_d101ea4d2a5c67dab98251f0b5de24dc=1740624162,1742534901; HMACCOUNT=D4F157DB7EC77225; ppfuid=FOCoIC3q5fKa8fgJnwzbE67EJ49BGJeplOzf+4l4EOvDuu2RXBRv6R3A1AZMa49I27C0gDDLrJyxcIIeAeEhD8JYsoLTpBiaCXhLqvzbzmvy3SeAW17tKgNq/Xx+RgOdb8TWCFe62MVrDTY6lMf2GrfqL8c87KLF2qFER3obJGkjS1Q+e/k7Rs6uiFpI37bSGEimjy3MrXEpSuItnI4KD9KksgOvde5bWiznpaD8XPvec00d5zy/PfOke0GlwLH6aarJj4DjNBifG+nBZjbJLhJsVwXkGdF24AsEQ3K5XBbh9EHAWDOg2T1ejpq0s2eFy9ar/j566XqWDobGoNNfmfpaEhZpob9le2b5QIEdiQcF+6iOKqU/r67N8lf+wxW6FCMUN0p4SXVVUMsKNJv2T/GamCSC3fVrsTWnPmpzB9jasmgOrJ40n63OsKSOpoSLBCO7+QldZ72iFUBLi59Hd5zJw3uXcmAZ/d4pYOPYL/7Q+//wdrn6SUz7a0vEMm7QqGqBJJILGchC/ZM0axiniVRKx4R3cqVpTVNqTP1tWGnGGu/AVLS3NcPF3XemJkZyi6L0BPA661JDj0lmZIgcCHm0lGODoYWzuL7ZDizBm0d8BJIJUS1lUOPNebjg5OCjwkSq16g64gugrO/OhN+XjRMTNne43cKuMDmex1CEngB2QvyTjxXMcJvDDEe3McIycHFbZmbEY9LT3RuWsSjij5HIeKAxeCJRzKQmiJrt2NeRZWapfkUEaTaBAP7Zh9q8HTpUnhZYIFif/4nddzodRSraHHBAOBUI15Uu3uPYGyJ/q1uQn9VsBjBmLNQsYnwiX1i39zQE19TGybrzqrM1pMrcfAL1vAAGPaqoVSU+0UqC6Ax2W4+eWZGSFET4OOzFSDqXCDYOVj6mkN34YnjwTqKLSLxy4ZAV9xy7XajfDioUYActwOXbJevGlZWPiC/PgZlslkXZx2dg8mvvQVCLuOQc0bLisc+KfWb7hlRZ37xT8Md02nRY6kZRuXdJ91DNBphe+V4Fu14ttSLk2gIAKE/mhl+gJ6goq69QQA9ddM9WM7RNOLSxWoVJ0b4YXKLTfCWubfAJE3xCxaFPXSlckvRGFwtNqAOfFq4X1+WdXCL0BvZozJbj5gfVVlYhSFve0u80c9MeQcVKn6OT+e9IiqbZApjp5oasaKfm1YDpXXq6oW4FLPwjQp97RBnCTk5BMdgjEiAtnKps2wlMuPlZVfNDYYDl6HxqJXScM4aa1+GJg2NuzY3E/RpwCACk13R7; BDUSS=B5emFLUHBnRlQ2T1ZLcGd3NmxzaDZ0eFplTzcyZX5CSzZYTEwtd29jSW1oZ1JvRUFBQUFBJCQAAAAAAAAAAAEAAACuUs9PTmRlZkxfOTcAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAACb53Gcm-dxnQT; SIGNIN_UC=70a2711cf1d3d9b1a82d2f87d633bd8a04925473999pzhUp0MS1Sc9ZpWEfBLIzmnZ6cXWKvJET208quStKFoqGot7h9a4uT8eG6PsghT52iMpi%2BcxVEEKUrWcBtXwc1Neao5GKx0MkP7T4%2FHAFlHtcGWoAqVyL%2FU3X0fav45my%2BIWXWFs4A07NgHQSsM8Ju4JhJNPG9WAZNYi6AxBVR%2BfI%2FG6CExn%2F5VgUfhT%2FP3D6x57vO%2B71C8tM8I7YwMCvK0bNU5OOLnxyOuFTSNvIgT6pUNwA422itMbRh7ATVjNwyxunaf%2FbNNKDHt%2FSo22xA%3D%3D93831287145419718733483258253925; __cas__rn__=492547399; __cas__st__212=e3b492db94b2112993d1e284a7474b226741c12f2f469c20b6ed2b2c88f23632f8fac83f45633fc926e6d179; __cas__id__212=59276089; CPTK_212=1692057612; CPID_212=59276089; bdindexid=g3bcmduodhs2dgab4o49e6ccp7; H_PS_PSSID=61027_61674_62325_62341_62370_62393_62427_62476_62456_62455_62453_62450_62546_62637_62644_62674_62687; BA_HECTOR=81a10k8l0h2gak0k21a00484089dtg1jtpufj23; ZFY=T5FZm98TPz8zngsJ5ZvND:BjrUQmDKN0OjXcZ:AfZleMo:C; BDRCVFR[feWj1Vr5u3D]=I67x6TjHwwYf0; PSINO=1; delPer=0; BDORZ=B490B5EBF6F3CD402E515D22BCDA1598; RT="z=1&dm=baidu.com&si=5f747355-f306-463a-9a66-fd2ebc567db2&ss=m8icajdp&sl=13&tt=ga9j&bcn=https%3A%2F%2Ffclog.baidu.com%2Flog%2Fweirwood%3Ftype%3Dperf"; Hm_lpvt_d101ea4d2a5c67dab98251f0b5de24dc=1742551864; BDUSS_BFESS=B5emFLUHBnRlQ2T1ZLcGd3NmxzaDZ0eFplTzcyZX5CSzZYTEwtd29jSW1oZ1JvRUFBQUFBJCQAAAAAAAAAAAEAAACuUs9PTmRlZkxfOTcAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAACb53Gcm-dxnQT; ab_sr=1.0.1_NzNjNzY1MWQ3OGY0NDE3NTZhOTYyOTZkZWY1N2UwODRkOWUwMzNiY2Y2N2I5ZGY4YjhiZjMzN2NjMWFmNmViZjA1MTFjYzFmZjM5ZDcyYjBmZTUzMmY1YTIzZWY2N2IwYTdhMDFlMDljNWI5NmU3YmFkMjQ3ZDY5NmQ3YzQwODVhZDFmMzM4NmE4YjgzNDVjYzZhMGM3OWIyMDNmZjczYQ=='
}

output_csv = "baidu_index.csv"  # 输出CSV文件名

# 创建 CSV 文件并写入表头
with open(output_csv, mode='w', newline='', encoding='utf-8') as file:
    writer = csv.writer(file)
    writer.writerow(["搜索关键字", "日期", "搜索数量"])  # 写入表头

for key in keys:
    for year in range(startDate, endDate + 1):
        print(f"正在处理第{year}年，请耐心等待……")
        words = [[{"name": key, "wordType": 1}]]
        words = str(words).replace(" ", "").replace("'", "\"")
        start_date = f"{year}-01-01"
        end_date = f"{year}-12-31"

        # 请求百度指数API
        url = f'http://index.baidu.com/api/SearchApi/index?area=0&word={words}&startDate={start_date}&endDate={end_date}'
        res = requests.get(url, headers=headers)
        res_json = res.json()
        # print(res_json)
        if res_json["message"] == "bad request":
            print("抓取关键词：" + key + " 失败，请检查cookie或者关键词是否存在")
            continue

        # 获取密钥
        uniqid = res_json['data']["uniqid"]
        ptbk_url = f'http://index.baidu.com/Interface/ptbk?uniqid={uniqid}'
        ptbk_res = requests.get(ptbk_url, headers=headers)
        t = ptbk_res.json()['data']

        # 获取加密数据
        data = res_json['data']
        encrypted_data = data['userIndexes'][0]['all']['data']

        decrypted_data = [int(x) for x in decrypt(t, encrypted_data).split(",")]


        if (year % 4 == 0 and year % 100 != 0) or (year % 400 == 0):
            days_in_year = 366
        else:
            days_in_year = 365

        # 填充数据
        decrypted_data = pad_data(decrypted_data, days_in_year)

        # 生成日期列表
        date_list = generate_date_list(start_date, end_date)

        # 写入 CSV
        with open(output_csv, mode='a', newline='', encoding='utf-8') as file:
            writer = csv.writer(file)
            for date, value in zip(date_list, decrypted_data):
                writer.writerow([key, date.strftime("%Y-%m-%d"), value])

print("数据已保存至 baidu_index.csv")
