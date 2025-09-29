import random

def random_weapon():
    return random.choice(["rock", "paper", "scissors"])


def rps_outcome(player, comp):
    if player == comp:
        return "DRAW"
    if (
        (player == "rock" and comp == "scissors")
        or (player == "paper" and comp == "rock")
        or (player == "scissors" and comp == "paper")
    ):
        return "YOU WIN"
    return "YOU LOSE"
