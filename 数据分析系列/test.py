import re 

def handle_value(value):
    # 去除空格
    value = value.replace(' ', '')
    # 出现中文的 （）, 也可能出现英文的(),可能有多个括号，用正则表达式一起去掉
    value = re.sub(r'（.*?）', '', value)
    value = re.sub(r'\(.*?\)', '', value)
    # 去除单位 rpm、kw、Nm, 忽略大小写
    value = value.replace('rpm', '')
    value = value.replace('Kw', '')
    value = value.replace('KW', '')
    value = value.replace('kw', '')
    value = value.replace('kW', '')
    value = value.replace('k.W', '')
    value = value.replace('k.w', '')
    value = value.replace('K.W', '')
    value = value.replace('K.w', '')
    value = value.replace('N.m', '')
    value = value.replace('N.M', '')
    value = value.replace('n.m', '')
    value = value.replace('n.M', '')
    value = value.replace('Nm', '')
    value = value.replace('nm', '')
    value = value.replace('NM', '')
    value = value.replace('nM', '')

    # 如果全是中文或者全是英文，直接返回 0
    if re.match(r'^[\u4e00-\u9fa5]+$', value):
        return 0
    if re.match(r'^[a-zA-Z]+$', value):
        return 0
    # 如果有中文，需要去掉中文
    if re.search(r'[\u4e00-\u9fa5]+', value):
        value = re.sub(r'[\u4e00-\u9fa5]+', '', value)
        # 如果有/，先判断是不是两个数字，如果不是，取第一个数字
        if '/' in value:
            arr = value.split('/')
            value = value_arr(arr)

    # 如果有多组数据，例如有, ， 、两个 / 以上，取第一个数字或者第二个数字
    if ',' in value:
        arr = value.split(',')
        value = value_arr(arr)
    if '，' in value:
        arr = value.split('，')
        value = value_arr(arr)
    if '、' in value:
        arr = value.split('、')
        value = value_arr(arr)
    if '/' in value:
        arr = value.split('/')
        value = value_arr(arr)
    
    return value

# 判断数字数组取值
def value_arr(arr):
    value = 0
    if len(arr) >= 2 and arr[0].isdigit() and arr[1].isdigit():
        # 如果第一个数字比1小，取第二个数字
        if float(arr[0]) <= 1:
            value = arr[1]
        else:
            value = arr[0]
    else:
        value = arr[0]
    return value


str1 = '0 / 2000转/分（rpm）（kw）(kw)(KW)'
str2 = '1500转/分（rpm）'
str3 = '0，5000KW(Nm)（N.m）,60-100nm'
str4 = '0.55kw，0.75kw，1.5Kw'

print(handle_value(str1))
print(handle_value(str2))
print(handle_value(str3))
print(handle_value(str4))
