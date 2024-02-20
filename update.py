#!/usr/bin/env python3
'''
@作者: 风沐白
@文件: update.py
@描述: 从网络来源更新白名单规则
'''

import requests
import re
import os
import time

# 默认来源 git@github.com:felixonmars/dnsmasq-china-list.git, 可能需要代理
confurl = 'https://raw.githubusercontent.com/felixonmars/dnsmasq-china-list/master/accelerated-domains.china.conf'

if __name__ == "__main__":
    conffile = 'accelerated-domains.china.conf'
    sorlfile = 'white-list.sorl'
    rules = set()
    up_time = time.ctime()
    headline = ['[SwitchyOmega Conditions]\n',
                '; Require: SwitchyOmega >= 2.3.2\n',
                '; Update @ {}\n'.format(up_time),
                '\n']

    r = requests.get(confurl)
    with open(conffile, 'wb') as f:
        f.write(r.content)

    with open(conffile, 'r') as f:
        for line in f.readlines():
            if line.startswith('#'):
                continue
            match = re.search(r'server=/([^/]+)/', line)
            if match:
                domain = match.group(1)
                rules.add('*.' + domain)

    rules = sorted(rules)  # 按字母顺序排序规则
    # 用转义的反斜杠连接教育网和一般规则，以实现单行格式
    formatted_rules = '[/' + '\\'.join([
        '*.cn', '*.acm.org', '*.dblp.org', '*.ebscohost.com', '*.edu', '*.edu.*', 
        '*.engineeringvillage.com', '*.ieee.org', '*.jstor.org', '*.lexis.com', 
        '*.msftconnecttest.com', '*.nature.com', '*.oclc.org', '*.proquest.com', 
        '*.researchgate.net', '*.sciencedirect.com', '*.sciencemag.org', 
        '*.springer.com', '*.tandfonline.com', '*.uni-trier.de', '*.webofknowledge.com', 
        '*.wiley.com'] + ['*.' + domain for domain in rules]) + '/]TLS://1 TLS://2\n'

    out = headline + [formatted_rules]

    with open(sorlfile, 'w') as f:
        f.writelines(out)

    os.remove(conffile)
