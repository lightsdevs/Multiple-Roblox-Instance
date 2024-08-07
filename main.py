import pygame
import sys
import ctypes
import os

def resource_path(relative_path):
    try:
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")

    return os.path.join(base_path, relative_path)

class Singleton:
    def create_mutex(mutex_name):
        ERROR_ALREADY_EXISTS = 396
        kernel32 = ctypes.WinDLL('kernel32', use_last_error=True)
        mutex_handle = kernel32.CreateMutexW(None, False, mutex_name)
        if mutex_handle is None:
            raise ctypes.WinError(ctypes.get_last_error())
        if ctypes.get_last_error() == ERROR_ALREADY_EXISTS:
            print(f"Mutex '{mutex_name}' already exists.")
            return False
        print(f"Mutex '{mutex_name}' created successfully.")
        return True
    def release_mutex(mutex_name):
        kernel32 = ctypes.WinDLL('kernel32', use_last_error=True)
        mutex_handle = kernel32.OpenMutexW(0x1F0001, False, mutex_name)  # MUTEX_ALL_ACCESS
        if mutex_handle is None:
            raise ctypes.WinError(ctypes.get_last_error())
        result = kernel32.ReleaseMutex(mutex_handle)
        if not result:
            raise ctypes.WinError(ctypes.get_last_error())
        kernel32.CloseHandle(mutex_handle)
        print(f"Mutex '{mutex_name}' released successfully.")

def render():
    try:
        Singleton.release_mutex("ROBLOX_singletonEvent") # release mutex if it exists
    except:
        pass
    Singleton.create_mutex("ROBLOX_singletonEvent") # create anti roblox mutex
    pygame.init()
    size = (200, 200)
    screen = pygame.display.set_mode(size)
    pygame.display.set_caption('Multi Roblox')
    image = pygame.image.load(resource_path('mr.png'))
    running = True
    screen.fill((0, 0, 0))
    screen.blit(image, (0, 0))
    pygame.display.flip()
    clock  = pygame.time.Clock()
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
        clock.tick(5)
        
    pygame.quit()
    sys.exit()

def main():
    render()

if __name__ == "__main__":
    main()
