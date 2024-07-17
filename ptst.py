import requests

# List of HTTP proxies with usernames and passwords
proxies = [
    {
        'http': 'http://adminproxy:e0oXocf7PsTAfdcadNMBEoOohXHCfU2V@185.83.114.211:3128',
        'https': 'http://adminproxy:e0oXocf7PsTAfdcadNMBEoOohXHCfU2V@185.83.114.211:3128'
    },
    {
        'http': 'http://adminproxy:e0oXocf7PsTAfdcadNMBEoOohXHCfU2V@62.60.135.93:3128',
        'https': 'http://adminproxy:e0oXocf7PsTAfdcadNMBEoOohXHCfU2V@62.60.135.93:3128'
    },
    {
        'http': 'http://adminproxy:e0oXocf7PsTAfdcadNMBEoOohXHCfU2V@62.60.135.92:3128',
        'https': 'http://adminproxy:e0oXocf7PsTAfdcadNMBEoOohXHCfU2V@62.60.135.92:3128'
    },
    {
        'http': 'http://adminproxy:e0oXocf7PsTAfdcadNMBEoOohXHCfU2V@62.60.135.89:3128',
        'https': 'http://adminproxy:e0oXocf7PsTAfdcadNMBEoOohXHCfU2V@62.60.135.89:3128'
    },
    {
        'http': 'http://adminproxy:e0oXocf7PsTAfdcadNMBEoOohXHCfU2V@62.60.135.57:3128',
        'https': 'http://adminproxy:e0oXocf7PsTAfdcadNMBEoOohXHCfU2V@62.60.135.57:3128'
    }
]

# URL to test against
url = 'https://jsonip.com'

for proxy in proxies:
    try:
        response = requests.get(url, proxies=proxy)
        
        print(response.json())
    except Exception as e:
        print(f"Proxy {proxy['http']} encountered an error: {str(e)}")
