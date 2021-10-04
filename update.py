import os
import requests
import tarfile, csv
import re


def untar(fname, dirs):
    """
    解压tar.gz文件
    :param fname: 压缩文件名
    :param dirs: 解压后的存放路径
    :return: bool
    """
    try:
        t = tarfile.open(fname)
        t.extractall(path=dirs)
        return True
    except Exception as e:
        print(e)
        return False


def mkcsv(package, local_ver, aur_ver=None):
    pass


def match_packages(package):
    if 'git' in package:
        # print("name:" + "^([a-z]+\d*-?)+[git]?|[a-z]")
        pkgname = re.search('^([a-z]+\d*-?)+[git]|[a-z]', package).group()
    else:
        # print("name:" + "^([a-z]+\d*-?)+[git]|[a-z]")
        pkgname = re.search('^([a-z]+\d*-?)+[a-z]', package).group()
    # print(pkgname)
    package = package[len(pkgname):]
    # print(str)

    # print("ver:" + "(\d+.|\w)+-?\w")
    pkgver = re.search('(\d+.|\w)+-?\w', package).group()
    # print(pkgver)
    # print(re.match('^[a-z-]+',str))
    return pkgname, pkgver


# 检测版本是否相同
def check_verson(pkgname, pkgver):
    req = requests.get(
        url='https://aur.tuna.tsinghua.edu.cn/rpc/?v=5&type=info&arg=' + pkgname).json()
    if req['resultcount'] == 0:
        print('未在aur找到' + pkgname + '相关软件！')
    else:
        aur_ver = req['results'][0]['Version']
        # print(aur_ver)
        if aur_ver == pkgver:
            print(pkgname + ' 版本一致！')
            return None
        elif pkgver > aur_ver:
            print(pkgname + ' 自建仓库版本： ' + pkgver + '  比aur版本： ' + aur_ver + ' 新！')
            return None
        else:
            print(pkgname + ' 需要更新！')
            return aur_ver


# untar('aa.tar.gz', './')
if __name__ == '__main__':
    url = 'https://arch.xmengnet.cn/'  # 仓库地址
    filename = 'xmengnet.db.tar.gz'  # 数据库文件
    db_dir = 'xmengnet.db'  # 解压文件夹
    # print(url + filename)
    if not os.path.exists(filename):
        db = requests.get(url + filename, stream=True)
        with open(filename, 'wb') as file:
            file.write(db.content)
        os.mkdir(db_dir)
        untar(filename, './' + db_dir)

    # os.system("ls ./")
    packages = os.listdir('./' + db_dir)
    print(packages)
    package_info = 'package_info.csv'
    if os.path.exists(package_info):
        os.remove(package_info)
    csvFile = open("package_info.csv", "w+")  # 创建csv文件

    file_header = ['package_name', 'repo_ver', 'aur_ver']
    writer = csv.writer(csvFile)

    writer.writerow(file_header)

    for i in packages:
        pkgname, pkgver = match_packages(i)
        # print('package:' + i + '\n' + 'pkgname:' + pkgname + '\t' + 'pkgver:' + pkgver)
        aur_ver = check_verson(pkgname, pkgver)
        info = [pkgname, pkgver, aur_ver]
        writer.writerow(info)
    csvFile.close()
