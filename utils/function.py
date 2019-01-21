
import random
import time


def get_order_sn():
    # 获取订单号，保证唯一
    s = '12357890qwertuiopasdgjklZxcbnmQWEOASLOZBM'
    order_sn = ''
    for i in range(20):
        order_sn += random.choice(s)
    order_sn += str(time.time())
    return order_sn