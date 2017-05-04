from analyze import mean, mode, median


def test():
    testlist0 = [1, 2, 3, 4, 5]
    testlist1 = [1, 2, 3, 4, 5, 6]
    testlist2 = [2, 2, 3, 4, 4, 6]
    testlist3 = [2, 2, 3, 4, 5, 6, 7]

    assert mean(testlist0) - 5 <= 1e-6, 'test 1: ' + mean(testlist0)
    assert mean(testlist1) - 3.5 <= 1e-6, 'test 2: ' + mean(testlist1)
    assert mean(testlist2) - 21 / 6 <= 1e-6, 'test 3: ' + mean(testlist2)
    assert mean(testlist3) - 29 / 7 <= 1e-6, 'test 4: ' + mean(testlist3)

    assert median(testlist0) == 3, 'test 5: ' + median(testlist0)
    assert median(testlist1) - 3.5 <= 1e-6, 'test 6: ' + median(testlist1)
    assert median(testlist2) - 3.5 <= 1e-6, 'test 7: ' + median(testlist2)
    assert median(testlist3) == 4, 'test 8: ' + median(testlist3)

    assert mode(testlist0) in testlist0, 'test 9'
    assert mode(testlist1) in testlist1, 'test 10'
    assert mode(testlist2) in [2, 4], 'test 11'
    assert mode(testlist3) in [2], 'test 12'


if __name__ == '__main__':
    test()
