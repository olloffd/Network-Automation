import xlrd, xlwt
from netmiko import ConnectHandler
import datetime
import time


writebook = xlwt.Workbook()
WBSheet = writebook.add_sheet("PortStats")



#Import the excel spreadsheet
file_location = "C:\\Users\\olloff.denuyschen\\Documents\\Training\\Cisco\\Programming\\Scripts\\Netmiko\\Testing\\ConfigGrab2.xlsx"
workbook = xlrd.open_workbook(file_location)
sheet = workbook.sheet_by_index(0)
rows = sheet.nrows
row_count = 1
errorState = False
testArray = []
portData = {}

while row_count < rows:
    # Create variables based on values in the master excel spreadsheet
    device_name = sheet.cell_value(row_count, 0)
    device_role = sheet.cell_value(row_count, 1)
    site = sheet.cell_value(row_count, 2)
    ip_address = sheet.cell_value(row_count, 3)
    username = sheet.cell_value(row_count, 4)
    password = sheet.cell_value(row_count, 5)
    enable = sheet.cell_value(row_count, 6)

    # SSH to device and execute commands
    try:
        print('Connecting to '+ device_name+ ' with IP '+ ip_address)
        net_connect = ConnectHandler(device_type='cisco_ios', ip=ip_address, username=username, password=password)
        output = net_connect.send_command("show interface status")
    except Exception as e:
        print(f'An Error Occurred on {device_name}. Error Details: {e}')
        errorState=True
        time.sleep(5)

    # Saves output in a .txt file
    if errorState == False:
        swPortDict = {}
        filename = open((device_name) + '.txt', 'w')
        filename.write(output)
        filename.close()
        #print(type(output))
        outputSplit = output.splitlines()
        #print (outputSplit)
        #testArray.append(outputSplit)
        lineCounter = 0
        portData[device_name] = {'ip':ip_address,
                                 'deviceRole':device_role,
                                 'site':site,
                                 'portCount':0,
                                 'UpInterfaces':0,
                                 'DownInterfaces':0,
                                 'GigPorts':0,
                                 '100MPorts':0,
                                 'TenGigPorts': 0}
        for line in outputSplit:
            lineCounter += 1

            if lineCounter > 2:
                lineArray = line.split(' ')
                for item in lineArray:
                    if item != '':
                        #print (item)

                        if 'Gi' in item or 'Fa' in item or 'Te' in item :
                            portData[device_name]['portCount'] +=1
                            if 'Gi' in item:
                                portData[device_name]['GigPorts'] += 1
                            elif 'Fa' in item:
                                portData[device_name]['100MPorts'] += 1
                            elif 'Te' in item:
                                portData[device_name]['TenGigPorts'] += 1
                        if 'notconnect' in item:
                            portData[device_name]['DownInterfaces'] += 1
                        elif 'connected' in item:
                            portData[device_name]['UpInterfaces'] +=1





    errorState = False
    print ('Done with '+ device_name+ ' with IP '+ ip_address )
    row_count +=1
#print (testArray)
print (portData)

WBSheet.write(0, 0,'Hostname')
WBSheet.write(0, 1,'IP')
WBSheet.write(0, 2,'site')
WBSheet.write(0, 3,'deviceRole')
WBSheet.write(0, 4,'portCount')
WBSheet.write(0, 5,'UpInterfaces')
WBSheet.write(0, 6,'DownInterfaces')
WBSheet.write(0, 7,'GigPorts')
WBSheet.write(0, 8,'100MPorts')
WBSheet.write(0, 9,'TenGigPorts')




writeLine = 1
for host in list(sorted(portData)):
    WBSheet.write(writeLine,0,host)
    WBSheet.write(writeLine, 1, portData[host]['ip'])
    WBSheet.write(writeLine, 2, portData[host]['site'])
    WBSheet.write(writeLine, 3, portData[host]['deviceRole'])
    WBSheet.write(writeLine, 4, portData[host]['portCount'])
    WBSheet.write(writeLine, 5, portData[host]['UpInterfaces'])
    WBSheet.write(writeLine, 6, portData[host]['DownInterfaces'])
    WBSheet.write(writeLine, 7, portData[host]['GigPorts'])
    WBSheet.write(writeLine, 8, portData[host]['100MPorts'])
    WBSheet.write(writeLine, 9, portData[host]['TenGigPorts'])
    writeLine +=1



writebook.save('C:\\Users\\Olloff.Denuyschen\\Desktop\\Python Scripts\\Netmiko\\Testing\\PortCountOut.xls')
time.sleep(3)