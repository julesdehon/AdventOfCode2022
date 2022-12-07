from pathlib import Path


def find_first_n_distinct_chars(stream: str, n: int) -> int:
    last_n = list(stream[:n])
    for i, char in enumerate(stream[4:]):
        if len(set(last_n)) == len(last_n):
            return i + 4
        last_n.pop(0)
        last_n.append(char)


def main():
    input_str = Path("input.txt").read_text()
    first_start_of_packet_marker = find_first_n_distinct_chars(input_str, 4)
    print(f"The first start of packet marker appears after the {first_start_of_packet_marker}th character arrives")

    first_start_of_message_marker = find_first_n_distinct_chars(input_str, 14)
    print(f"The first start of message marker appears after the {first_start_of_message_marker}th character arrives")


if __name__ == "__main__":
    main()
