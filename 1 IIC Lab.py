def is_prime(num):
    if num <= 1:
        return False
    elif num == 2:
        return True
    elif num % 2 == 0:
        return False
    else:
        for i in range(3, int(num**0.5) + 1, 2):
            if num % i == 0:
                return False
        return True

def generate_prime_list(N):
    prime_list = []
    for i in range(2, N + 1):
        if is_prime(i):
            prime_list.append(i)
    return prime_list

try:
    N = int(input("Введіть число N: "))
    if N < 1:
        print("Введіть додатне ціле число більше за 1.")
    else:
        primes = generate_prime_list(N)
        print(f"Список простих чисел від 1 до {N}: {primes}")
except ValueError:
    print("Введено неправильний формат даних. Будь ласка, введіть ціле число.")
