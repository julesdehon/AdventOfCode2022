from pathlib import Path


class Choice:
    ROCK = 1
    PAPER = 2
    SCISSORS = 3

    @staticmethod
    def parse(letter):
        if letter == "A" or letter == "X":
            return Choice.ROCK
        elif letter == "B" or letter == "Y":
            return Choice.PAPER
        elif letter == "C" or letter == "Z":
            return Choice.SCISSORS
        else:
            raise Exception("Invalid letter")


class Outcome:
    WIN = 6
    DRAW = 3
    LOSS = 0

    WIN_CONDITIONS = {(Choice.ROCK, Choice.SCISSORS),
                      (Choice.SCISSORS, Choice.PAPER),
                      (Choice.PAPER, Choice.ROCK)}

    @staticmethod
    def calculate(opponent_choice, my_choice):
        if opponent_choice == my_choice:
            return Outcome.DRAW
        elif (my_choice, opponent_choice) in Outcome.WIN_CONDITIONS:
            return Outcome.WIN
        else:
            return Outcome.LOSS

    @staticmethod
    def parse(letter):
        if letter == "X":
            return Outcome.LOSS
        elif letter == "Y":
            return Outcome.DRAW
        elif letter == "Z":
            return Outcome.WIN
        else:
            raise Exception("Invalid letter")


def score(raw_opponent_choice, raw_my_choice):
    return Choice.parse(raw_my_choice) + Outcome.calculate(Choice.parse(raw_opponent_choice),
                                                           Choice.parse(raw_my_choice))


def get_choice_for_outcome(opponent_choice, outcome):
    if outcome == Outcome.WIN:
        return [winner for (winner, loser) in Outcome.WIN_CONDITIONS if opponent_choice == loser][0]
    elif outcome == Outcome.DRAW:
        return opponent_choice
    else:
        return [loser for (winner, loser) in Outcome.WIN_CONDITIONS if opponent_choice == winner][0]


def score_after_clarification(raw_opponent_choice, raw_game_outcome):
    game_outcome = Outcome.parse(raw_game_outcome)
    return get_choice_for_outcome(Choice.parse(raw_opponent_choice), game_outcome) + game_outcome


def main():
    input_str = Path("input.txt").read_text()
    games = [line.split(" ") for line in input_str.splitlines()]
    total_score = sum([score(*game) for game in games])
    print(f"If I followed the strategy guide, my score would be {total_score}")

    total_score_after_clarification = sum([score_after_clarification(*game) for game in games])
    print(f"After clarifying, my score would be {total_score_after_clarification}")


if __name__ == "__main__":
    main()
