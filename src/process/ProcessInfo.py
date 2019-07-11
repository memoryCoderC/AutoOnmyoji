import os

import psutil


def get_all_process():
    """
    获取全部进程信息
    :return: list
    """
    _pids = psutil.pids()
    for pid in _pids:
        p = psutil.Process(pid)
        print('pid-%s,pname-%s' % (pid, p.name()))
        # if p.name() == 'dllhost.exe':
        #     cmd = 'taskkill /F /IM dllhost.exe'
        #     os.system(cmd)


def is_running(process_name):
    try:
        process = len(os.popen('tasklist | findstr ' + process_name).readlines())
        if process >= 1:
            return True
        else:
            return False
    except:
        print("程序错误")
        return False


if __name__ == '__main__':
    is_running("onmyoji.exe")
