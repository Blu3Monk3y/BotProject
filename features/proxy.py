from random import randint

https_proxy_list = [
    { "ip" : "163.172.35.121", "port" : 8088, "country" : "FR"},
    { "ip" : "178.18.245.74", "port" : 8888, "country" : "GER"},
    { "ip" : "101.99.95.54", "port" : 80, "country" : "ML"},
]

def randomHttps():
    proxy = https_proxy_list[randint(0, len(https_proxy_list) - 1)]
    return proxy['ip'], proxy['port'], proxy['country']