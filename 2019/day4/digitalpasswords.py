#!python3

def find_matching_passwords(start, end):

    for password in range(start, end):

        num, prev_digit = password // 10, password % 10
        is_ascending, is_double, adjacency_registry = False, False, {}

        while num:
            num, cur_digit = num // 10, num % 10
            if prev_digit < cur_digit:
                break
            elif prev_digit == cur_digit:
                if cur_digit not in adjacency_registry:
                    adjacency_registry[cur_digit] = 2
                else:
                    adjacency_registry[cur_digit] += 1
            prev_digit = cur_digit
        else:
            is_ascending = True

        if is_ascending and any(count == 2 for count in adjacency_registry.values()):
            yield password

if __name__ == "__main__":
    input = "134792-675810"
    start, end = input.split("-")
    passwords = find_matching_passwords(int(start), int(end))
    print(f"matching passwords count: {sum(map(lambda x: 1, passwords))}.")
