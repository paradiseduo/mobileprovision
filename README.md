# mobileprovision
Quick search connect device in which mobileprovision

## How to use

First, make sure you have installed Xocde.app

then, connect iphone or apple device with usb.

finally, git clone

```bash
git clone https://github.com/paradiseduo/mobileprovision
cd mobileprovision
python3 provisioning.py -i  ~/Library/MobileDevice/Provisioning\ Profiles/ 
```

and output info like this:
```bash
xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx.mobileprovision
{
    "ApplicationIdentifierPrefix": [
        "xxxxxxxxxx"
    ],
    "Cert_CN": "Apple Development: paradiseduo (ABCDEFGHIJ)",
    "Cert_OU": "ABCDEFGHIJ",
    "Cert_UID": "ABCDEFGHIJ",
    "Name": "match Development com.paradiseduo.python",
    "TeamIdentifier": [
        "ABCDEFGHIJ"
    ],
    "TeamName": "paradiseduo"
}
```
