import string
import random
import pytest
import yaml
from datetime import datetime
from checkers import hash_func, ssh_checkout, ssh_get
from upload_files import upload_files

with open('config.yaml') as f:
    data = yaml.safe_load(f)


@pytest.fixture()
def make_folder():
    return ssh_checkout(data['host'], data['login'], data['passwd'],
                        'mkdir {} {} {} {}'.format(data['folder_in'], data['folder_out'], data['folder_ext'],
                                                   data['folder_ext2']), '')


@pytest.fixture()
def clear_folder():
    return ssh_checkout(data['host'], data['login'], data['passwd'],
                        'rm -rf {}/* {}/* {}/* {}/*'.format(data['folder_in'], data['folder_out'], data['folder_ext'],
                                                            data['folder_ext2']), '')


@pytest.fixture()
def make_files():
    list_off_files = []
    for i in range(data['count']):
        filename = ''.join(random.choices(string.ascii_uppercase + string.digits, k=5))
        if ssh_checkout(data['host'], data['login'], data['passwd'],
                        'cd {};  dd if=/dev/urandom of={} bs={} count=1 iflag=fullblock'.format(data['folder_in'],
                                                                                                filename,
                                                                                                data['bs']), ''):
            list_off_files.append(filename)
    return list_off_files


@pytest.fixture()
def make_subfolder():
    testfilename = ''.join(random.choices(string.ascii_uppercase + string.digits, k=5))
    subfoldername = ''.join(random.choices(string.ascii_uppercase + string.digits, k=5))
    if not ssh_checkout(data['host'], data['login'], data['passwd'],
                        'cd {}; mkdir {}'.format(data['folder_in'], subfoldername), ''):
        return None, None
    if not ssh_checkout(data['host'], data['login'], data['passwd'],
                        'cd {}/{}; dd if=/dev/urandom of={} bs=1M count=1 iflag=fullblock'.format(data['folder_in'],
                                                                                                  subfoldername,
                                                                                                  testfilename), ''):
        return subfoldername, None
    else:
        return subfoldername, testfilename


@pytest.fixture(autouse=True, scope='module')
def make_bad_arx():
    ssh_checkout(data['host'], data['login'], data['passwd'],
                 'cd {}; 7z a {}/bad_arx'.format(data['folder_in'], data['folder_out']),
                 'Everything is Ok')
    ssh_checkout(data['host'], data['login'], data['passwd'], 'truncate -s 1 {}/bad_arx.7z'.format(data['folder_out']),
                 '')

#ДЗ4 Загрузка логов.
@pytest.fixture(autouse=True)
def stat():
    stat = ssh_get(data['host'], data['login'], data['passwd'], "cat /proc/loadavg")
    hash_func("echo 'From /proc/loadavg:\nTime: {} count: {} size: {} load: {}'>> stat.txt".format(
        datetime.now().strftime('%H:%M:%S.%f'),
        data['count'], data['bs'], stat))
    with open('stat.txt', 'a') as f:
        stat_ssh = ssh_get(data['host'], data['login'], data['passwd'],
                           "journalctl --since '{}'".format(datetime.now().strftime('%Y-%m-%d %H:%M:%S')))
        f.write(f'Journal of logs:\n{stat_ssh}')


@pytest.fixture(autouse=True)
def print_time():
    print('Start: {}'.format(datetime.now().strftime('%H:%M:%S.%f')))
    yield
    print('Finish: {}'.format(datetime.now().strftime('%H:%M:%S.%f')))


@pytest.fixture(autouse=True, scope='module')
def deploy():
    res = []
    upload_files(data['host'], data['login'], data['passwd'], "/home/user/p7zip-full.deb", "/home/user2/p7zip-full.deb")
    res.append(ssh_checkout(data['host'], data['login'], data['passwd'],
                            "echo '2222' | sudo -S dpkg -i /home/user2/p7zip-full.deb",
                            'Настраивается пакет'))
    res.append(ssh_checkout(data['host'], data['login'], data['passwd'], "echo '2222' | sudo -S dpkg -s p7zip-full",
                            'Status: install ok installed'))
    print(f'{res}')
    return all(res)

#ДЗ4 Установка crc32
@pytest.fixture(autouse=True, scope='module')
def deploy_apt():
    res = []

    res.append(ssh_checkout(data['host'], data['login'], data['passwd'],
                            "echo '2222' | sudo -S apt install libarchive-zip-perl",
                            'Настраивается пакет'))
    res.append(
        ssh_checkout(data['host'], data['login'], data['passwd'], "echo '2222' | sudo -S apt list libarchive-zip-perl",
                     'установлен'))
    print(f'{res}')
    return all(res)
