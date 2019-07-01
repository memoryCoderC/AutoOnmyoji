from win32gui import *

titles = set()


def foo(hwnd, mouse):
    # 去掉下面这句就所有都输出了，但是我不需要那么多
    if IsWindow(hwnd) and IsWindowEnabled(hwnd) and IsWindowVisible(hwnd):
        titles.add(GetWindowText(hwnd))


if __name__ == '__main__':
    EnumWindows(foo, 0)
    lt = [t for t in titles if t]
    for t in lt:
        print(t)

if __name__ == '__main__':
    EnumWindows(foo, 0)
    lt = [t for t in titles if t]
    for t in lt:
        print(t)
