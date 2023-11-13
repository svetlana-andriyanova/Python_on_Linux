import subprocess

def execute_command(cmd, text):
    result = subprocess.run(cmd, shell=True, stdout=subprocess.PIPE, encoding="utf-8")
    if result.returncode == 0 and text in result.stdout:
        return True
    else:
        return False

if __name__ == '__main__':
    print(execute_command('ls /home/user', 'Видео'))
    print(execute_command('ls --help', 'Выдаёт информацию о ФАЙЛАХ'))
    print(execute_command('cat /etc/os-release', 'Страница'))