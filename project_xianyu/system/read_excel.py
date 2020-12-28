#导入xlrd模块
import xlrd
from datetime import datetime

class ExcelData():
    def __init__(self,data_path,sheetname='Sheet1'):
        self.data_path = data_path                                 # excle表格路径，需传入绝对路径
        self.sheetname = sheetname                                 # excle表格内sheet名
        self.data = xlrd.open_workbook(self.data_path)             # 打开excel表格
        self.table = self.data.sheet_by_name(self.sheetname)       # 切换到相应sheet
        self.keys = self.table.row_values(0)                       # 第一行作为key值
        self.rowNum = self.table.nrows                             # 获取表格行数
        self.colNum = self.table.ncols                             # 获取表格列数
        # print(self.rowNum)
        # print(self.colNum)

    def readExcel(self):
        if self.rowNum<2:
            print("excle内数据行数小于2")
        else:
            list_user = []                                         #列表存放取出的user数据
            list_commodity = []                                    #列表存放取出的commodity数据
            list_username = []
            for i in range(1,self.rowNum):                         #从第二行（数据行）开始取数据
                # 定义字典用来存放对应数据
                dictuser = {}
                dictcommodity = {}
                if self.table.row_values(i)[0] not in list_username:
                    list_username.append(self.table.row_values(i)[0])

                    # j对应列值
                    for j in range(self.colNum):
                        if j <=5 :
                            if self.table.row_values(i)[0] not in list_username:
                                list_username.append(self.table.row_values(i)[0])
                                continue
                            # 把第i行第j列的值取出赋给第j列的键值，构成user字典
                            if j == 4:
                                dictuser[self.keys[j]] = str(int(self.table.row_values(i)[j]))
                                # print(str(int(self.table.row_values(i)[j])))
                            else:
                                dictuser[self.keys[j]] = self.table.row_values(i)[j]

                        else:
                            # 取商品相关的值
                            if self.keys[j]=="commodity_count":
                                dictcommodity[self.keys[j]] = int(self.table.row_values(i)[j])
                            elif self.keys[j] == "commodity_date":
                                dictcommodity[self.keys[j]] = datetime.strptime(self.table.row_values(i)[j],
                                                                            '%Y-%m-%d %H:%M:%S')
                                # print(datetime.strptime(self.table.row_values(i)[j], '%Y-%m-%d %H:%M:%S'))
                            else:
                                dictcommodity[self.keys[j]] = self.table.row_values(i)[j]
                    # 一行值取完之后，追加到相应的列表中
                        dictcommodity["user_id"] = list_username.index(self.table.row_values(i)[0])+79
                    list_commodity.append(dictcommodity)
                    list_user.append(dictuser)
                else:
                    for j in range(6,self.colNum):
                        # 取商品相关的值
                        if self.keys[j] == "commodity_count":
                            dictcommodity[self.keys[j]] = int(self.table.row_values(i)[j])
                        elif self.keys[j] == "commodity_date":
                            dictcommodity[self.keys[j]] = datetime.strptime(self.table.row_values(i)[j], '%Y-%m-%d %H:%M:%S')
                            # print(datetime.strptime(self.table.row_values(i)[j], '%Y-%m-%d %H:%M:%S'))
                        else:
                            dictcommodity[self.keys[j]] = self.table.row_values(i)[j]
                        dictcommodity['user_id'] = list_username.index(self.table.row_values(i)[0])+79
                    # 一行值取完之后，追加到相应的列表中
                    list_commodity.append(dictcommodity)

            return list_user,list_commodity

if __name__ == '__main__':
    data_path = "/home/tarena/虚拟用户 - 副本.xls"
    get_data= ExcelData(data_path,sheetname="Sheet5")
    get_user,get_comm = get_data.readExcel()
    for i in get_user:
        print(i)  #['user_name']
    for i in get_comm:
        print(i)
    # print(len(get_user))
    # print(len(get_comm))