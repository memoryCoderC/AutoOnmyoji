from ctypes import windll
from sys import executable, version_info


def is_admin():
    try:
        return windll.shell32.IsUserAnAdmin()
    except:
        return False


def check_get_permission():
    if is_admin():
        return True  # 将要运行的代码加到这里
    else:
        apply_permission()


def apply_permission():
    if version_info[0] == 3:
        windll.shell32.ShellExecuteW(None, "runas", executable, __file__, None, 1)
    else:  # in python2.x
        from numpy import unicode
        windll.shell32.ShellExecuteW(None, u"runas", unicode(executable), unicode(__file__), None, 1)
    exit(0)
