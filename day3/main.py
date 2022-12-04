from pathlib import Path


def get_common_letter(strings):
    return set.intersection(*[set(string) for string in strings]).pop()


def priority(letter):
    if letter.islower():
        return ord(letter) - ord('a') + 1
    else:
        return ord(letter) - ord('A') + 27


def main():
    input_str = Path("input.txt").read_text()
    lines = input_str.splitlines()
    rucksacks = [(line[:len(line) // 2], line[len(line) // 2:]) for line in lines]
    common_items = [get_common_letter(rucksack) for rucksack in rucksacks]
    sum_of_priorities = sum([priority(common_item) for common_item in common_items])
    print(f"The sum of the priorities of item types in both compartments is {sum_of_priorities}")

    elf_groups = zip(lines[::3], lines[1::3], lines[2::3])
    common_items = [get_common_letter(elf_group) for elf_group in elf_groups]
    sum_of_priorities = sum([priority(common_item) for common_item in common_items])
    print(f"The sum of the priorities of item types corresponding to each elf group is {sum_of_priorities}")


if __name__ == "__main__":
    main()
