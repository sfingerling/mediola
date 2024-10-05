import requests

class Mediola:
    _intertechno = {
            'ON' : 0x10,
            'OFF' : 0x00
            }

    _warema = {
            'UP' : 0x741C000001,
            'OPEN' : 0x741C000001,
            'STEPUP' : 0x741C000000,
            'STOP' : 0x3404000000,
            'STEPDOWN' : 0x7418000000,
            'DOWN' : 0x7418000001,
            'CLOSE' : 0x7418000001
            }
    _somfy = {
            'UP' : '20',
            'OPEN' : '20',
            'STOP' : '10',
            'DOWN' : '40',
            'CLOSE' : '40',
            'LEARN' : '60'
            }
    def __init__(self, host, port=80):
        self.host = host
        self.port = port

    def send(self, parameter):
        url = "http://{}:{}/command".format(self.host, self.port)
        r = requests.get(url, params=parameter)

    def send_intertechno(self, device, action):
        data = int(device, 16)
        data += self._intertechno.get(action, 0)
        data = format(data, 'X')
        para = {'XC_FNC':'SendSC', 'type':'IT', 'data': data}
        self.send(para)

    def send_warema(self, device, action):
        data = int(device+"00", 16)
        data += self._warema.get(action, 0)
        data = format(data, 'X')
        para = {'XC_FNC':'SendSC', 'type':'WA', 'data': data}
        self.send(para)

    def send_send2(self, code):
        para = {'XC_FNC':'Send2', 'code': code}
        self.send(para)

    def send_somfy(self, device, action):
        data = self._somfy.get(action, '00') + device
        print(data)
        para = {'XC_FNC':'SendSC', 'type':'RT', 'data': data}
        self.send(para)

if __name__ == '__main__':
    m = Mediola('192.168.178.8')
    #m.send_intertechno('56C82181', 'OFF')
    #m.send_warema('C00A85', 'UP')
    m.send_send2('190800810005001903009C003D002D00A4002D064000000100010001010000010000000100010100000101010102')
