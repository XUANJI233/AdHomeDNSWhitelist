
# SwitchyOmega-Whitelist
适用于 AdGuard Home 的中国网站白名单,使用脚本添加进`AdGuardHome.yaml`,因为使用配置文件设置的上游dns会失效。

参考脚本
```
#!/bin/bash

# 定义需要修改的配置文件路径
config_file_path="/opt/1panel/apps/adguardhome/adguardhome/data/conf/AdGuardHome.yaml"

# 定义网络地址前缀   
url_prefixes=(
"https://raw.gitmirror.com/"
"https://mirror.ghproxy.com/https://raw.githubusercontent.com/"
"https://ghproxy.net/https://raw.githubusercontent.com/"
"https://ghproxy.com/https://raw.githubusercontent.com/"
"https://gh-proxy.com/https://raw.githubusercontent.com/")

file_path="XUANJI233/SwitchyOmega-Whitelist/master/white-list.sorl"

# 使用curl下载文件，如果失败则尝试其他URL
download_success=false
for url_prefix in "${url_prefixes[@]}"; do
    if curl -f -o "temp_download_file" "${url_prefix}${file_path}"; then
        echo "Downloaded from ${url_prefix}${file_path}"
        download_success=true
        break
    else
        echo "Failed to download from ${url_prefix}${file_path}, trying next URL..."
    fi
done

if ! $download_success; then
    echo "All downloads failed."
    exit 1
fi

# 提取最后一行
last_line=$(tail -n 1 "temp_download_file")

# 找到定位的行数
line_number=$(grep -n 'upstream_dns_file: ""' "$config_file_path" | cut -d : -f 1)

# 分割文件并在中间插入新的内容
head -n $(($line_number - 1)) "$config_file_path" > temp.txt
echo "$last_line" >> temp.txt
tail -n +$(($line_number + 1)) "$config_file_path" >> temp.txt

# 将临时文件替换原文件
#sudo docker stop adguardhome
sudo mv temp.txt "$config_file_path"
#sudo docker start adguardhome
```

主要内容来自 [felixonmars/dnsmasq-china-list](https://github.com/felixonmars/dnsmasq-china-list)，纯列表，自动更新。


    ```
    https://raw.githubusercontent.com/XUANJI233/SwitchyOmega-Whitelist/master/white-list.sorl
    ```
    
代理加速 (一个一个试):

> 1. https://ghproxy.com/https://raw.githubusercontent.com/XUANJI233/SwitchyOmega-Whitelist/master/white-list.sorl
  
> 2. https://mirror.ghproxy.com/https://raw.githubusercontent.com/XUANJI233/SwitchyOmega-Whitelist/master/white-list.sorl
   
> 3. https://ghproxy.net/https://raw.githubusercontent.com/XUANJI233/SwitchyOmega-Whitelist/master/white-list.sorl
