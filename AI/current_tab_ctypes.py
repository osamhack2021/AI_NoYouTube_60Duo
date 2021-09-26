import time, ctypes

time.sleep(3)    # 타이틀을 가져오고자 하는 윈도우를 활성화 하기위해 의도적으로 3초 멈춥니다. 

lib = ctypes.windll.LoadLibrary('user32.dll')
handle = lib.GetForegroundWindow()    # 활성화된 윈도우의 핸들얻음
buffer = ctypes.create_unicode_buffer(255)    # 타이틀을 저장할 버퍼
lib.GetWindowTextW(handle, buffer, ctypes.sizeof(buffer))    # 버퍼에 타이틀 저장

print(buffer.value)    # 버퍼출력
