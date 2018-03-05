import random

if __name__ == '__main__':
    i = 0
    while i < 60:
        inte = random.randint(20,64)
        print(''.join(random.choice('0123456789abcdef') for n in range(inte)))
        i = i + 1
