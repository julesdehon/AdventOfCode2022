from pathlib import Path


def parse_range(raw_range):
    start, end = raw_range.split("-")
    return range(int(start), int(end) + 1)


def fully_contains(first_range, second_range):
    intersection = set(first_range).intersection(second_range)
    return intersection == set(first_range) or intersection == set(second_range)


def overlaps(first_range, second_range):
    return len(set(first_range).intersection(second_range)) != 0


def main():
    input_str = Path("input.txt").read_text()
    elf_pairs = [(parse_range(first), parse_range(second)) for (first, second) in
                 [line.split(",") for line in input_str.splitlines()]]
    num_fully_overlapping_pairs = len([elf_pair for elf_pair in elf_pairs if fully_contains(*elf_pair)])
    print(f"{num_fully_overlapping_pairs} assignment pairs have one range fully containing the other")

    num_overlapping_pairs = len([elf_pair for elf_pair in elf_pairs if overlaps(*elf_pair)])
    print(f"{num_overlapping_pairs} assignment pairs have overlapping ranges")


if __name__ == "__main__":
    main()
