from pathlib import Path


def main():
    input_str = Path("input.txt").read_text()
    calorie_lists = [[int(raw_calorie) for raw_calorie in raw_calorie_list.split("\n")] for raw_calorie_list in
                     input_str.split("\n\n")]
    calories_per_elf = [sum(calorie_list) for calorie_list in calorie_lists]

    max_calories = max(calories_per_elf)
    print(f"The elf carrying the most calories is carrying {max_calories} calories")

    top_3_calories_sum = sum(sorted(calories_per_elf, reverse=True)[:3])
    print(f"The three elves carrying the most calories are carrying {top_3_calories_sum} calories in total")


if __name__ == "__main__":
    main()
