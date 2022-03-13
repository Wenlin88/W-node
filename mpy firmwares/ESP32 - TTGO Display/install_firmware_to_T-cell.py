
import subprocess
def exicute_cmd_command_with_realtime_output(cmd):
    import subprocess
    import sys

    process = subprocess.Popen(cmd, shell = True,bufsize = 1,
                            stdout=subprocess.PIPE, stderr = subprocess.STDOUT,encoding='utf-8', errors = 'replace' ) 
    while True:
        realtime_output = process.stdout.readline()
        if realtime_output == '' and process.poll() is not None:
            return
        if realtime_output:
            print(realtime_output.strip(), flush=False)
            sys.stdout.flush()

exicute_cmd_command_with_realtime_output(cmd = 'esptool --chip esp32 --port COM6 erase_flash')
exicute_cmd_command_with_realtime_output(cmd = 'esptool --chip esp32 --port COM6 write_flash -z 0x1000 esp32-20220117-v1.18.bin')
input('press enter to continue...')

# %%
