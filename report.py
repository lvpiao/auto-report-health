# encoding:utf-8
import sys
import main
import db

if __name__ == '__main__':
    usr = sys.argv[1]
    pwd = sys.argv[2]
    res = main.autoReport((usr, pwd, None))
    print(res)     
    # print(db.alluser())



