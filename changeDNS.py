# coding:utf-8
from re import match
from re import findall
from wmi import WMI
from ctypes import windll
from sys import executable
'''
sync
'''

class Network2(object):
    @property
    def testEnvDNS(self):
        return ['192.168.6.1']

    @property
    def proEnvDns(self):
        return ['114.114.114.114']

    @property
    def googleEnvDns(self):
        return ['8.8.8.8']


# print('正在修改IP，请稍后')

wmiService = WMI()

colNicConfigs = wmiService.Win32_NetworkAdapterConfiguration(IPEnabled=True)

# 调试代码，打印出所有的object


def showAll():
    for objNicConfig in colNicConfigs:
        print(
'''    ------------------------------------------------
    |index      |%s
    |Description|%s
    |SettingID  |%s
    |ip         |%s
    |subnet     |%s
    |gateway    |%s
    |dns        |%s   '''

        % (
            objNicConfig.Index,
            objNicConfig.Description,
            objNicConfig.SettingID,
            objNicConfig.IPAddress,
            objNicConfig.IPSubnet,
            objNicConfig.DefaultIPGateway,
            objNicConfig.DNSServerSearchOrder,
           )
        )


if len(colNicConfigs) < 1:
    print('没有找到可用的网络适配器')
    exit()

# 获取第一个网络适配器的设置
objNicConfig = colNicConfigs[0]

# for method_name in objNicConfig.methods:
#   method = getattr(objNicConfig, method_name)
#   print method


# ----------------ip地址、网关等-------------------
arrIPAddresses = ['192.168.1.136']
arrSubnetMasks = ['255.255.0.0']
arrDefaultGateways = ['192.168.1.1']
arrGatewayCostMetrics = [1]
# ----------------ip地址、网关等-------------------

arrDNSServers = ['']

intReboot = 0


def modifyIP():
    returnValue = objNicConfig.EnableStatic(IPAddress=arrIPAddresses, SubnetMask=arrSubnetMasks)
    if returnValue[0] == 0:
        print('  成功设置IP')
    elif returnValue[0] == 1:
        print('  成功设置IP')
        # intReboot += 1
    else:
        print(returnValue[0])
        print('修改IP失败(IP设置发生错误)')
        exit()


def modifyGateway():
    returnValue = objNicConfig.SetGateways(DefaultIPGateway=arrDefaultGateways, GatewayCostMetric=arrGatewayCostMetrics)
    if returnValue[0] == 0:
        print('  成功设置网关')
    elif returnValue[0] == 1:
        print('  成功设置网关')
        # intReboot += 1
    else:
        print('修改IP失败(网关设置发生错误)')
        exit()

prompt_str = 'DNS修改成功，当前DNS %s'

def modifyDNS(dns=['']):
    returnValue = objNicConfig.SetDNSServerSearchOrder(DNSServerSearchOrder=dns)
    if returnValue[0] == 0:
        print(prompt_str % dns[0])
    elif returnValue[0] == 1:
        print(prompt_str % dns[0])
        # intReboot += 1
    else:
        print('修改IP失败(DNS设置发生错误)')
        # print (returnValue[0])  调试代码。 打印出当前修改的object。
        exit()


def notUse():
    if intReboot > 0:
        print('需要重新启动计算机')
    else:
        print('')
        print('  修改后的配置为：')
        print('  IP: ', ', '.join(objNicConfig.IPAddress))
        print('  掩码:', ', '.join(objNicConfig.IPSubnet))
        print('  网关:', ', '.join(objNicConfig.DefaultIPGateway))
        print('  DNS:', ', '.join(objNicConfig.DNSServerSearchOrder))


# print ('修改IP结束')



def specific():
    # 正则匹配输入的dns格式
    dns_str = input('输入自定义的DNS >>')
    pattern = "[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}"
    pattern_split = '\d{1,3}'
    if (match(pattern,dns_str)) != None:
        dns_ls = findall(pattern_split,dns_str)
        format_correct = True
        for dns_unit in dns_ls:
            if int(dns_unit) > 255:
                format_correct = False
                print('输入的DNS格式不正确(号段只能在256以内）')
                break
        if format_correct:
            modifyDNS([dns_str])
    else:
        print('输入的DNS格式不正确')


def help_note():
    print('操作命令')
    print('1    --   切换DNS到测试环境')
    print('2    --   切换DNS到生产环境')
    print('3    --   切换DNS到8.8.8.8，可在公司访问谷歌')
    print('spec --   自己输入dns')
    print('des  --   查看当前适配器名称')
    print('ip   --   查看当前ip（输入ipv6或v6可查看ipv6地址）')
    print('gw   --   查看当前网关（gateway,wg,wangguan均可)')
    print('dns  --   查看当前DNS')
    print('all  --   查看所有网络适配器信息')
    print('h    --   显示帮助')
    print('doc')
    # print('q    --   退出')



def run():
    currentDns = objNicConfig.DNSServerSearchOrder[0]
    if currentDns == '192.168.6.1':
        env_str = '测试环境'
    elif currentDns == '8.8.8.8':
        env_str = '可访问google'
    elif currentDns == '114.114.114.114':
        env_str = '生产环境'
    elif currentDns == '223.5.5.5':
        env_str = '生产环境'
    else:
        env_str = '生产环境'
    print('当前%s（%s）' % (env_str,currentDns) ,end=',')


    print('按数字切换当前DNS\n\t1 - 测试环境(192.168.6.1)\n\t2 - 生产环境（114.114.114.114）\n\t3 - 访问google（8.8.8.8）\n')


    while True:
        i = input('>>')
        c = str.strip(i)


        if c == '1':
            modifyDNS(Network2().testEnvDNS)

        elif c == '2':
            modifyDNS(Network2().proEnvDns)

        elif c == '3':
            modifyDNS(Network2().googleEnvDns)

        elif c == 'h':
            help_note()

        elif c == 'spec':
            specific()

        elif c == 'des':
            print(objNicConfig.Description)

        elif c == 'ip' or c == 'ipv4':
            print(objNicConfig.IPAddress[0])

        elif c == 'ipv6' or c == 'v6':
            print(objNicConfig.IPAddress)

        elif c == 'gateway' or c == 'wangguan' or c == 'wg' or c == 'gw':
            print(objNicConfig.DefaultIPGateway[0])

        elif c == 'dns':
            print(objNicConfig.DNSServerSearchOrder[0])

        elif c == 'all':
            showAll()

        else:
            print('按h显示帮助')


if __name__ == '__main__':

    def is_admin():
        try:
            return windll.shell32.IsUserAnAdmin()
        except:
            return False


    if is_admin():
        # Code of your program here
        run()
    else:
        # Re-run the program with admin rights
        windll.shell32.ShellExecuteW(None, "runas", executable, "", None, 1)
