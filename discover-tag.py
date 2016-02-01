from tagreader import TagReader

def print_tag (a):
    print (a)



tr = TagReader('tty:AMA0:pn532')
tr.tag_discovered += print_tag

wait = input("PRESS ENTER TO CONTINUE.")
