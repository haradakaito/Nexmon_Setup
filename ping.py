from ping3 import ping
import sys
import time

roop_count = 0

if __name__ == '__main__':

    addr = input('addr: ') # Bloadcast Addr
    if addr == '':
        addr = 'XXX.XXX.XXX.XXX'

    rate = input('late[1/s]: ') # Transmission interval
    if rate == '':
        rate = 1.0
    else:
        rate = int(rate)
    sleep_time = 1/rate

    print(addr+'にpingを送信しています')
    while(True):

        # Pingの送信
        res = ping(addr)
        roop_count += 1
        print("\rパケット数："+str(roop_count), end="")
        sys.stdout.flush()
        time.sleep(sleep_time)