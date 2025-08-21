# visa_server

## Description

This Python script, based on the <a href="https://github.com/coburnw/python-vxi11-server">vxi11-server</a> code, runs in
a Windows environment and communicates with the PPMS/VersaLab (Quantum Design) device via the MultiVu software. It
provides a standard VISA interface over the TCP/IP protocol. Additional devices can be integrated into the server to
expose them through the VISA protocol; for example, support for a LinkBone switching matrix backend has been added.

The program requires Python 3 (version ≤ 3.12) and the <a href="https://pypi.org/project/pywin32/">pywin32</a> extension
to access Windows API functions. Also, for the server to work, the _rpcbind_ portmapper service is required, which can
be launched in a WSL Linux virtual environment.

## Client

To send requests to the server, you can use the <a href="https://pypi.org/project/PyVISA/">pyvisa</a> package with the
Python backend <a href="https://pypi.org/project/PyVISA-py/">pyvisa-py</a>. For example, to request device
identification:

```
import pyvisa
rm = pyvisa.ResourceManager()
inst = rm.open_resource("TCPIP0::127.0.0.1::inst0")
print(inst.query("*IDN?"))
```

_Response:_

```
'Quantum Design,PPMSVersaLab,XXXXXX,V1.0.6.4\r\n'
```

## Versalab queries

### Temperature

**Get temperature:**

```
TEMP?
```

_Response:_

```
'0,300.0,"K",1,"Stable"\r\n'
```

Format: *return_code, value, units, state_code, state_description*

States:

| Code | State                   |
|------|-------------------------|
| 1    | Stable                  |
| 2    | Tracking                |
| 5    | Near                    |
| 6    | Chasing                 |
| 7    | Pot Operation           |
| 10   | Standby                 |
| 13   | Diagnostic              |
| 14   | Impedance Control Error |
| 15   | General Failure         |

**Set temperature:**

```
TEMP 320.5, 20, 0
```

_Response:_

```
'OK\r\n'
```

Format: *value, rate, mode*\
_value_ is set in "K", _rate_ is set in "K/min" (max. 20)

Mode codes:

| Code | Mode         |
|------|--------------|
| 0    | Fast Settle  |
| 1    | No Overshoot |

### Field

**Get field:**

```
FIELD?
```

_Response:_

```
'0,10.0,"Oe",1,"Stable"\r\n'
```

Format: *return_code, value, units, state_code, state_description*

States:

| Code | State            |
|------|------------------|
| 1    | Stable           |
| 2    | Switch Warming   |
| 3    | Switch Cooling   |
| 4    | Holding (Driven) |
| 5    | Iterate          |
| 6    | Ramping          |
| 7    | Ramping          |
| 8    | Resetting        |
| 9    | Current Error    |
| 10   | Switch Error     |
| 11   | Quenching        |
| 12   | Charging Error   |
| 14   | PSU Error        |
| 15   | General Failure  |

**Set field:**

```
FIELD 100.0, 20, 1, 0 
```

_Response:_

```
'OK\r\n'
```

Format: *value, rate, approach, mode*\
_value_ is set in "Oe", _rate_ is set in "Oe/sec", _mode_ is not used

Approach codes:

| Code | Approach  |
|------|-----------|
| 1    | Linear    |
| 2    | Oscillate |

### Chamber

**Get chamber state:**

```
CHAMBER?
```

_Response:_

```
'0,760.0,"Torr",3,"Sealed"\r\n'
```

Format: *return_code, pressure_value, units, state_code, state_description*

States:

| Code | State                 |
|------|-----------------------|
| 0    | Sealed                |
| 1    | Purged and Sealed     |
| 2    | Vented and Sealed     |
| 3    | Sealed                |
| 4    | Performing Purge/Seal |
| 5    | Performing Vent/Seal  |
| 6    | Pre-HiVac             |
| 7    | HiVac                 |
| 8    | Pumping Continuously  |
| 9    | Flooding Continuously |
| 14   | HiVac Error           |
| 15   | General Failure       |

**Change chamber state:**

```
CHAMBER 1
```

_Response:_

```
'OK\r\n'
```

Format: *action*

Action codes:

| Code | Action     |
|------|------------|
| 0    | Seal       |       
| 1    | Purge/Seal |
| 2    | Vent/Seal  |
| 3    | Pump Cont. |
| 4    | Vent Cont. |
| 5    | HiVac      |

### Rotator (if installed)

**Get position:**

```
POS?
```

_Response:_

```
'0,30.0,"Deg",1,"In position"\r\n'
```

Format: *return_code, angle_value, units, state_code, state_description*

States:

| Code | State       |
|------|-------------|
| 1    | In position |
| 2    | Calibrating |
| 5    | Moving      |

**Set position:**

```
POS 90, 30, 0
```

_Response:_

```
'OK\r\n'
```

Format: *value, rate, mode*\
_value_ is set in "Degrees", _rate_ is set in "Deg/sec" (max. 30)

Mode codes:

| Code | Mode              |
|------|-------------------|
| 0    | Move to position  |
| 1    | Move to index     |
| 2    | Redefine position |

## Instrument development

Additional instruments can be added as packages in the `backend` folder, inheriting from the _BaseDevice_ class.
Device parameters such as Manufacturer, Model, IP address, and others can be defined in the `__init__.py` file.