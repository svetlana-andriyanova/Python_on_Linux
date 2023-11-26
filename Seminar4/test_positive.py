import yaml
from checkers import ssh_checkout, ssh_get

with open('config.yaml') as f:
    data = yaml.safe_load(f)


class TestPositive:
    def test_step1(self, make_folder, clear_folder, make_files):
        result1 = ssh_checkout(data['host'], data['login'], data['passwd'],
                               'cd {}; 7z a {}/arx2 -t{}'.format(data['folder_in'], data['folder_out'], data['type']),
                               'Everything is Ok')
        result2 = ssh_checkout(data['host'], data['login'], data['passwd'], 'cd {}; ls'.format(data['folder_out']),
                               'arx2.{}'.format(data['type']))
        assert result1 and result2, 'test1 Fail'

    def test1_hash(self, clear_folder, make_files):
        res = []
        for i in make_files:
            res.append(
                ssh_checkout(data['host'], data['login'], data['passwd'], "cd {}; 7z h {}".format(data['folder_in'], i),
                             'Everything is Ok'))
            hash = ssh_get(data['host'], data['login'], data['passwd'],
                           'cd {}; crc32 {}'.format(data['folder_in'], i)).upper()
            res.append(
                ssh_checkout(data['host'], data['login'], data['passwd'], 'cd {}; 7z h {}'.format(data['folder_in'], i),
                             hash))
        assert all(res), 'test1_hash'

    def test_step2(self, clear_folder, make_files):
        res = []
        res.append(ssh_checkout(data['host'], data['login'], data['passwd'],
                                'cd {}; 7z a {}/arx2 -t{}'.format(data['folder_in'], data['folder_out'], data['type']),
                                'Everything is Ok'))
        res.append(ssh_checkout(data['host'], data['login'], data['passwd'],
                                'cd {}; 7z e arx2.{} -o{} -y'.format(data['folder_out'], data['type'],
                                                                     data['folder_ext']),
                                'Everything is Ok'))
        for i in make_files:
            res.append(ssh_checkout(data['host'], data['login'], data['passwd'], 'ls {}'.format(data['folder_ext']), i))
        assert all(res), 'test2 Fail'

    def test_step3(self):
        assert ssh_checkout(data['host'], data['login'], data['passwd'],
                            'cd {}; 7z t arx2.{}'.format(data['folder_out'], data['type']),
                            'Everything is Ok'), 'test3 Fail'

    def test_step4(self):
        assert ssh_checkout(data['host'], data['login'], data['passwd'],
                            'cd {}; 7z u {}/arx2.{}'.format(data['folder_in'], data['folder_out'], data['type']),
                            'Everything is Ok'), 'test4 Fail'

    def test_step5(self, clear_folder, make_files):
        res = []
        res.append(ssh_checkout(data['host'], data['login'], data['passwd'],
                                'cd {}; 7z a {}/arx2 -t{}'.format(data['folder_in'], data['folder_out'], data['type']),
                                'Everything is Ok'))
        for i in make_files:
            res.append(
                ssh_checkout(data['host'], data['login'], data['passwd'],
                             'cd {}; 7z l arx2.{}'.format(data['folder_out'], data['type']),
                             i))
        assert all(res), 'test5 FAIL'

    def test_step6(self, clear_folder, make_files, make_subfolder):
        res = []
        res.append(ssh_checkout(data['host'], data['login'], data['passwd'],
                                'cd {}; 7z a {}/arx2 -t{}'.format(data['folder_in'], data['folder_out'], data['type']),
                                'Everything is Ok'))
        res.append(ssh_checkout(data['host'], data['login'], data['passwd'],
                                'cd {}; 7z x arx2.{} -o{} -y'.format(data['folder_out'], data['type'],
                                                                     data['folder_ext2']),
                                'Everything is Ok'))
        for i in make_files:
            res.append(
                ssh_checkout(data['host'], data['login'], data['passwd'], 'ls {}'.format(data['folder_ext2']), i))
        res.append(ssh_checkout(data['host'], data['login'], data['passwd'], 'ls {}'.format(data['folder_ext2']),
                                make_subfolder[0]))
        res.append(ssh_checkout(data['host'], data['login'], data['passwd'],
                                'ls {}/{}'.format(data['folder_ext2'], make_subfolder[0]),
                                make_subfolder[1]))
        assert all(res), 'test6 FAIL'

    def test_step7(self):
        assert ssh_checkout(data['host'], data['login'], data['passwd'],
                            'cd {}; 7z d arx2.{}'.format(data['folder_out'], data['type']),
                            'Everything is Ok'), 'test7 Fail'
