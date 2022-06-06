#!/bin/bash

WLAN="$1"
wpconf="/etc/wpa_supplicant/wpa_supplicant-$WLAN.conf"
wlan_network="/etc/systemd/network/*-$WLAN.network"

rm -rf $wpconf $wlan_network
systemctl unmask networking.service dhcpcd.service
mv /etc/network/{interfaces~,interfaces} # restore file
systemctl disable systemd-networkd.service systemd-resolved.service wpa_supplicant@$WLAN.service
systemctl enable wpa_supplicant.service
rm -rf /etc/resolv.conf
cp /etc/{resolv.conf~,resolv.conf}

sudo systemctl restart systemd-networkd.service
sudo systemctl restart wpa_supplicant.service

echo "1"