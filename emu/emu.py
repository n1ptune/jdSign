from unicorn import *
from unicorn.arm64_const import *
from capstone import *
table = []
 

def bytes2bin(bytes):
    arr = []
    for v in [m for m in bytes]:
        arr.append(
            [(v & 128) >> 7, (v & 64) >> 6, (v & 32) >> 5, (v & 16) >> 4, (v & 8) >> 3, (v & 4) >> 2, (v & 2) >> 1,
             v & 1])
    return [i for j in arr for i in j]
 
 
def bin2bytes(arr):
    length = len(arr) // 8
    arr1 = [0 for _ in range(length)]
    for j in range(length):
        arr1[j] = arr[j * 8] << 7 | arr[j * 8 + 1] << 6 | arr[j * 8 + 2] << 5 | arr[j * 8 + 3] << 4 | arr[
            j * 8 + 4] << 3 | arr[j * 8 + 5] << 2 | arr[j * 8 + 6] << 1 | arr[j * 8 + 7]
    return bytes(arr1)
 
 
def read(name):
    with open(name, 'rb') as f:
        return f.read()
 

def hook_code(mu, address, size, user_data):
    if address == BASE + 0x17638:
        arr2 = []
        for byte in mu.mem_read(PLAINTEXT_ADDR, 8):
            arr2.append(byte)
        table.append([user_data.index(1), bytes2bin(arr2).index(1)])
 
 
if __name__ == "__main__":
    key0 = b'7d0069660c9b5d32074facf37c3738a1'
    mu = Uc(UC_ARCH_ARM64, CS_MODE_ARM)
    BASE = 0x400000
    STACK_ADDR = 0x0
    STACK_SIZE = 1024 * 2
    PLAINTEXT_ADDR = 1024 * 2
    PLAINTEXT_SIZE = 1024
    KEY_ADDR = 1024 * 3
    KEY_SIZE = 1024

    mu.mem_map(BASE, 1024 * 1024 * 1024)
    mu.mem_map(STACK_ADDR, STACK_SIZE)
    mu.mem_map(PLAINTEXT_ADDR, PLAINTEXT_SIZE)
    mu.mem_map(KEY_ADDR, KEY_SIZE)
    # mu.mem_write(BASE, read("F:\\Code\\Pycharm\\JDSign\\libjdbitmapkit.so"))
    mu.mem_write(BASE, read("./libjdbitmapkit.so"))
    mu.mem_write(KEY_ADDR, key0)
 
    for i in range(64):
        arr1 = [0 for j in range(64)]
        arr1[i] = 1
        h = mu.hook_add(UC_HOOK_CODE, hook_code, arr1)
        mu.reg_write(UC_ARM64_REG_SP, STACK_ADDR + STACK_SIZE - 1)
        mu.mem_write(PLAINTEXT_ADDR, bin2bytes(arr1))
        mu.reg_write(UC_ARM64_REG_X1, KEY_ADDR)
        mu.reg_write(UC_ARM64_REG_X2, 16)
        mu.reg_write(UC_ARM64_REG_X3, PLAINTEXT_ADDR) 
        mu.emu_start(BASE + 0x165e0, BASE + 0x1763c)
        mu.hook_del(h)
    print(table)