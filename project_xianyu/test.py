#!/usr/bin/env python2.7
# -*- coding:UTF-8 -*-

# import paramiko,os,sys
#
# ip = "10.67.19.186" #raw_input("input ip address :>>>")
# password = "nsf0cus.JF2Z"#raw_input("input password:>>>")
# cmd = "pwd " #raw_input("input your cmd:>>> ")
#
# print('''
# ------connecting to %s ,--------
# '''%ip)
# def ssh_cmd(ip,port,cmd,user,passwd):
#     result = ""
#     try:
#         ssh = paramiko.SSHClient()
#         ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
#         ssh.connect(ip,port,user,passwd)
#         stdin, stdout, stderr = ssh.exec_command(cmd)
#         result = stdout.read()
#         print (result)
#         ssh.close()
#     except:
#         print ("ssh_cmd err.")
#     return result

# pg库中生成的事件字段以及部分外发字段映射关系
pg_event_map = {'start_time': 'create_time',  # 日志发生时间
                'dst_city': 'dst_city',  # 目的IP地址所属市
                'dst_country': 'dst_country',  # 目的IP地址所属国家
                'dip': 'dst_ip',  # 目的IP地址
                'dst_province': 'dst_province',  # 目的IP地址所属省份
                'sequence_id': 'id',  # 事件ID
                'priority': 'severity',  # 威胁等级
                'src_city': 'src_city',  # 来源IP地址所属市
                'src_country': 'src_country',  # 来源IP地址所属国家
                'sip': 'src_ip',  # 来源IP地址
                'src_province': 'src_province',  # 来源IP地址所属省份
                'event_type': 'event_type',  # 事件类型
                'name': 'event_name',  # 事件名称
                'rule_id': 'rule_name',  # 规则名称
                'description': 'event_description',  # 事件详细描述
                }
# pg关联事件的映射
pg_related_event_map = {
    'related_id_list': 'related_id_list'  # 通过event视图关联各个事件
}
# 事件视图字段
event_data = [(k, v) for k, v in pg_event_map.items() if v]
# 关联的字段
related_data = [(k, v) for k, v in pg_related_event_map.items() if v]
# 查询的字段
event_columns = [i[0] for i in event_data]
related_columns = [i[0] for i in related_data]

columns = [event_columns, related_columns]  # 事件表 + 关联表字段
print(columns)
event_columns = columns[0]
related_columns = columns[1]

columns = list(map(lambda x: "e.{}".format(x), event_columns)) + list(
    map(lambda x: "et.{}".format(x), related_columns))
print(columns)

print({'related_id_list': '{}#{}'.format(['related_id_list'],['related_id_list'])})

hive_wss_arplog_map = {
    'dev_ip': 'dev_ip',
    'dev_id': 'dev_id',
    'msgtype': 'msgtype',
    'product': 'product',
    'action': 'action',
    'alertlevel': 'alertlevel',
    'attack_type': 'attack_type',
    'conflit_mac': 'conflit_mac',
    'count_num': 'count_num',
    'def_ip': 'def_ip',
    'def_ip_int': 'def_ip_int',
    'def_mac': 'def_mac',
    'dip': 'dip',
    'dip_int': 'dip_int',
    'dmac': 'dmac',
    'event_type': 'event_type',
    'sip': 'sip',
    'sip_int': 'sip_int',
    'smac': 'smac',
    'timestamp': 'timestamp',
    'status': 'status',
    'probe_id': 'probe_id',
    'log_id': 'log_id'
}
print(",".join([i  for i in hive_wss_arplog_map ]))

