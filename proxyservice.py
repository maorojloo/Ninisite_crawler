from fastapi import FastAPI
from typing import Dict
import itertools

app = FastAPI()

# List of proxies
# proxies = [
#     {
#         'http': 'twitter-proxy-twprox2.go-dev.ir:8888',
#         'https': 'twitter-proxy-twprox2.go-dev.ir:8888'
#     },
#     {
#         'http': 'proxy-Aparat-tw.go-dev.ir:8888',
#         'https': 'proxy-Aparat-tw.go-dev.ir:8888'
#     },
#     {
#         'http': 'http://twitter-qute-proxy.go-dev.ir:8888',
#         'https': 'http://twitter-qute-proxy.go-dev.ir:8888'
#     },
#     {
#         'http': 'http://twitter-post-proxy.go-dev.ir:8888',
#         'https': 'http://twitter-post-proxy.go-dev.ir:8888'
#     },
#     {
#         'http': 'http://adminproxy:e0oXocf7PsTAfdcadNMBEoOohXHCfU2V@62.60.135.57:3128',
#         'https': 'http://adminproxy:e0oXocf7PsTAfdcadNMBEoOohXHCfU2V@62.60.135.57:3128'
#     }
# ]




proxies = [
    {
        'http': 'http://twitter-proxy-twprox2.go-dev.ir:8888',
        'https': 'http://twitter-proxy-twprox2.go-dev.ir:8888'
    },
    # {
    #     'http': 'http://proxy-Aparat-tw.go-dev.ir:8888',
    #     'https': 'http://proxy-Aparat-tw.go-dev.ir:8888'
    # },
    {
        'http': 'http://twitter-qute-proxy.go-dev.ir:8888',
        'https': 'http://twitter-qute-proxy.go-dev.ir:8888'
    },
    {
        'http': 'http://twitter-post-proxy.go-dev.ir:8888',
        'https': 'http://twitter-post-proxy.go-dev.ir:8888'
    },

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





 



# Create an iterator for the proxies
proxy_iterator = itertools.cycle(proxies)

@app.get("/get_proxy", response_model=Dict[str, str])
def get_proxy():
    # Get the next proxy in the sequence
    proxy = next(proxy_iterator)
    return proxy

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
