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
    "application-identifier": "xxxxxxxxxx.com.xxxx.xxxxx.xxxxx",
    "com.apple.developer.team-identifier": "xxxxxxxxxx",
    "com.apple.security.application-groups": [
        "group.com.xxxx.xxxxx"
    ],
    "get-task-allow": true,
    "keychain-access-groups": [
        "xxxxxxxxxx.*",
        "com.apple.token"
    ]
}
```
