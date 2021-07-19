import xattr
import os
import sys
import uuid
from iterfzf import iterfzf

def create_name():
    # creates random v4 uuid
    file_uuid = uuid.uuid4()
    # clean filename
    s = str(file_uuid)
    filename = s.replace('-', '')
    return filename
    
def is_just_hex(filename):
    not_hex_chars = set('ghijklmnopqrstuvwxyz`~!@#$%^&*()-_=+{}[];:,<.>/?|')
    if any((c in not_hex_chars) for c in filename):
        raise Exception('not hex char found')
    else:
        print('not not hex')
        return 0

def is_32_len(filename):    
    filename_length = len(filename)
    if not filename_length == 32:
        raise Exception('all dogma files are 32 hexadecimal characters')
    else:
        print('name is 32 hex chars')
        return 0

def is_filename_unique(filename):
    # produce list of files in dogma dir to check for prexisting filenames
    files_in = os.listdir(dogma_dir)
    # checks all preexisting filenames against the new filename
    for file in files_in:
        if file == filename:
            raise Exception('Wow, you beat the odds and found a match on a UUID! Hooray!!')
        else:
            return 0
        
def create_file():
    filename = create_name()
    print(filename)
    i_hex = is_just_hex(filename)
    i_length = is_32_len(filename)
    i_unique = is_filename_unique(filename)
    if i_hex == 0 and i_length == 0 and i_unique == 0:
        file_path = os.path.join(dogma_dir , filename)
        os.umask(0)
        open(os.open(file_path, os.O_CREAT, 0o720), 'x')
        print(file_path, 'made')
        return file_path
    else:
        raise Exception('error; boop beep')

# xattr functions    
def set_xattrs(file_path, *x_pair):
    pair = list(x_pair[0])
    try:
        set_mime_xattr(file_path, pair[0])
        set_name_xattr(file_path, pair[1])
    except:
        print('There was an error')
        
def set_mime_xattr(file_path, *mimev):
    mime_file = os.path.join(dogma_dir, '0b3851eefaf8de727bfb4cacf1c94100')
    s = str(mimev[0])
    if len(s) > 0:
        mime = s
        print(s)
    else:
        with open(mime_file) as file:
            lines = file.read().splitlines()

            mime = iterfzf(lines)
            
    xattr.set(file_path, "user.mime", mime)

def set_name_xattr(file_path, *namev):
    s = str(namev[0])
    if len(s) > 0:
        name = s
        print(name)
    else:
        name = input("What is the files real name? ")
        
    xattr.set(file_path, "user.name", name)    

dogma_dir = "/x1j5e/.dogma"
file = create_file()

if len(sys.argv) > 1:
    set_xattrs(file, sys.argv[1:])
else:
    set_xattrs(file)