s = "  raw_data  | ns_hour  | log_type  |  timestamp  |  recv_time  | vender  | pversion  |    ds_id     | platform_id  | platform_gid  | collector_id  | product  |    dev_ip    |                log_id                 |      sip       | sport  |      dip       | dport  | proto  |             msg              |        dmac        | user_name  |        smac        | gr_pop  | type  |                                    ds                                     | vid  | last_times  | gr_type  | gr_os  | action  | gr_danger  |                                                                                                                                                                                                                                                                                                                                                                                                                                                           raw_info                                                                                                                                                                                                                                                                                                                                                                                                                                                            | msgtype  | app_id  | module  | ar  | gr_tech  | app_name  | acted  | gr_service  | raw_len  | rule_id  | card  | msel  |                  snapshot                  |       log_date       |  sip_int   |  dip_int   | src_asset  | dst_asset  |        dev_id        |       probe_id       |  ns_date  "
list00 = ["           | 14       | 1009      | 1587709791  | 1587714277  |         |           | ips_tac_log  |              |               |               | ips      | 10.67.1.135  | e0e46b0d-1daa-44b3-9a72-0ee4ce9ff80d  | 36.192.108.63  | 1165   | 42.83.131.241  | 80     | -1     | TROJ_CRYPTESLA.XXRH恶意勒索木马通信  | D8:24:BD:89:78:C8  |            | 08:00:27:74:A2:27  | 3       | NULL  | SFRUUG5TZjBDdXNDTElFTlRuU2YwQ3VzVVJMPS93cC1jb250ZW50L3RoZW1lcy9yLnBocD8=  | 0    | 79          | 4        | 1      | 2       | 3          | 2CS9iXjICAAndKInCABFAAKOxLNAAIAGl7MKCDsBldLBJwSNAFA140+9AArnrFAY//9g0gAAR0VUIC93cC1jb250ZW50L3RoZW1lcy9yLnBocD9EMEIxNzQ1MTg0RDRCMTkzMjVGOENBMjM5RDc4RTgwNDZFMjkwNjc2QjJFMDZBN0VCM0I0ODM4OUYzOUEyMEI1NzkxNUJFQTFFRjNCNDZDOUJFODZDMzJBQTZDQTlBRjBDNDRBQTAxNkVCRDdDQ0ZCRjk2RUU2NTFGMUMxQjkxNkM3NUNFMThCRTMyQkU5NEVDQUFFRDY5QTRGMzEwRDUzNThBMEJBNkMyMjREMkNGNDAwQjY5Q0JBRTJGMDg2OUFGNDA5MEMwQTFGNTAxRDlDRjhCMTBCRjEyN0Q1MDJDNDA4NjhCNUI5NjQ0M0M2QTRFOUVCRDk2OTY5OThCMUVEQkQ2OTg5MzFBODhENTZGQTg3OUMzMDcyNTREQkE5N0I5QjBERkI2QkZDNkU5RTk3QkUzNzk3QTJCQzZEOUY4N0FBRURDQTAxNzVFQzE2QUQxMzYwQUIyODRDMDlFNThDOTA3NjVFNjc3MEEwQzBFNTM3RDJFOTk1MEU3QkU3MTYwMEUyQ0VGMkJEMkUwNjBFNjc2ODM2M0VFRDVBMTQ1QjI4REE2Rjg5QkQyMDVBQ0U2NDFFMDA2NDdENzVFNURFIEhUVFAvMS4xDQpVc2VyLUFnZW50OiBNb3ppbGxhLzUuMCAoV2luZG93cyBOVCA2LjE7IHJ2OjMxLjApIEdlY2tvLzIwMTAwMTAxIEZpcmVmb3gvMzEuMA0KSG9zdDogbGVkc2hvcHBlbi5ubA0KQ29ubmVjdGlvbjogS2VlcC1BbGl2ZQ0KDQo=  | 30721    | NULL    | 0       | 2   | 32       | NULL      | 2      | 1           | 892      | 41226    | G1/1  | 0     | HTTP CLIENT URL=/wp-content/themes/r.php?  | 2020-04-24 14:29:51  | 616590399  | 710116337  | 0          | 0          | 87AE-1EB2-0228-2087  | 87AE-1EB2-0228-2087  | 20200424  | |           | 14       | 1009      | 1587709793  | 1587714277  |         |           | ips_tac_log  |              |               |               | ips      |              | 1ec5790f-1046-49d1-aaea-51159b6a17da  | 36.192.108.61  | 3306   | 42.83.131.240  | 445    | -1     | IMAP服务用户认证成功                 | 00:E0:4C:0B:92:E1  |            | E8:40:40:97:C3:C1  | 2       | NULL  | SU1BUG5TZjBDdXNT                                                          | 0    | 75          | 5        | 3      | 0       | 1          | AAAAm/9TTUJyAAAAABhTyAAAAAAAAAAAAAAAAP////4AAAAAAHgAAlBDIE5FVFdPUksgUFJPR1JBTSAxLjAAAkxBTk1BTjEuMAACV2luZG93cyBmb3IgV29ya2dyb3VwcyAzLjFhAAJMTTEuMlgwMDIAAkxBTk1BTjIuMQACTlQgTE0gMC4xMgACU01CIDIuMDAyAAJTTUIgMi4/Pz8A                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                          | 1        | NULL    | 0       | 2   | 512      | NULL      | 3      | 9           | 212      | 50036    | G1/6  | 0     | IMAP S                                     | 2020-04-24 14:29:53  | 616590397  | 710116336  |            |            | 1FF6-FBE0-39CF-185C  | 1FF6-FBE0-39CF-185C  | 20200424 "]
dict(zip([i.strip() for i in s.split("|")],[i.strip() for i in list00[0].split("|")]))
for k,v in dict(zip([i.strip() for i in s.split("|")],[i.strip() for i in list00[0].split("|")])).items():
    print(k+": "+v)

