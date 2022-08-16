''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''
#作者：cacho_37967865
#博客：https://blog.csdn.net/sinat_37967865
#文件：pymysqlModel.py
#日期：2018-10-22
#备注：pip install pymysql  pymysql是Python中操作MySQL的模块   F:\python_env\PaChong_env
'''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''
import xlrd
import xlwt
from xlutils.copy import copy
import pandas as pd
import datetime

sample_file = '发票模板.xls'


# 发票模板：需要修改的地方（动态）
def invoice():
    data = xlrd.open_workbook(sample_file)
    table = data.sheets()[0]
    in_no = table.cell_value(2, 1)
    in_dt = table.cell_value(2, 8)
    in_cpy = table.cell_value(4, 6)
    in_add = table.cell_value(5, 6)
    in_post = table.cell_value(6, 6)
    in_cty = table.cell_value(7, 6)
    in_country = table.cell_value(8, 6)
    in_con = table.cell_value(10, 6)
    in_phno = table.cell_value(11, 6)


def get_excel_data():
    order_no = input('请输入订单号：')
    sheet_name = input('请输入sheet名')
    data = pd.read_excel('客户跟进情况.xlsx', sheet_name=sheet_name)
    # data['订单号'][0]
    data1 = data[data['订单号'] == order_no]

    name = data1['全名'].tolist()[0]
    in_add = data1['地址'].tolist()[0]
    in_cty = data1['城市'].tolist()[0]
    in_post = str(data1['邮编'].tolist()[0])
    in_phno = data1['电话'].tolist()[0]
    # in_country='United States'
    in_dt = datetime.date.today().strftime('%Y/%m/%d')
    return order_no, name, in_add, in_cty, in_post, in_phno, in_dt


# TypeError: descriptor 'decode' requires a 'bytes' object but received a 'NoneType'
# F:\python_env\PaChong_env\lib\site-packages\\xlwt\UnicodeUtils.py
def make_excel():
    s = get_excel_data()
    invoice_no = s[0] + '-LG'
    # width = 256 * 8
    font = xlwt.Font()
    font.height = 240  # 12号字体
    font.bold = False
    font.name = 'Arial'
    align = xlwt.Alignment()
    style = xlwt.XFStyle()
    style.font = font
    align.vert = 0
    style.alignment = align
    inv = invoice_no + '发票.xls'
    data = xlrd.open_workbook(sample_file, formatting_info=True)
    new_excel = copy(data)
    ws = new_excel.get_sheet(0)  # 获取第一个sheet
    # first_col = ws.col(0)            # 第一列
    # first_col.width=width            # 第一列宽
    ws.write(2, 1, invoice_no, style)
    ws.write(2, 3, invoice_no, style)  # B8(7,1)
    ws.write(4, 6, s[1], style)  # F9(8,5)
    ws.write(2, 8, s[-1], style)
    ws.write(10, 6, s[1], style)
    ws.write(5, 6, s[2], style)
    ws.write(7, 6, s[3], style)
    ws.write(6, 6, s[4], style)
    ws.write(11, 6, s[5], style)
    new_excel.save(inv)


if __name__ == '__main__':
    make_excel()
