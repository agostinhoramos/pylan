from pylan.wlan import Wlan

wlan = Wlan()

# r = wlan.getIWList('wlan0')
# print( r )

wlan.restartConfig('wlan0')

# wlan.setAccessPoint(
#     wlanSSID="WiFi Brave",
#     wlanPASS="ngueTela",
#     secLevel="1",
#     wlanNetwork="192.168.65.1",
#     wlan="wlan0"

# )

# wlan.setWlanReceiver(
#     wlanSSID="CASA RAMOS",
#     wlanPASS="ngueTela",
#     keyMGMT="WPA-PSK",
#     wlan="wlan1"
# )