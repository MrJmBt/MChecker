import requests, os, shutil
from bs4 import BeautifulSoup as bs
from concurrent.futures import ThreadPoolExecutor

try: shutil.rmtree(
    'get_proxy/__pycache__'
  )
except: pass

proxy_list = []
valid_proxy = []

def prox():
    return proxy_net()

def proxy_checker(prox):
  try:
    global valid_proxy
    if requests.get(
       'http://ip.ml.youngjoygame.com:30220/myip',
          verify=False,
          proxies=prox,
          timeout=10
        ).status_code == 200:
      valid_proxy.append(
        prox
      )
    print(
      end='\r[*] Found (%s) valid proxy.'%(
        len(
          valid_proxy
        )
      ),
      flush=True
    )
  except: pass

def proxy_net():
  print(
    '[*] Searching proxy...'
  )
  r = requests.get(
    'https://free-proxy-list.net/',
    headers={'user-agent':'chrome'}
  ).text
  soup = bs(
    r,
    'html.parser'
  )
  proxs = soup.find(
    'textarea'
  ).text.split(
    '\n'
  )
  [
    proxy_list.append({
      'http':'http://'+e.strip(),
      'https':'https://'+e.strip()
    }) if len(
      e.strip(
      ).split(
        ':'
      )
    ) == 2 else None for e in proxs
  ]
  if len(
    proxy_list
  ) != 0:
    with ThreadPoolExecutor(
      max_workers=50
      ) as thread:
      [
        thread.submit(
          proxy_checker,(
            prox
          )
        ) for prox in proxy_list
      ]
    if len(
      valid_proxy
    ) != 0:
      print(
        '\n'
      )
      return valid_proxy
    else: exit(
      '[!] Maaf tidak ada proxy yang valid silahkan coba lagi :('
    )
  else: exit(
    '[!] Maaf proxy tidak ada :('
  )
