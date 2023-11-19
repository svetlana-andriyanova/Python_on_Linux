import subprocess

def checkout(cmd, text):
    result = subprocess.run(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, encoding="utf-8")
    if (text in result.stdout or text in result.stderr) and result.returncode != 0:
        return True
    else:
        return False


out = "/home/user/out"
folder1 = "/home/user/folder1"


# def test_step1():
#     # test1 ======== take docs from folder: out and copy this docs to folder1
#     result = checkout("cd /home/user/out; 7z e bad_arx.7z -o/home/user/folder1 -y", "ERRORS")
#     assert result, "Test1 FAIL"
#
# def test_step2():
#     # test1 =========show info about arx2.7z
#     assert checkout("cd /home/user/out; 7z t bad_arx.7z", "ERRORS"), "Test2 FAIL"
#

def test_step1():
    # test1 ======== take docs from folder: out and copy this docs to folder1
    assert checkout("cd {}; 7z e bad_arx.7z -o{} -y".format(out, folder1), "ERRORS"), "Test1 FAIL"


def test_step2():
    # test2 =========show info about arx2.7z
    assert checkout("cd {}; 7z t bad_arx.7z".format(out), "ERRORS"), "Test2 FAIL"