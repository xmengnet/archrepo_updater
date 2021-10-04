import re, requests

# str = 'zsh-theme-powerlevel10k-git-r3931.4f3d2ff-1'
# str = 'aria2-config-script-0.3-1'
# str = 'spotify-adblock-git-1:1.0.0.r6.gd129a8d-1'
str = 'dingtalk-bin-1.0.0.285-1'
if 'git' in str:
    print("name:" + "^([a-z]+\d*-?)+[git]?|[a-z]")
    pkgname = re.search('^([a-z]+\d*-?)+[git]|[a-z]', str).group()
else:
    print("name:" + "^([a-z]+\d*-?)+[a-z]")
    pkgname = re.search('^([a-z]+\d*-?)+[a-z]', str).group()
print(pkgname)
str = str[len(pkgname):]


# print(str)
def check_vesion():
    req = requests.get(
        url='https://aur.tuna.tsinghua.edu.cn/rpc/?v=5&type=info&arg=' + pkgname).json()
    if req['resultcount'] == 0:
        print('未在aur找到相关软件！')
    else:
        aur_ver = req['results'][0]['Version']
        print(aur_ver)
        if aur_ver == pkgver:
            print('版本一致！')
        else:
            print('版本不一致！自建仓库版本：' + pkgver + '  aur版本：' + aur_ver)


print("ver:" + "(\d+.|\w)+-?\w")
pkgver = re.search('(\d+.|\w)+-?\w', str).group()
# print(pkgver)
print(pkgver)
# print(re.match('^[a-z-]+',str))
pkg_list = [pkgname, pkgver]
print(pkg_list)
