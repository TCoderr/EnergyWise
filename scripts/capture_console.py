"""Run app.py in a REAL Windows console window, type answers into THAT console only (WriteConsoleInputW, no
global SendKeys), then capture the window (PrintWindow) and the console text buffer.
Output: reports/console_screenshot.png, reports/console_transcript.txt
Run: .venv/Scripts/python scripts/capture_console.py
"""
import ctypes
import subprocess
import sys
import time
from ctypes import wintypes as W
from pathlib import Path

from PIL import Image

ROOT = Path(__file__).resolve().parent.parent
k32, u32, g32 = ctypes.WinDLL('kernel32', use_last_error=True), ctypes.WinDLL('user32'), ctypes.WinDLL('gdi32')
ANSWERS = ['1', 'abc', '1', '2', '0,25', '3']   # menu, invalid input, shape, orientation, glazing, distribution
TITLE = 'EnergyWise - konsol demo'


class KEY_EVENT_RECORD(ctypes.Structure):
    _fields_ = [('bKeyDown', W.BOOL), ('wRepeatCount', W.WORD), ('wVirtualKeyCode', W.WORD),
                ('wVirtualScanCode', W.WORD), ('uChar', W.WCHAR), ('dwControlKeyState', W.DWORD)]


class INPUT_RECORD(ctypes.Structure):
    class _U(ctypes.Union):
        _fields_ = [('KeyEvent', KEY_EVENT_RECORD), ('_pad', ctypes.c_byte * 16)]
    _fields_ = [('EventType', W.WORD), ('Event', _U)]


def children(pid):
    out = subprocess.run(['powershell', '-NoProfile', '-Command',
                          f'(Get-CimInstance Win32_Process -Filter "ParentProcessId={pid}").ProcessId'],
                         capture_output=True, text=True).stdout.split()
    return [int(x) for x in out]


def find_console_window(pids):
    found = []
    @ctypes.WINFUNCTYPE(W.BOOL, W.HWND, W.LPARAM)
    def cb(hwnd, _):
        pid = W.DWORD(); u32.GetWindowThreadProcessId(hwnd, ctypes.byref(pid))
        cls = ctypes.create_unicode_buffer(64); u32.GetClassNameW(hwnd, cls, 64)
        if pid.value in pids and cls.value == 'ConsoleWindowClass' and u32.IsWindowVisible(hwnd):
            found.append(hwnd)
        return True
    u32.EnumWindows(cb, 0)
    return found[0] if found else None


def type_line(conin, text):
    recs = []
    for ch in text + '\r':
        vk = 0x0D if ch == '\r' else 0
        for down in (True, False):
            r = INPUT_RECORD(); r.EventType = 1
            r.Event.KeyEvent = KEY_EVENT_RECORD(down, 1, vk, 0, ch, 0)
            recs.append(r)
    arr = (INPUT_RECORD * len(recs))(*recs); written = W.DWORD()
    if not k32.WriteConsoleInputW(conin, arr, len(recs), ctypes.byref(written)):
        raise OSError(ctypes.get_last_error())


def read_buffer(conout, cols, rows):
    buf = ctypes.create_unicode_buffer(cols * rows); n = W.DWORD()
    k32.ReadConsoleOutputCharacterW(conout, buf, cols * rows, 0, ctypes.byref(n))
    lines = [buf.value[i:i + cols].rstrip() for i in range(0, n.value, cols)]
    while lines and not lines[-1]:
        lines.pop()
    return '\n'.join(lines)


