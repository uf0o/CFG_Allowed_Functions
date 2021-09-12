# CFGAllowedFunctions
A pykd version-independent tool that finds and dump Control Flow Guard allowed functions.

Given a list of module/symbols, it resolves it and by emulating ntdll!LdrpDispatchUserCallTarget logic, it can verify at runtime
if a function is allowed from CFG bitmap table.

## Sample Usage
```
[from within WinDBG]
py c:\users\uf0\desktop\cfg_allowed_functions.py 
```
