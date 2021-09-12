from pykd import *
import sys

# .load C:\Users\uf0\Desktop\pykd\pykd.dll
# !py c:\users\uf0\desktop\cfg_allowed_functions.py 

def get_bitmap_address(addr):
    right_shifted = addr >> 9
    near_symbol = (pykd.dbgCommand("ln ntdll!LdrpMrdataUnprotected")).split('|')[0]
    near_symbol_address = near_symbol[near_symbol.find('(')+1:near_symbol.find(')')].replace('`','').strip('\n')

    index = 0

    while True:
        cmd = "dq " + near_symbol_address + "-" + hex(index) + " L1"
        magic_value = (pykd.dbgCommand(cmd)).split('  ')[1].strip('\n')
        if magic_value == '00000200`00000000':
            #print('[*] found magic value')
            index = index +0x8
            cmd = "dq " + near_symbol_address + "-" + hex(index) + " L1"
            bitmap_base_index = (pykd.dbgCommand(cmd)).split('  ')[1].replace('`','').strip('\n')
            break
        else:
            index = index + 0x8
            #print(hex(index))
            
    #print("[*] BITMAP BASE:\t\t\t      " +bitmap_base_index)
    bitmap_function_address = (pykd.dbgCommand("dq " + bitmap_base_index + " + " + hex(right_shifted) + " * 8 L1")).split('  ')[1].replace('`','').strip('\n')
    #print("[*] BITMAP FUNCTION ADDR:\t\t      " + bitmap_function_address)
    return bitmap_function_address

def main():
    # file with a list of APIs
    kernelbase_apis_file = "c:\\users\\uf0\\desktop\\kernelbase.txt"
    f = open(kernelbase_apis_file, "r")
    total_lines = sum(1 for line in open(kernelbase_apis_file)) 
    
    for i, line in enumerate(f):
        print("line %d of %s" % (i+1,total_lines))
        #function_to_check = sys.argv[1]
        function_to_check = line.strip('\n').strip()
        try: 
            function_address = (pykd.dbgCommand("x "+function_to_check)).split(' ')[0].replace('`','').strip()
            print("\n[*] " + function_to_check + " at: " +function_address)
        except(AttributeError):
            print("[!] - " + function_to_check + "is unmapped\n")
        int_function_address = int(function_address, 16)
        bit_position = (int_function_address >> 3) % 0x40
        #print("[*] Nth bit to check:\t\t\t      "  + (hex(bit_position)))
        
        bitmap_function_address = (int(get_bitmap_address(int_function_address),16))
        mask = pow(2,bit_position)

        check_valid_function =  bitmap_function_address & mask
        if  mask == check_valid_function:
            print("[!] Function "+ function_to_check + " is allowed by CFG")
            with open("c:\\users\\uf0\\desktop\\cfg_allowed_kernelbase.txt", "a") as myfile:
                myfile.write(function_to_check+"\n")
        else:
            #print("[!] Function "+ function_to_check + " is NOT allowed by CFG")
            pass
        
if __name__ == "__main__":
    main()


