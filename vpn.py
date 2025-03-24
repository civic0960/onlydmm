import requests
import pandas as pd
from io import StringIO
import base64
import os
import re
import random

# 定義要插入的配置內容
additional_config = '''
data-ciphers AES-256-GCM:AES-128-GCM:AES-128-CBC
route-nopull
# accounts.dmm.com games.dmm.com
route 13.35.0.0 255.255.0.0
# dmm.co.jp
route 13.248.0.0 255.255.0.0
# games.dmm.co.jp
route 18.65.0.0 255.255.0.0
# osapi.dmm.com
route 202.6.0.0 255.255.0.0
# apidgp-gameplayer.games.dmm.com
route 35.76.0.0 255.255.0.0
route 54.249.0.0 255.255.0.0
'''

# 定義 ISRG Root X1 證書
ISRG_Root_X1 = '''<ca>
-----BEGIN CERTIFICATE-----
MIIFazCCA1OgAwIBAgIRAIIQz7DSQONZRGPgu2OCiwAwDQYJKoZIhvcNAQELBQAw
TzELMAkGA1UEBhMCVVMxKTAnBgNVBAoTIEludGVybmV0IFNlY3VyaXR5IFJlc2Vh
cmNoIEdyb3VwMRUwEwYDVQQDEwxJU1JHIFJvb3QgWDEwHhcNMTUwNjA0MTEwNDM4
WhcNMzUwNjA0MTEwNDM4WjBPMQswCQYDVQQGEwJVUzEpMCcGA1UEChMgSW50ZXJu
ZXQgU2VjdXJpdHkgUmVzZWFyY2ggR3JvdXAxFTATBgNVBAMTDElTUkcgUm9vdCBY
MTCCAiIwDQYJKoZIhvcNAQEBBQADggIPADCCAgoCggIBAK3oJHP0FDfzm54rVygc
h77ct984kIxuPOZXoHj3dcKi/vVqbvYATyjb3miGbESTtrFj/RQSa78f0uoxmyF+
0TM8ukj13Xnfs7j/EvEhmkvBioZxaUpmZmyPfjxwv60pIgbz5MDmgK7iS4+3mX6U
A5/TR5d8mUgjU+g4rk8Kb4Mu0UlXjIB0ttov0DiNewNwIRt18jA8+o+u3dpjq+sW
T8KOEUt+zwvo/7V3LvSye0rgTBIlDHCNAymg4VMk7BPZ7hm/ELNKjD+Jo2FR3qyH
B5T0Y3HsLuJvW5iB4YlcNHlsdu87kGJ55tukmi8mxdAQ4Q7e2RCOFvu396j3x+UC
B5iPNgiV5+I3lg02dZ77DnKxHZu8A/lJBdiB3QW0KtZB6awBdpUKD9jf1b0SHzUv
KBds0pjBqAlkd25HN7rOrFleaJ1/ctaJxQZBKT5ZPt0m9STJEadao0xAH0ahmbWn
OlFuhjuefXKnEgV4We0+UXgVCwOPjdAvBbI+e0ocS3MFEvzG6uBQE3xDk3SzynTn
jh8BCNAw1FtxNrQHusEwMFxIt4I7mKZ9YIqioymCzLq9gwQbooMDQaHWBfEbwrbw
qHyGO0aoSCqI3Haadr8faqU9GY/rOPNk3sgrDQoo//fb4hVC1CLQJ13hef4Y53CI
rU7m2Ys6xt0nUW7/vGT1M0NPAgMBAAGjQjBAMA4GA1UdDwEB/wQEAwIBBjAPBgNV
HRMBAf8EBTADAQH/MB0GA1UdDgQWBBR5tFnme7bl5AFzgAiIyBpY9umbbjANBgkq
hkiG9w0BAQsFAAOCAgEAVR9YqbyyqFDQDLHYGmkgJykIrGF1XIpu+ILlaS/V9lZL
ubhzEFnTIZd+50xx+7LSYK05qAvqFyFWhfFQDlnrzuBZ6brJFe+GnY+EgPbk6ZGQ
3BebYhtF8GaV0nxvwuo77x/Py9auJ/GpsMiu/X1+mvoiBOv/2X/qkSsisRcOj/KK
NFtY2PwByVS5uCbMiogziUwthDyC3+6WVwW6LLv3xLfHTjuCvjHIInNzktHCgKQ5
ORAzI4JMPJ+GslWYHb4phOWim57iaztXOoJwTdwJx4nLCgdNbOhdjsnvzqvHu7Ur
TkXWStAmzOVyyghqpZXjFaH3pO3JLF+l+/+sKAIuvtd7u+Nxe5AW0wdeRlN8NwdC
jNPElpzVmbUq4JUagEiuTDkHzsxHpFKVK7q4+63SM1N95R1NbdWhscdCb+ZAJzVc
oyi3B43njTOQ5yOf+1CceWxG1bQVs5ZufpsMljq4Ui0/1lvh+wjChP4kqKOJ2qxq
4RgqsahDYVvTH9w7jXbyLeiNdd8XM2w9U/t7y0Ff/9yi0GE44Za4rF2LN9d11TPA
mRGunUHBcnWEvgJBQl9nJEiU0Zsnvgc/ubhPgXRR4Xq37Z0j4r7g1SgEEzwxA57d
emyPxgcYxn/eR44/KJ4EBs+lVDR3veyJm+kXQ99b21/+jh5Xos1AnX5iItreGCc=
-----END CERTIFICATE-----
</ca>'''

