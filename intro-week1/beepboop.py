if __name__ == '__main__':
    for i in range(1, 31):
        print(('beep' * (i % 3 == 0) + 'boop' * (i % 5 == 0)) or i)
