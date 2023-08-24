import subprocess


## TODO: update to account for failures of output?
def getsysinfo(cmd):
    result = subprocess.run(cmd.split(), stdout=subprocess.PIPE).stdout.decode("utf-8").strip()
    return result
