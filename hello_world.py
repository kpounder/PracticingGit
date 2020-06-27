print('Hello world!')
print('Hello again!')
print('Third hello')
print('Fourth hello')
print('Fifth hello')


def print_n_times(word):
    for i in range(n):
        print(word)


def multiply_by_two(num):
    try:
        print(num * 2)
    except Exception:
        print('Input must be number.')
