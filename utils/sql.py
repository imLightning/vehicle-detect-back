import pymysql

# 连接
def get_connection():
    con = None
    try:
        con = pymysql.connect(host="localhost", user="root", password="1234", database="vehicle")
    except Exception as e:
        print(e)
    return con

# 关闭
def close(con, cur):
    if cur is not None:
        cur.close()
    if con is not None:
        con.close()

# 选择
def select(sql, *params):
    con = get_connection()
    cur = con.cursor()
    try:
        cur.execute(sql, *params)
        result = cur.fetchone()
        con.commit()
        return result
    except Exception as e:
        print(f"错误:{e}")
        con.rollback()
    finally:
        close(con, cur)

# 更新
def update(sql, *params):
    con = get_connection()
    cur = con.cursor()
    try:
        cur.execute(sql, *params)
        con.commit()
        return cur.rowcount
    except Exception as e:
        print(f"错误:{e}")
        con.rollback()
    finally:
        if cur is not None:
            cur.close()
        if con is not None:
            con.close()

# 插入
def insert(sql, *params):
    update(sql, *params)

# 删除
def delete(sql, *params):
    update(sql, *params)
