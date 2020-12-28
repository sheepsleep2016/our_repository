import csv
import decimal

dec = decimal.Decimal("%.6f" % float(3.1567))
# print(type(dec))


def reader(path):
    csv_file = csv.reader(open(path,'r'))

    list_type = next(csv_file)
    list_user = []
    list_commodity =[]

    for line in csv_file:
        dict_user = {}
        dict_commodity = {}
        dict_user["user_name"]=line[0]
        dict_user['user_email']=line[1]
        dict_user['user_pwd']=line[2]
        dict_user['user_idcard_num']=line[3]
        dict_user['phonenum']=line[4]
        dict_user['isActive']=bool(line[5])
        dict_commodity['commodity_name']=line[6]
        dict_commodity['commodity_discrib']=line[7]
        dict_commodity['commodity_position']=line[8]
        dict_commodity['commodity_price'] =line[9]
        dict_commodity['commodity_date']=line[10]
        dict_commodity['commodity_type']=line[11]
        dict_commodity['commodity_count']=line[12]
        list_user.append(dict_user)
        list_commodity.append(dict_commodity)

    return list_user,list_commodity

list_user,list_commodity = reader('无标题文档 (复件).csv')
print(list_user[0])
print(list_commodity[0])



