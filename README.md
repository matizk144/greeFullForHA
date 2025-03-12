# Gree HVAC Home Assistant Integration
Yet another custom integration for GREE devices

## Why projects was created and why this integration is better then other?
__Build-in GREE integration in Home Assistant often lose connectivity to devices.__

GREE devices, make since 2022 have (probably different - cheaper) Wi-Fi integration which lose some PING packets.
   
_This integration use written from the scratch Python library __greeclimateapi__ (https://github.com/matizk144/greeclimateapi/) which handle this issue_

__Build-in GREE integration detect devices by broadcasting packets only.__

_This integration support devices, which IP/hostname was entered manually._

__Build-in GREE integration support Vertical Swing only__

_This integration support all modes in Vertical Swing & Horizontal Swing. Beside this handle UV lamp, Fresh Air_


# How to install
1. Copy content from folder _custom_components_ into your Home Assistant instance
2. Add entry in _configuration.yaml_ file with name and IP/hostname(s)
3. Since GREE changed encryption _enc_ parameter is needed to set encryption. There is two possibilites:
  - _ecb_ - for older HVACs which WIFI module is less that v1.21
  - _gcm_ - for newer HVACS which WIFI module is above v1.21

  If you have troubles with connection try another encryption. I don't have exacly specified from which version GCM encryption is used.

## Example
```
gree_full:
  - name: biuro
    host: 10.0.4.104
    enc: ecb
  - name: salon
    host: 10.0.4.107
    enc: gcm
```

# Which entites are added:
- climate HVAC with temperature and fun modes
- horizontal swing option list
- vertical swing option list
- switch to control Display LED
- switch to control UV lamp
- switch to control fresh air

## Example:

![image](https://github.com/matizk144/greeFullForHA/assets/14313831/027a0827-bce6-42ff-98e4-f2c15498ddfc)


