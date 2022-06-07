
def set_to_txt(set, filename):
    with open(filename, 'w') as f:
        for item in set:
            f.write("%s\n" % item)


def txt_to_set(filename):
    data = set()
    with open(filename, 'r') as f:
        for line in f.readlines():
            x = line[:-1]
            data.add(x)
    return data
