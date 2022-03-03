from threading import Thread
from . import proxy
from . import user_agent



class numThreadTest(Thread):
    
    def run(self):
            ip, port, country = proxy.randomHttps()
        
            print(
        f"""
        PROXY CONFIGURATION FOR THIS TASK
        Ip Address: {ip}
        Port: {port}
        Country: {country}
        Current thread: {self.name}
        Execute on number: {self.number}
        """)
            return

    def __init__(self, name, number):
        self.th = Thread(target=self.run, name=name, daemon=True)





