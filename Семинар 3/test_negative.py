import subprocess
import pytest
import yaml
from checkers import checkout_negative

with open('config.yaml') as f:
    data = yaml.safe_load(f)


class TestNegative:
    def test_step1(self):
        result1 = checkout_negative('cd {}; 7z e bad_arx.7z -o{} -y'.format(data['folder_out'], data['folder_ext']),
                                    'ERRORS')
        assert result1, 'test2 Fail'

    def test_step2(self):
        assert checkout_negative('cd {}; 7z t bad_arx.7z'.format(data['folder_out']), 'ERRORS'), 'test2 Fail'