# 獲取 VPNGate 的 API 數據
def fetch_vpn_data():
    url = 'http://www.vpngate.net/api/iphone/'
    response = requests.get(url)
    data = '\n'.join(response.text.splitlines()[1:])  # 移除第一行標題
    df = pd.read_csv(StringIO(data))
    return df

# 過濾並找到最快的 N 個 VPN 伺服器
def filter_top_vpns(df, top_n=5):
    # 過濾日本的伺服器，排除 IP 以 219 開頭的伺服器，按速度排序
    filtered_df = df[(df['CountryShort'] == 'JP') & (~df['IP'].str.startswith('219', na=False))]
    top_vpns = filtered_df.sort_values('Speed', ascending=False).head(top_n)  # 取速度最快的前 N 個
    return top_vpns

# 處理 VPN 配置文件
def process_vpn_config(config):
    # 將 bytes 轉為字符串
    config = config.decode('utf-8')
    
    # 替換 CA 證書
    config = re.sub(r'(<ca>)(.+?)(</ca>)', ISRG_Root_X1, config, flags=re.DOTALL)
    
    # 找到 "#auth-user-pass" 行並在其下方插入 additional_config
    #if "#auth-user-pass" in config:
        #config = config.replace("#auth-user-pass", f"#auth-user-pass\n{additional_config}")
    
    # 將字符串轉回 bytes
    return config.encode('utf-8')

# 保存 VPN 配置文件
def save_vpn_config(ip, config, output_dir='OVPN'):
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
    file_path = os.path.join(output_dir, f"{ip}.ovpn")
    with open(file_path, 'wb') as f:
        f.write(config)
    print(f"Saved VPN config for IP {ip} to {file_path}")

# 主函數
def main():
    # 獲取並處理 VPN 數據
    df = fetch_vpn_data()
    top_vpns = filter_top_vpns(df, top_n=5)  # 取速度最快的前 5 個

    # 隨機選擇一個 VPN 伺服器
    random_vpn = top_vpns.sample(1).iloc[0]

    # 處理並保存隨機選擇的 VPN 配置文件
    ip = random_vpn['IP']
    config_base64 = random_vpn['OpenVPN_ConfigData_Base64']
    config = base64.b64decode(config_base64)  # 解碼 Base64
    config = process_vpn_config(config)  # 插入 additional_config 並替換 CA 證書
    save_vpn_config(ip, config)  # 保存配置文件

if __name__ == "__main__":
    main()