import random
import string
import json
import tls_client
from raducord import Logger, Discord, Utils
import concurrent.futures

def eat_proxies(filename='proxies.txt'):
    with open(filename, 'r') as f:
        return f.read().splitlines()

def randoproxy(proxies):
    return random.choice(proxies)

def randousername():
    return ''.join(random.choices(string.ascii_lowercase, k=4))

def check_username(username, proxy):
    session = tls_client.Session(client_identifier="chrome112", random_tls_extension_order=True)
    fingerprint = Discord.get_fingerprint(proxy)
    url = 'https://discord.com/api/v9/unique-username/username-attempt-unauthed'
    headers = {
        'Accept': '*/*',
        'Accept-Encoding': 'gzip, deflate, br, zstd',
        'Accept-Language': 'en-US,en;q=0.9',
        'Content-Type': 'application/json',
        'Cookie': '__dcfduid=42befe801f5111efb8ec338969478576; __sdcfduid=42befe811f5111efb8ec338969478576b7289ff5d0e79c0957567e50da2a91d62708592eb3890538adf8a9d0aafe4b47; __cfruid=bb845449d4e76cbcab9a1778df69237aa03094c8-1717161934; _cfuvid=0qzgb3mYskKrXn94Uz_LS2UVvPE0pbX3FeFFutOLmj4-1717161934448-0.0.1.1-604800000; locale=en-US; cf_clearance=pgcUkHRRF6981dLPqWI_FMwzvKON.A8Jp3Bb1nmiEcQ-1717161937-1.0.1.1-WQWxPF_k031.KXpHOaRkCJ32.wXWhIIqJW2fWpYbt2Nrm_NZEQr5KGkn23sWL3UN51T00D9a2ytP9oNidYBYMw; _gcl_au=1.1.1989320239.1717161939; OptanonConsent=isIABGlobal=false&datestamp=Fri+May+31+2024+15%3A25%3A39+GMT%2B0200+(Central+European+Summer+Time)&version=6.33.0&hosts=&landingPath=https%3A%2F%2Fdiscord.com%2F&groups=C0001%3A1%2CC0002%3A1%2CC0003%3A1; _ga=GA1.1.1221245423.1717161939; _ga_Q149DFWHT7=GS1.1.1717161939.1.0.1717161940.0.0.0',
        'Origin': 'https://discord.com',
        'Priority': 'u=1, i',
        'Referer': 'https://discord.com/register',
        'Sec-Ch-Ua': '"Google Chrome";v="125", "Chromium";v="125", "Not.A/Brand";v="24"',
        'Sec-Ch-Ua-Mobile': '?0',
        'Sec-Ch-Ua-Platform': '"Windows"',
        'Sec-Fetch-Dest': 'empty',
        'Sec-Fetch-Mode': 'cors',
        'Sec-Fetch-Site': 'same-origin',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/125.0.0.0 Safari/537.36',
        'X-Debug-Options': 'bugReporterEnabled',
        'X-Discord-Locale': 'en-US',
        'X-Discord-Timezone': 'Europe/Oslo',
        'X-Fingerprint': fingerprint,
        'X-Super-Properties': 'eyJvcyI6IldpbmRvd3MiLCJicm93c2VyIjoiQ2hyb21lIiwiZGV2aWNlIjoiIiwic3lzdGVtX2xvY2FsZSI6ImVuLVVTIiwiYnJvd3Nlcl91c2VyX2FnZW50IjoiTW96aWxsYS81LjAgKFdpbmRvd3MgTlQgMTAuMDsgV2luNjQ7IHg2NCkgQXBwbGVXZWJLaXQvNTM3LjM2IChLSFRNTCwgbGlrZSBHZWNrbykgQ2hyb21lLzEyNS4wLjAuMCBTYWZhcmkvNTM3LjM2IiwiYnJvd3Nlcl92ZXJzaW9uIjoiMTI1LjAuMC4wIiwib3NfdmVyc2lvbiI6IjEwIiwicmVmZXJyZXIiOiIiLCJyZWZlcnJpbmdfZG9tYWluIjoiIiwicmVmZXJfY3VycmVudCI6IiIsInJlbGVhc2VfY2hhbm5lbCI6InN0YWJsZSIsImNsaWVudF9idWlsZF9udW1iZXIiOjI5NzI3NCwiY2xpZW50X2V2ZW50X3NvdXJjZSI6bnVsbCwiZGVzaWduX2lkIjowfQ=='
    }
    payload = {'username': username}
    response = session.post(url, headers=headers, json=payload, proxy=proxy)
    return response.json()

def handle(proxies):
    username = randousername()
    proxy = randoproxy(proxies)
    try:
        result = check_username(username, proxy)
        if result.get('taken') == False:
            Logger.success(f"Username: {username}, Status: VALID, ExtraInfo: SUCCESS")
            with open('valid_usernames.txt', 'a') as f:
                f.write(f"{username}\n")
        else:
            Logger.failed(f"Username: {username}, Status: INVALID, ExtraInfo: FAILURE")
    except Exception as e:
        Logger.warning(f"Proxy error: {e}")

def main():
    proxies = eat_proxies()
    num_threads = int(input("Enter the number of threads: "))
    num_attempts = 10000

    with concurrent.futures.ThreadPoolExecutor(max_workers=num_threads) as executor:
        futures = [executor.submit(handle, proxies) for _ in range(num_attempts)]
        concurrent.futures.wait(futures)

if __name__ == '__main__':
    main()
