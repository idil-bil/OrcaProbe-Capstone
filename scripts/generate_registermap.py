import pandas as pd

def generate_register_files(excel_path):
    # Load register map
    sheet_data = pd.read_excel(excel_path)
    
    # Extract relevant data
    registers = []
    for _, row in sheet_data.iterrows():
        register_name = row["Register"]
        address = int(row["Address"])
        bitfields = row["Bitfields"].split("\n") if pd.notna(row["Bitfields"]) else []
        registers.append({
            "name": register_name,
            "address_hex": f"0x{address:X}",
            "address_dec": address,
            "bitfields": bitfields
        })
    
    # Generate constants.py
    with open("../Software/registers.py", "w") as f:
        f.write("# Register Addresses\n")
        for reg in registers:
            f.write(f"{reg['name']} = {reg['address_hex']}  # Address in decimal: {reg['address_dec']}\n")
        f.write("\n# Bitfields\n")
        for reg in registers:
            if reg['bitfields']:
                f.write(f"# {reg['name']}\n")
                for field in reg['bitfields']:
                    bit_range, name = field.split(": ")
                    if "-" in bit_range:
                        end, start = map(int, bit_range.split("-"))
                        length = end - start + 1
                    else:
                        start, length = int(bit_range), 1
                    f.write(f"{reg['name']}_{name}_POSITION = {start}\n")
                    f.write(f"{reg['name']}_{name}_LENGTH = {length}\n")
                f.write("\n")
    
    # Generate registers
        f.write("# Register Classes\n")
        for reg in registers:
            f.write(f"class DVC_{reg['name']}:\n")
            f.write(f"    def __init__(self):\n")
            if reg['bitfields']:
                for field in reg['bitfields']:
                    bit_range, name = field.split(": ")
                    f.write(f"        self.{name[0] + name[1:]} = [0xDEAD,{reg['name']}_{name}_POSITION, {reg['name']}_{name}_LENGTH]\n")
            else:
                f.write("    pass\n")
            f.write("\n")
        f.write("class DVC_RegisterMap:\n")
        f.write(f"    def __init__(self):\n")
        for reg in registers:
            f.write(f"        self.{reg['name']} = DVC_{reg['name']}()\n")
        f.write("\n\nreg_map = DVC_RegisterMap()\n")

    # Generate interface.py
    with open("../Software/interface.py", "w") as f:
        f.write("# interface.py\n\n")
        f.write("import comm\n\n")
        f.write("from registers import *\n\n")
        f.write("def read_register(ser,register_address):\n")
        f.write("    valW = comm.pack_32bit(register_address,0)\n")
        f.write("    comm.send_value(ser,valW)\n")
        f.write("    _, valR = comm.unpack_32bit(comm.receive_value(ser))\n")
        f.write("    return valR\n\n")
        f.write("def write_register(ser,register_address, value):\n")
        f.write("    valW = comm.pack_32bit(128+register_address,value)\n")
        f.write("    comm.send_value(ser,valW)\n")
        f.write("    return\n\n")
        
        # Generate targeted write register functions
        for reg in registers:
            if reg['bitfields']:
                f.write(f"def write_reg_{reg['name']}(ser, reg_map):\n")
                f.write(f"    write_register(ser, {reg['name']}, \n                  ")
                f.write("\n                 |"
                      .join([f"(reg_map.{reg['name']}.{field.split(': ')[1]}[0] << reg_map.{reg['name']}.{field.split(': ')[1]}[1])" for field in reg['bitfields']]))
                f.write(")\n\n")

                # Generate targeted read register functions
        for reg in registers:
            if reg['bitfields']:
                f.write(f"def read_reg_{reg['name']}(ser, reg_map):\n")
                f.write(f"    valR = read_register(ser, {reg['name']})\n")
                for field in reg['bitfields']:
                    name = field.split(": ")[1]
                    f.write(f"    reg_map.{reg['name']}.{name}[0] = (valR >> reg_map.{reg['name']}.{name}[1]) & ((1 << reg_map.{reg['name']}.{name}[2]) - 1)\n")
                f.write("\n")
    
    print("Files generated: interface.py, registers.py in Software directory")

# Example usage
generate_register_files("JY85-FW_Register_Map.xlsx")