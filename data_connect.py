import pymysql
def db_connect():
    db=pymysql.connect(host="localhost", #默认用主机名
    port=3305,
    user="root",  #默认用户名
    password="87885471",   #mysql密码
    database='amazon', #库名
    charset='utf8'   #编码方式
    )
    cursor =db.cursor()
    cursor.execute("SELECT VERSION()")
    data =cursor.fetchone()
    print(f"database version:{data}")
def create_table():
    db = pymysql.connect(host="localhost", #默认用主机名
    port=3305,
    user="root",  #默认用户名
    password="87885471",   #mysql密码
    database='amazon', #库名
    charset='utf8'   #编码方式
    )
    cursor = db.cursor()
    cursor.execute("DROP TABLE IF EXISTS TEST_TABLE")
    sql="""CREATE TABLE TEST_TABLE(
     id int,
     日期 DATE,
     order_id varchar(25),
     sku varchar(20),
     quantity int,city varchar(20),
     state varchar(5),
     postal varchar(15),
     sales decimal(10.2),
     tax_in decimal(10.2),
     ship_credit decimal(10.2),
     ship_credit_tax decimal(10.2),
     gift_cradit decimal(10.2),
     gift_credit_tax decimal(10.2),
     regulatory_fee decimal(10.2),
     promot_rebates decimal(10.2),
     promot_rebates_tax decimal(10.2),
     tax_out decimal(10.2),
     selling_fee decimal(10.2),
     fba_fee decimal(10.2),
     trans_fee decimal(10.2),
     other_fee decimal(10.2),
     total decimal(10.2)
     )"""
    try:
        cursor.execute(sql)
        print("CREATE TABLE SUCCESS")
    except Exception as e:
        print(f"CREATE TABLE FAILED,CASE:{e}")
    finally:
        db.close()
def main():
    db_connect()
    create_table()
if __name__=="__main__":
    main()