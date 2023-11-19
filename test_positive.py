import subprocess

def checkout(cmd, text):
    result = subprocess.run(cmd, shell=True, stdout=subprocess.PIPE, encoding="utf-8")
    if text in result.stdout and result.returncode == 0:
        return True
    else:
        return False


tst = "/home/user/tst"
out = "/home/user/out"
folder1 = "/home/user/folder1"
folder2 = "/home/user/folder2"


# def test_step1():
#     # test1 =================== create archive
#     assert checkout("cd /home/user/tst; 7z a ../out/arx2", "Everything is Ok"), "Test1 FAIL"
#
#
# def test_step2():
#     # test1 ======== take docs from folder: out and copy this docs to folder1
#     assert checkout("cd /home/user/out; 7z e arx2.7z -o/home/user/folder1 -y", "Everything is Ok"), "Test2 FAIL"
#
#

def test_step1():
    result1 = checkout("cd {}; 7z a {}/arx2".format(tst, out), "Everything is Ok")
    result2 = checkout("cd {}; ls".format(out), "arx2.7z")
    assert result1 and result2, "Test1 FAIL"


def test_step2():
    result1 = checkout("cd {}; 7z e arx2.7z -o{} -y".format(out, folder1), "Everything is Ok")
    result2 = checkout("cd {}; ls".format(folder1), "qw")
    assert result1 and result2, "Test2 FAIL"

def test_step3():

    assert checkout("cd {}; 7z t arx2.7z".format(out), "Everything is Ok"), "Test3 FAIL"


def test_step4():
    # test1 ========= add archive update
    assert checkout("cd {}; 7z u {}arx2.7z".format(tst, out), "Everything is Ok"), "Test4 FAIL"


# def test_step5():
#     # test1 ========= delete docs one and two from archive in folder out
#     assert checkout("cd {}; 7z d arx2.7z".format(out), "Everything is Ok"), "Test5 FAIL"

def test_step6():
    assert checkout(" cd {}; 7z l arx2.7z".format(out), "2 files"), "Test6 FAIL"


def test_step7():
    assert checkout("cd {}; 7z x arx2.7z -o/{} -y".format(out, folder2), "Everything is Ok"), "Test7 FAIL"

def test_step8():
    res = subprocess.run("crc32 /home/user/out/arx2.7z", shell=True, stdout=subprocess.PIPE, encoding='utf-8')
    assert checkout("cd {}; 7z h arx2.7z".format(out), (res.stdout).rstrip().upper()), "test8 FAIL"
