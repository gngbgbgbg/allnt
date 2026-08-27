import time
import urllib3
try:
    from curl_cffi import requests
except ImportError:
    import requests

# غیرفعال کردن اخطارهای SSL
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

class RenderWARPClient:
    def __init__(self, base_url, username, password):
        self.base_url = base_url.rstrip('/')
        self.username = username
        self.password = password
        
        # ساخت نشست پایتون
        self.session = requests.Session(impersonate="chrome120")
        
        # هدایت تمام ترافیک به سمت پروکسی موضعی Cloudflare WARP
        warp_proxy = "socks5://127.0.0.1:4001"
        self.session.proxies = {
            "http": warp_proxy,
            "https": warp_proxy
        }
        
        self.headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
            "Accept": "application/json, text/plain, */*",
            "Content-Type": "application/json",
            "Origin": self.base_url,
            "Referer": f"{self.base_url}/panel/"
        }

    def login(self):
        login_url = f"{self.base_url}/login"
        payload = {"username": self.username, "password": self.password}
        
        try:
            print("[*] در حال اتصال به 3x-ui از طریق تونل WARP...")
            response = self.session.post(login_url, json=payload, headers=self.headers, timeout=15, verify=False)
            
            if response.status_code == 200 and response.json().get("success"):
                print("[+] لاگین موفقیت‌آمیز بود! ترافیک با موفقیت از Cloudflare WARP عبور کرد.")
                return True
            else:
                print(f"[-] لاگین ناموفق: {response.text}")
        except Exception as e:
            print(f"[-] خطای ارتباطی (تست سلامت WARP): {e}")
            
        return False

if __name__ == "__main__":
    PANEL_URL = "https://YOUR_PANEL_DOMAIN_OR_IP:2053"
    USERNAME = "admin"
    PASSWORD = "your_password"

    client = RenderWARPClient(PANEL_URL, USERNAME, PASSWORD)
    client.login()
