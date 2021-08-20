#!/usr/bin/python3
#-*- coding: utf-8 -*-

import os
from terminaltables import DoubleTable
from tabulate import tabulate
import sys, traceback
from time import sleep
import sys

def main():

    try:

        #Configure the network interface and gateway.
        def config0():

            global up_interface
            up_interface = open('tools/files/iface.txt', 'r').read()
            up_interface = up_interface.replace("\n","")
            if up_interface == "0":
                up_interface = os.popen("route | awk '/Iface/{getline; print $8}'").read()
                up_interface = up_interface.replace("\n","")

            global gateway
            gateway = open('tools/files/gateway.txt', 'r').read()
            gateway = gateway.replace("\n","")
            if gateway == "0":
                gateway = os.popen("ip route show | grep -i 'default via'| awk '{print $3 }'").read()
                gateway = gateway.replace("\n","")

        def home():
            config0()
            n_name = os.popen('iwgetid -r').read() # Get wireless network name
            n_mac = os.popen("ip addr | grep 'state UP' -A1 | tail -n1 | awk '{print $2}' | cut -f1  -d'/'").read() # Get network mac
            n_ip = os.popen("hostname -I").read() # Local IP address
            n_host = os.popen("hostname").read() # hostname

            # Show a random banner. Configured in banner.py .
            
            print("""\033[1;33m[+]═══════════[ Author : @shakarr\033[1;m \033[1;36m_-\|/-_\033[1;m \033[1;33mWebsite: shakarr.github.io ]═══════════[+]\033[1;m""")

            # Print network configuration , using tabulate.

            print("""\033[0;35m
┌═════════════════════════════════════════════════════════════════════════════┐
█                                                                             █
█                         Your Network Configuration                          █
█                                                                             █
└═════════════════════════════════════════════════════════════════════════════┘\n \033[1;m""")

            table = [["IP Address","MAC Address","Gateway","Iface","Hostname"],
            ["","","","",""],
            [n_ip,n_mac.upper(),gateway,up_interface,n_host]]
            print (tabulate(table, stralign="center",tablefmt="fancy_grid",headers="firstrow"))
            print ("")

        def scan():
            config0()

            scan = os.popen("nmap " + gateway + "/24 -n -sP").read()

            f = open('tools/log/scan.txt','w')
            f.write(scan)
            f.close()

            devices = os.popen("grep report tools/log/scan.txt | awk '{print $5}'").read()
            devices_mac = os.popen("grep MAC tools/log/scan.txt | awk '{print $3}'").read() + os.popen("ip addr | grep 'state UP' -A1 | tail -n1 | awk '{print $2}' | cut -f1  -d'/'").read().upper() # get devices mac and localhost mac address
            devices_name = os.popen("grep MAC tools/log/scan.txt | awk '{print $4 ,S$5 $6}'").read() + "\033[1;32m(This device)\033[1;m"

            table_data = [
                ['IP Address', 'Mac Address', 'Manufacturer'],
                [devices, devices_mac, devices_name]
            ]
            table = DoubleTable(table_data)

            #show devices found on your Network
            print("\033[1;36m[+]═══════════[ Devices found on your network ]═══════════[+]\n\033[1;m")
            print(table.table)
            

                     

        def cmd0():
            while True:
                print("\033[1;32m\n[+] Please type 'help' to view commands.\n\033[1;m")
                cmd_0 = input("\033[1;36m\033[4mSCANNER\033[0m\033[1;36m ➮ \033[1;m").strip()
                if cmd_0 == "scan": # Map the network
                    print("\033[1;34m\n[++] Mapping your network ... \n\033[1;m")
                    scan()
                elif cmd_0 == "gateway": # Change gateway
                    def gateway():
                        print("")
                        table_datas = [
                            ["\nInformation\n", "\nManually set your gateway.\nInsert '0' if you want to choose your default network gateway.\n"]
                        ]
                        table = DoubleTable(table_datas)
                        print(table.table)
                        print("\033[1;32m\n[+] Enter your network gateway.\n\033[1;m")
                        n_gateway = input("\033[1;36m\033[4mSCANNER\033[0m»\033[1;36m\033[4mgateway\033[0m\033[1;36m ➮ \033[1;m").strip()

                        if n_gateway == "back":
                            home()
                        elif n_gateway == "exit":
                            os.system("clear")
                            sys.exit()
                        elif n_gateway == "home":
                            os.system('clear')
                            home()
                        else:
                            s_gateway = open('/tools/files/gateway.txt','w')
                            s_gateway.write(n_gateway)
                            s_gateway.close()

                            home()
                    gateway()

                

                elif cmd_0 == "iface": # Change network interface.
                    def iface():
                        print ("")
                        table_datas = [
                            ["\nInformation\n", "\nManually set your network interface.\nInsert '0' if you want to choose your default network interface.\n"]
                        ]
                        table = DoubleTable(table_datas)
                        print(table.table)

                        print("\033[1;32m\n[+] Enter your network interface.\n\033[1;m")
                        n_up_interface = input("\033[1;36m\033[4mSCANNER\033[0m»\033[1;36m\033[4miface\033[0m\033[1;36m ➮ \033[1;m").strip()

                        if n_up_interface == "back":
                            home()
                        elif n_up_interface == "exit":
                            os.system("clear")
                            sys.exit()
                        elif n_up_interface == "home":
                            os.system('clear')
                            home()
                        else:
                            s_up_interface = open('tools/files/iface.txt','w')
                            s_up_interface.write(n_up_interface)
                            s_up_interface.close()

                            home()

                    iface()

                elif cmd_0 == "rmlog": # Remove all logs
                    def rm_log():
                        print("\033[1;32m\n[+] Do want to remove all logs ? (y/n)\n\033[1;m")
                        cmd_rmlog = input("\033[1;36m\033[4mSCANNER\033[0m»\033[1;36m\033[4mrmlog\033[0m\033[1;36m ➮ \033[1;m").strip()
                        if cmd_rmlog == "y":
                            os.system("rm -f -R tools/log/*")
                            print("\033[1;31m\n[++] All logs have been removed. \n\033[1;m")
                            sleep(1)
                            os.system("clear")
                            home()
                        elif cmd_rmlog == "n":
                            home()
                        elif cmd_rmlog == "exit":
                            os.system("clear")
                            sys.exit()
                        elif cmd_rmlog == "home":
                            os.system('clear')
                            home()
                        elif cmd_rmlog == "back":
                            home()
                        else:
                            print("\033[1;91m\n[!] Error : Command not found. type 'y' or 'n'\033[1;m")
                            rm_log()

                    rm_log()


                elif cmd_0 == "exit":
                    os.system("clear")
                    sys.exit()

                elif cmd_0 == "home":
                    os.system('clear')
                    home()
                elif cmd_0 == "help":
                    print ("")
                    table_datas = [
                        ["\n\n\n\n\n\nCOMMANDS\n", """

scan      :  Map your network.

iface     :  Manually set your network interface.

gateway   :  Manually set your gateway.

rmlog     :  Delete all logs.

help      :  Display this help message.

exit      :  Close.\n"""]
                        ]
                    table = DoubleTable(table_datas)
                    print(table.table)

                else:
                    print("\033[1;91m\n[!] Error : Command not found.\033[1;m")

        home()
        cmd0()

    except KeyboardInterrupt:
		#print ("\n" + exit_msg)
        sleep(1)

    except Exception:
        traceback.print_exc(file=sys.stdout)
    sys.exit(0)

if __name__ == '__main__':
    main()
