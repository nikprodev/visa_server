# visa_server

This Python script runs in a Windows environment and communicates with the PPMS/VersaLab (Quantum Design) device via the MultiVu software. It provides a standard VISA interface over the TCP/IP protocol. Additional devices can be integrated into the server to expose them through the VISA protocol; for example, support for a LinkBone switching matrix backend has been added.

The program requires Python 3 (version ≤ 3.12) and the <a href="https://pypi.org/project/pywin32/">pywin32</a> extension to access Windows API functions. Also, for the server to work, the _rpcbind_ portmapper service is required, which can be launched in a WSL Linux virtual environment.