def capture(hwnd, path):
    rect = W.RECT(); u32.GetWindowRect(hwnd, ctypes.byref(rect))
    w, h = rect.right - rect.left, rect.bottom - rect.top
    hdc = u32.GetWindowDC(hwnd); mdc = g32.CreateCompatibleDC(hdc); bmp = g32.CreateCompatibleBitmap(hdc, w, h)
    g32.SelectObject(mdc, bmp)
    ok = u32.PrintWindow(hwnd, mdc, 2)   # PW_RENDERFULLCONTENT: works even if the window is covered
    class BMI(ctypes.Structure):
        _fields_ = [('biSize', W.DWORD), ('biWidth', W.LONG), ('biHeight', W.LONG), ('biPlanes', W.WORD), ('biBitCount', W.WORD),
                    ('biCompression', W.DWORD), ('biSizeImage', W.DWORD), ('biXPelsPerMeter', W.LONG), ('biYPelsPerMeter', W.LONG),
                    ('biClrUsed', W.DWORD), ('biClrImportant', W.DWORD)]
    bmi = BMI(ctypes.sizeof(BMI), w, -h, 1, 32, 0, 0, 0, 0, 0, 0)
    data = ctypes.create_string_buffer(w * h * 4)
    g32.GetDIBits(mdc, bmp, 0, h, data, ctypes.byref(bmi), 0)
    g32.DeleteObject(bmp); g32.DeleteDC(mdc); u32.ReleaseDC(hwnd, hdc)
    Image.frombuffer('RGBA', (w, h), data, 'raw', 'BGRA', 0, 1).convert('RGB').save(path)
    return ok, (w, h)


def main():
    u32.SetProcessDPIAware()   # otherwise GetWindowRect returns scaled (logical) size and the capture is cropped
    # launcher .cmd avoids Popen's \" quoting, which cmd.exe does not understand
    host = subprocess.Popen(['conhost.exe', 'cmd.exe', '/k', str(ROOT / 'scripts' / 'run_app_console.cmd')])
    time.sleep(4)
    pids = {host.pid, *children(host.pid)}
    hwnd = find_console_window(pids)
    shell_pids = children(host.pid)
    if not hwnd or not shell_pids:
        host.kill(); sys.exit(f'console window not found (pids={pids})')
    k32.FreeConsole()
    if not k32.AttachConsole(shell_pids[0]):
        host.kill(); sys.exit(f'AttachConsole failed: {ctypes.get_last_error()}')
    GENERIC_RW, SHARE, OPEN = 0xC0000000, 3, 3
    conin = k32.CreateFileW('CONIN$', GENERIC_RW, SHARE, None, OPEN, 0, None)
    conout = k32.CreateFileW('CONOUT$', GENERIC_RW, SHARE, None, OPEN, 0, None)
    class SMALL_RECT(ctypes.Structure):
        _fields_ = [('Left', W.SHORT), ('Top', W.SHORT), ('Right', W.SHORT), ('Bottom', W.SHORT)]
    full = SMALL_RECT(0, 0, 89, 39)   # show the whole 90x40 buffer (mode con sets the buffer, not always the window)
    if not k32.SetConsoleWindowInfo(conout, True, ctypes.byref(full)):
        print('SetConsoleWindowInfo failed:', ctypes.get_last_error())
    time.sleep(2)  # wait for the model to load and the menu to appear
    for a in ANSWERS:
        type_line(conin, a); time.sleep(0.8)
    time.sleep(1.5)
    ok, size = capture(hwnd, ROOT / 'reports' / 'console_screenshot.png')
    text = read_buffer(conout, 90, 300)
    type_line(conin, 'q'); time.sleep(1.5)
    final = read_buffer(conout, 90, 300)
    (ROOT / 'reports' / 'console_transcript.txt').write_text(
        '# Gerçek konsol çalıştırması (conhost.exe + cmd.exe, app.py). Girdiler WriteConsoleInputW ile bu konsola yazıldı.\n'
        f'# Tarih: {time.strftime("%Y-%m-%d %H:%M:%S")}\n# Girdiler: {ANSWERS + ["q"]}\n\n' + final + '\n', encoding='utf-8')
    type_line(conin, 'exit'); time.sleep(1)
    k32.FreeConsole()
    try:
        host.wait(timeout=5)
    except subprocess.TimeoutExpired:
        host.kill()
    print('PrintWindow ok:', bool(ok), 'size:', size, '| prediction lines:', text.count('Tahmini ısıtma yükü'))


if __name__ == '__main__':
    main()
