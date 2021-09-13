# CFGAllowedFunctions
A pykd version-independent tool that finds and dump Control Flow Guard allowed functions.

Given a list of module/symbols, it resolves it and by emulating ntdll!LdrpDispatchUserCallTarget logic, it can verify at runtime
if a function is allowed from CFG bitmap table.

Tested on Win10 21H1 - Should work on all previous releases as well.

## Requirements

* PYKD Bootstrapper x64
* Python3 x64 

## Sample Usage
```
[from within WinDBG]
.load C:\Users\uf0\Desktop\pykd\pykd.dll
py c:\users\uf0\desktop\cfg_allowed_functions.py 
0:007> !py c:\users\uf0\desktop\cfg_check.py
line 1 of 1775

[*] KERNELBASE!AccessCheck at: 00007fffe7262500
[!] Function KERNELBASE!AccessCheck is allowed by CFG
line 2 of 1775

[...]

[*] KERNELBASE!AccessCheckByTypeResultListAndAuditAlarmW at: 00007fffe72cf460
line 8 of 1775
[!] - KERNELBASE!AcquireSRWLockExclusiveis unmapped
...
[*] KERNELBASE!AddAccessDeniedAceEx at: 00007fffe724fff0
[!] Function KERNELBASE!AddAccessDeniedAceEx is allowed by CFG
line 17 of 1775
```

A module's function list can be generated from one of the [Geoff Chappell](https://www.geoffchappell.com/studies/windows/win32/kernel32/api/index.htm) up-to-date pages.
