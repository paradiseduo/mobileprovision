# -*- coding: utf-8 -*-
import os
import sys
import subprocess
import getopt
import plistlib
import json

tasks = []

class RunCMD:
    def __init__(self, cmd):
        self.p = None
        self.cmd = cmd

    def run_cmd(self):
        self.p = subprocess.Popen(self.cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)
        tasks.append(self)
        return self.p.communicate()

    @property
    def is_running(self):
        if self.p.poll() is None:
            return True
        else:
            tasks.remove(self)
            return False

    def stop(self):
        self.p.kill()
        tasks.remove(self)

    def log(self):
        return ''.join([str(item, encoding='utf-8') for item in self.p.communicate()])


def printUse():
    print('''
    Usage:      
        python3 Provisioning.py -i ~/Library/MobileDevice/Provisioning\ Profiles
    
        -h show help
        -i <inputPath>
    ''')


def main(argv):
    inputfile = ''
    try:
        opts, args = getopt.getopt(argv, "hi:", ["ipath="])
    except getopt.GetoptError:
        printUse()
        sys.exit(2)

    for (opt, arg) in opts:
        if opt == "-h":
            printUse()
            sys.exit()
        elif opt in ("-i", "--ipath"):
            inputfile = arg
    
    runner = RunCMD("ideviceinfo -s | grep UniqueDeviceID")
    result = str(runner.run_cmd()[0])
    deviceId = result.split(':')[1].strip()[:-3]
    
    files= os.listdir(inputfile)
    for file in files:
        if (".mobileprovision" in file) and (not os.path.isdir(file)):
            plistName = os.path.abspath(file.replace('mobileprovision', 'plist'))
            cmd = "security cms -D -i " + str(inputfile.replace(' ', '\ ')) + "/" + file + " > " + plistName
            RunCMD(cmd).run_cmd()
            
            cmd = "security cms -D -i " + str(inputfile.replace(' ', '\ ')) + "/" + file
            out = RunCMD(cmd).run_cmd()[0]
 
            start = str(out).find('<data>')+6
            end = str(out).find('</data>')
            cacheName = os.path.abspath(file.replace('mobileprovision', 'txt'))
            cmd = "echo '-----BEGIN CERTIFICATE-----\n" + str(out)[start:end] + "\n-----END CERTIFICATE-----' > " + cacheName
            RunCMD(cmd).run_cmd()
            
            cerName = os.path.abspath(file.replace('mobileprovision', 'cer'))
            cmd = "fold -w 64 " + cacheName + " > " + cerName
            RunCMD(cmd).run_cmd()
            
            cmd = "openssl x509 -inform pem -noout -text -in " + cerName
            outs = RunCMD(cmd).run_cmd()[0].decode('utf-8', 'ignore').split('\n')
            for line in outs:
                if 'Subject:' in line:
                    subject = line.replace('Subject:', '').strip().split(', ')
                    UID = subject[0].replace('UID=', '')
                    CN = subject[1].replace('CN=', '')
                    OU = subject[2].replace('OU=', '')
                    break
            with open(plistName, 'rb') as f:
                pl = plistlib.load(f)
                try:
                    if deviceId in pl['ProvisionedDevices']:
                        dir = {
                            'Name':pl['Name'],
                            'ApplicationIdentifierPrefix':pl['ApplicationIdentifierPrefix'],
                            'TeamIdentifier':pl['TeamIdentifier'],
                            'TeamName':pl['TeamName'],
                            'Cert_UID': UID,
                            'Cert_CN': CN,
                            'Cert_OU': OU
                            }
                        j = json.dumps(dir, sort_keys=True, indent=4, separators=(',', ': '))
                        print(file + '\n' + j + '\n')
                    os.remove(plistName)
                    os.remove(cacheName)
                    os.remove(cerName)
                except:
                    os.remove(plistName)
                    os.remove(cacheName)
                    os.remove(cerName)
                    continue


if __name__ == '__main__':
    main(sys.argv[1:])
