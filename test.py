'''
该源程序用于生成测试用例
'''

import string
import random
import sys
from checkLE import check

# 所有大写字母
s = string.ascii_uppercase


def random_mini_exp():
    # 随机选择 二元运算符或者一元运算符
    if random.randint(0, 1) == 0:
        return "~" + random.choice(s)
    else:
        # 随机二元运算符
        return random.choice(s) + ["|", "&"][random.randint(0, 1)] + random.choice(s)


def random_exp(max_deep):
    # 递归生成表达式 max_deep是最大深度
    # 随机值成立或者达到最大深度截止
    if random.randint(0, 9) < 3 or max_deep == 0:
        return random_mini_exp()
    # 递归生成
    if random.randint(0, 1) == 0:
        return "~" + random_exp(max_deep - 1)
    else:
        # 随机二元运算符
        return "(%s)%s(%s)" % (random_exp(max_deep - 1), ["|", "&"][random.randint(0, 1)], random_exp(max_deep - 1))


if __name__ == "__main__":
    count = 1000
    max_deep = 6
    if len(sys.argv) == 3:
        count = int(sys.argv[1])
        max_deep = int(sys.argv[2])
    for i in range(count):
        print(check(random_exp(random.randint(0, max_deep))))
