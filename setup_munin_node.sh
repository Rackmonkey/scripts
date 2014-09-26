#!/bin/bash
#
# written by David Bauer, initial start 17.09.2014
# 
# Status: Sollte funzen

aptitude -y update 1>/dev/null
aptitude install munin-node

echo " " >> /etc/munin/munin-node.conf
echo " " >> /etc/munin/munin-node.conf
echo "# ==================================================" >> /etc/munin/munin-node.conf
echo "# Automatisch hinzugefügt durch setup_munin_node.sh" >> /etc/munin/munin-node.conf
echo "# https://github.com/rackmonkey/scripts" >> /etc/munin/munin-node.conf
echo "# ==================================================" >> /etc/munin/munin-node.conf
echo " " >> /etc/munin/munin-node.conf
echo " " >> /etc/munin/munin-node.conf
echo "# Rackmonkey Monitoring Server monitor01.rackmonkey.de " >> /etc/munin/munin-node.conf
echo "allow ^88\.198\.253\.10$" >> /etc/munin/munin-node.conf

/etc/init.d/munin-node restart