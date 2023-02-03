import requests

url = 'https://item.taobao.com/item.htm?id=649820697321&ali_refid=a3_430582_1006:1377200012:N:h3Xlj6rOOjyiJDcV2Dtgpn2trDRs9%2Fqc:d1ac90ad770f8b2070d0ca0d21b6726b&ali_trackid=1_d1ac90ad770f8b2070d0ca0d21b6726b&spm=a230r.1.14.3#detail'
headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:109.0) Gecko/20100101 Firefox/109.0",
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8",
    "Accept-Language": "zh-CN,zh;q=0.8,zh-TW;q=0.7,zh-HK;q=0.5,en-US;q=0.3,en;q=0.2",
    "Accept-Encoding": "gzip, deflate, br",
    "Referer": "https://s.taobao.com/",
    "Connection": "keep-alive",
    "Cookie": "miid=58187891350589861; t=89b4ce3f3cf5f4be110cd1c2ab56cd9f; cna=fqlBHOX8lFIBASQJilVEs+4c; isg=BBMTQO-ddOHnxDjUDh8821gzoZc9yKeKOftjWcUw-jJpRDLmTJl_2yPeejQqf_-C; l=fBOqArolTlmsKdFbBO5BEurza77tgIR48kPzaNbMiIEGa1oh6FGG4NCeIkOWJdtfgT5DAeKrVsSi6d3k-4U38AOhfIVrOC0eQg968etzRyMc.; tfstk=c8yVBFtJOtBVwkwrdYDaTcW03BpAavuiRLoEiNaj1pHwighr7sqkW0xTW0ow4Fcc.; sgcookie=E100gxvuf1wtnKvAWSstyMOmCeQqCKP0A6Q7eT0CDQGgfPMrv3IejZt9ATizbIgzWkuLU1DReMja2cSIeORIwF0qZWlST5Zo3NrQ14LqJYfylZo%3D; uc3=vt3=F8dCvjIRWrlTpH4o0o4%3D&id2=UU2w5i%2BWehFvzg%3D%3D&nk2=05SrVV98BFtwfA%3D%3D&lg2=WqG3DMC9VAQiUQ%3D%3D; lgc=%5Cu9738%5Cu6C14%5Cu7684%5Cu9F99%5Cu53D4; uc4=id4=0%40U2%2F301n2q%2Fn1XZ2bupitJh4j85OZ&nk4=0%400S%2FTDglR3XLlerFViO4UQn3czz1R; tracknick=%5Cu9738%5Cu6C14%5Cu7684%5Cu9F99%5Cu53D4; _cc_=URm48syIZQ%3D%3D; thw=cn; tk_trace=oTRxOWSBNwn9dPyorMJE%2FoPdY8zMG1aAN%2F0TkjYGZjkj6rrK3kv4LgxGhtlxvv5DK7siwhr9c%2BstdFdCVk5KEMg7W1c2qo%2FVPg1UYbbIL8UG4AGgqkg2yLJ3S5fPQkVk611ihRo%2ByilOcKXggOoNpLJmGqrKS7S%2FlAfRmvbeOsqhZPjfLp5IFl8Hro2PhPx8Iu1%2Brj3g8oM%2FP5iQq9G1Zrayskg%2FX%2Be0LndkmUTB1aiOcumjpTVKnxYz%2Fn4idqBLMH1X5Cd5TAT65RXTpSkNzY0AOm6XH0Pem2%2F4RRnqUORK%2FM8hOZMgPYk7SWZLqqEPX5nbgmZdTsV9Lo06857sssctUQxPR44qVFbHzqexkJG4joKESCvNm8rXBp00mhxh22NcRXdgU9K4q4YpfcqR%2B6K%2BpVYF3A%3D%3D; cookie2=16a207d1b2645720a55f4158df6c9e43; _tb_token_=edb0ba7e3377e; _samesite_flag_=true; csg=fa38e0e4; cancelledSubSites=empty; dnk=%5Cu9738%5Cu6C14%5Cu7684%5Cu9F99%5Cu53D4; skt=e84136be022bf756; existShop=MTY3NTM0MzQzMg%3D%3D; uc1=cookie15=VFC%2FuZ9ayeYq2g%3D%3D&cookie14=UoezSgXGf%2FUg1A%3D%3D&cookie16=U%2BGCWk%2F74Mx5tgzv3dWpnhjPaQ%3D%3D&existShop=false&pas=0&cookie21=UtASsssmeW6lpyd%2BB%2B3t; v=0; mt=ci=-1_0; _m_h5_tk=fffe43bf084019558292931f10871784_1675352798409; _m_h5_tk_enc=fe62f1e0e1846a9c3c77aab867a79536; xlly_s=1; unb=2528679550; cookie17=UU2w5i%2BWehFvzg%3D%3D; _l_g_=Ug%3D%3D; sg=%E5%8F%9408; _nk_=%5Cu9738%5Cu6C14%5Cu7684%5Cu9F99%5Cu53D4; cookie1=B0BQ1OA8SD%2B4rdjFt6hT2qckqW8ReDEHniyKqWK4Piw%3D",
    "Upgrade-Insecure-Requests": "1",
    "Sec-Fetch-Dest": "document",
    "Sec-Fetch-Mode": "navigate",
    "Sec-Fetch-Site": "same-site",
    "Sec-Fetch-User": "?1",
    "Pragma": "no-cache",
    "Cache-Control": "no-cache",
    "TE": "trailers"
    }

html = requests.get(url, headers=headers)
with open('./resource/test.html', 'w', encoding='utf-8') as f:
    f.write(html.text)
print(html.text)

html.close()