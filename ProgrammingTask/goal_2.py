full_name = input("Write full names separated by a comma: \n")


def counter(last_name):
    name_as_list = last_name.split(',')
    occurrence = 0

    for name in name_as_list:
        name = name.lower()
        split_name = name.split()

        if split_name[-1] == 'siddique':
            occurrence += 1
            
    return occurrence


print(counter(full_name))
