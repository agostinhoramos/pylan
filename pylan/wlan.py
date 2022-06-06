from subprocess import check_output
import os, time, re, socket, urllib.request, subprocess, json

# WARNING: Run as admin

def _cmd_output(proc=None, output=None):
    out=None
    if proc:
        out, err = proc.communicate()
        out = out.decode('ascii')
        out = out.replace("\r","").replace("\n","")
    if output:
        out = output.decode('ascii')
        out = out.replace("\r","").replace("\n","")
    return out

class Wlan:
    def __init__(self, *args, **kwargs):
        self.ROOT_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        self.country = "PT"
        self.fRefex = self.readJSON("debian_gnu_linux_en")

    def readJSON(self, name):
        f = open(self.ROOT_DIR + '/pylan/json/{}.json'.format(name))
        return json.load(f)

    def getWiList(self, interface):
        proc1 = subprocess.Popen(['sudo', 'iwlist', interface, "scan"], stdout=subprocess.PIPE)
        proc2 = subprocess.Popen(['egrep', self.fRefex["main_regex"]], stdin=proc1.stdout,
                                        stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        list_cell = self.fRefex["regex"]
        output, err = proc2.communicate()
        out = output.decode('ascii')
        group_id=0
        
        data = []
        obj = {"ssid": None}
        for split in out.split('\n'):
            split=split.strip()
            if split:
                for cell in list_cell:
                    if re.search(cell["re"]["l"], split):
                        
                        attr = cell["lb"].strip()
                        value = split.split(cell["re"]["l"])[1]
                        arg = cell["re"]["r"]
                        if arg:
                            value = value.split(arg)[0]
                        value = value.strip()

                        obj.update({attr: value})

                if re.search(r'Cell [0-9]+ -', split):
                    group_id=group_id+1
                    data.append(obj)
                    obj = {"ssid": None}

        nj = []
        for dd in data:
            jn = {}
            for attr, value in dd.items():
                if attr == 'id':
                    jn.update({attr: int(value)})
                elif attr == 'frequency':
                    jn.update({attr: float(value)})
                elif attr == 'signal':
                    jn.update({attr: int(value)})
                elif attr == 'channel':
                    jn.update({attr: int(value)})
                elif attr == 'quality':
                    n = value.split("/")
                    r = int(n[1]) - int(n[0])
                    jn.update({attr: r})
                elif attr == 'encryption':
                    boo = False
                    if value == 'on':
                        boo = True
                    jn.update({attr: boo})
                elif attr == 'security' or attr == 'mode':
                    jn.update({attr: value.lower()})
                else:
                    jn.update({attr: value})

            nj.append(jn)

        proc1.stdout.close()
        return nj

    def setAccessPoint(self, wlanSSID, wlanPASS, secLevel, wlanNetwork, wlan, country=None):
        if country == None:
            country=self.country
        FILE=self.ROOT_DIR + '/pylan/shell/ap_conf.sh'
        out = check_output(['sudo', FILE, wlanSSID, wlanPASS, secLevel, wlanNetwork, wlan, country])
        out = _cmd_output(output=out)
        if out == 1:
            return True
        return False
    
    def setWlanReceiver(self, wlanSSID, wlanPASS, keyMGMT, wlan, country=None):
        if country == None:
            country=self.country
        FILE=self.ROOT_DIR + '/pylan/shell/wl_conf.sh'
        out = check_output(['sudo', FILE, wlanSSID, wlanPASS, keyMGMT, wlan, country])
        out = _cmd_output(output=out)
        if out == 1:
            return True
        return False

    def restartConfig(self):
        return True