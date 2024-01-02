# Gree HVAC Home Assistant Integration
Yet another custom integration for GREE devices

## Why projects was created and why this integration is better then other?
__Build-in GREE integration in Home Assistant often loose connectivity to devices.__

GREE devices, make since 2022 have different (probably cheaper) Wi-Fi integration which loose some PING packets.
   
_This integration use written from the scratch Python library __greeclimateapi__ (https://github.com/matizk144/greeclimateapi/) which handle this issue_

__Build-in GREE integration detect devices by broadcasting packets only.__

_This integration support devices, which IP/hostname was entered manually._

__Build-in GREE integration support Vertical Swing only__

_This integration support all modes in Vertical Swing & Horizontal Swing. Beside this handle UV lamp, Fresh Air 


# How to install
1. Copy content from folder _custom_components_ into your Home Assistant instance
2. Add entry in _configuration.yaml_ file with name and IP/hostname(s) like in example:

```
gree_full:
  - name: office_hvac
    host: 10.0.4.104
  - name: corridor_hvac
    host: 10.0.4.175    
  - name: bedroom_hvac
    host: 10.0.4.225
```