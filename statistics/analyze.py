def mode(input_list):
    return sorted(input_list, key=input_list.count)[-1]


def median(input_list):
    idx = len(input_list) // 2
    if len(input_list) & 1:
        return sorted(input_list)[idx]
    else:
        return mean(sorted(input_list)[idx - 1:idx + 1])


def mean(input_list):
    return sum(input_list) / len(input_list)


if __name__ == '__main__':

    combinations = [
        ('name', mode),
        ('age', mean),
        ('age', median),
        ('age', mode),
        ('eye-color', mode)
    ]

    with open('data.txt') as f:
        data = {k: v for k, v in
                      zip(('name', 'age', 'eye-color'),
                          zip(*[l.split(', ')
                                for l in f.read().splitlines()[1:]]))}
        data['age'] = list(map(int, data['age']))

    for attr, meth in combinations:
        print(f'Attribute: {attr} | Method: {meth.__name__} | Result: {meth(data[attr])}')
