import subprocess 
import shlex 
def run_command(command):
    process = subprocess.Popen(shlex.split(command), stdout=subprocess.PIPE)
    while True:
        output = process.stdout.readline()
        if output == '' and process.poll() is not None:
            break
        if output:
            print (output.strip().decode('utf-8'))
    rc = process.poll()
    return rc

run_command("ls -lh")