ss = " app_id | event_id | rule_id |     name     |         description          | event_type_major | event_type | stage |         suggestion         |      sip      |   dip   | priority | reliability | occurrence | start_time |  end_time  | related_info |             sequence_id              | state | src_country | src_province | src_city | src_area | dst_country | dst_province | dst_city | dst_area | action | result | probe_id | platform_hash "
print([i.strip() for i in ss.split("|")])

class Demo(object):
    def __init__(self,a):
        self.a = a
        if type(a) != 'int':
            print('TYPE ERROR')

    def add(self,b):
        print(self.a+b)

getattr(Demo(33),'add')(66)

class EventData(object):
    def __init__(self,log_id,status,event_table):
        self.sequence_id = log_id
        self.status = status
        self.event_table = event_table

    def get_event_data(self):
        columns_map = {
            "internal_app_bsackc.event":[("start_time","suggestion"),'sequence_id'],
            "internal_app_bsaata.nta_t_event":[("start_timestamp",),'id'],
        }

        if self.status == 3:
            sql = """select {columns} from {db} where {id}='{value}'""".format(
                columns = ','.join(columns_map[self.event_table][0]),
                db=self.event_table,
                id=columns_map[self.event_table][-1],
                value=self.sequence_id)
            print(sql)
            event_datas = [[158666685]]
            data_dict = dict(zip(columns_map[self.event_table][0],event_datas[0]))
            print(data_dict)

DE = EventData('asdlio-awfw123-asd32r2rf',3,'internal_app_bsackc.event')
DE0 = EventData('asdlio-awfw123-asd32r2rf',3,'internal_app_bsaata.nta_t_event')
DE.get_event_data()
DE0.get_event_data()

hive_column_map = {
    # 网站安全hive库字段映射wss
    'internal_app_bsawss.waf_webseclog': 1,
    'internal_app_bsawss.waf_arplog': 2,
    'internal_app_bsawss.waf_ddoslog': 3,
    'internal_app_bsawss.waf_defacelog': 4,
    'internal_app_bsawss.waf_reputation': 5,

    # 网络入侵hive库字段映射ckc
    'internal_app_bsaips.ipslog': 6}

ss = """
select action,'{db}' as db_name from {db}
"""
sql = 'UNION ALL '.join([ss.format(db=i) for i in hive_column_map.keys()])
print(sql)

def testtt(a):
    b = a / 5
    if not b:
        pass
    else:
        print(b)
    print('这是一个测试')

"""
1.联调提测+ 修改整体样式  100%   --王琛
2.联调自测,修复bug  --吴狄
3.联调，打包提测  --查凯进
4.核对API文档，深入了解各种请求接口实现的代码及规范 --肖超雄
5.大屏样式调整-- 冯叶青
1.部署测试环境，安装app,本轮提测内容接收测试  --张雷"""
