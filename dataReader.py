import os
cur_dir = os.path.dirname(os.path.realpath(__file__))

def read_hary_potter():
    with open(cur_dir + '/data/hary_potter.txt') as hary_potter_book:
        hary_potter_content = hary_potter_book.readlines()
        hary_potter_text = []
        for row in hary_potter_content:
            hary_potter_text.append(row)
        return hary_potter_text