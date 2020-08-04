from syslog import syslog

def log(message):
    print(message)
    syslog(message)