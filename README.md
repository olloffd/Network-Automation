# Network-Automation
Network automation with Python and Secure_CRT scripts.

There are files that go with each other like:

1. m_inventory_report.py + Devices.csv = This must be run from Secure_CRT and it prompts you to fetch the file Devices.csv. It then outputs an text file with all the inventory details of all the switches named in the Devices file. 

2. SwitchportStats.py + ConfigGrab.xlsx = This must be run from an executable .exe Python file or from a docker container. It fetches the  ConfigGrab.xlsx file that is mentioned in the SwitchportStats.py where it is saved. It then outputs an text file with all the Switchport details of all the switches named in the ConfigGrab file. 

3. m_show_cdp_neig.py + myswitches.txt = This must be run from an executable .exe Python file or from a docker container. It fetches the  myswitches.txt file automatically. It then outputs an text file with all switches named in the myswitches file. This will show cdp nei detail info.
