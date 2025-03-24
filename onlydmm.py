
import os
def list_ovpn_files():
    ovpn_files = [f for f in os.listdir() if f.endswith(".ovpn")]
    if not ovpn_files:
        print("ovpn files not found.\n")
        return None
    print("請選擇要修改的ovpn config:\n")
    for i, file in enumerate(ovpn_files):
        print(f"{i}. {file}")
        
    try:
        print("------------------")
        choose = int(input())
        if 0 <= choose < len(ovpn_files):
            return ovpn_files[choose]
        else:
            print("Error.\n")
            return None
    except ValueError:
        print("Error.\n")
        return None
    
def insert_text_in_ovpn(file_path, target):
    with open(file_path, "r") as file:
        lines = file.readlines()
    
    insert_index = -1
    for i, line in enumerate(lines):
        if "#auth-user-pass" in line:
            insert_index = i + 1
            break
    if insert_index == -1:
        print("ovpn config error.\n")
        return None
    
    lines.insert(insert_index, target + "\n")
    
    with open(file_path, "w") as file:
        file.writelines(lines)
        
    print("Done.\n")
    return None

def main():
    ovpn_file = list_ovpn_files()
    if not ovpn_file:
        return None
    
    target_section = """
data-ciphers AES-256-GCM:AES-128-GCM:AES-128-CBC
route-nopull
# accounts.dmm.com games.dmm.com
route 13.35.0.0 255.255.0.0
# dmm.co.jp
route 13.248.0.0 255.255.0.0
# games.dmm.co.jpㄢ
route 18.65.0.0 255.255.0.0
# osapi.dmm.com
route 202.6.0.0 255.255.0.0
# apidgp-gameplayer.games.dmm.com
route 35.76.0.0 255.255.0.0
route 54.249.0.0 255.255.0.0
    """.strip()
    
    insert_text_in_ovpn(ovpn_file, target_section)
    os.system("pause")
    
if __name__ == "__main__":
    main()

