from itertools import combinations
from collections import Counter
from random import choice


def calculate_iv_probabilities(perfect_ivs_parent1, perfect_ivs_parent2, overlap, destiny_knot=True):
    """
    Calculates the probability distribution of a child Pokemon inheriting 0-6 perfect IVs.
    Assumes one parent is holding a Destiny Knot if enabled, so the child inherits 5 IVs, otherwise 3 IVs.

    Parameters:
    - perfect_ivs_parent1: Number of perfect IVs in parent 1
    - perfect_ivs_parent2: Number of perfect IVs in parent 2
    - overlap: Number of perfect IVs that both parents share
    - destiny_knot: Whether a Destiny Knot is being held (default: True)

    Returns:
    - Dictionary mapping number of perfect IVs (0-6) to their probabilities.
    """
    total_iv_slots = 6
    inherited_iv_count = 5 if destiny_knot else 3  # Destiny Knot ensures 5 IVs are inherited, otherwise 3

    # Compute unique perfect IVs for each parent
    unique_perfect_ivs_p1 = perfect_ivs_parent1 - overlap
    unique_perfect_ivs_p2 = perfect_ivs_parent2 - overlap

    ivs_p1 = set(range(overlap))
    ivs_p2 = set(range(overlap))

    # List of all IV slots
    iv_slots = list(range(total_iv_slots))

    # Define which slots contain perfect IVs
    perfect_iv_slots = set()
    perfect_iv_slots.update(choice(iv_slots) for _ in range(unique_perfect_ivs_p1))
    perfect_iv_slots.update(choice(iv_slots) for _ in range(unique_perfect_ivs_p2))
    perfect_iv_slots.update(choice(iv_slots) for _ in range(overlap))

    # Store probability results
    probability_distribution = Counter()

    # Iterate over all possible IV inheritance combinations
    for inherited_set in combinations(iv_slots, inherited_iv_count):
        inherited_perfect_count = sum(1 for iv in inherited_set if iv in perfect_iv_slots)

        # The last IVs are random (1/32 chance of being perfect for each)
        remaining_ivs = total_iv_slots - inherited_iv_count
        remaining_perfect_prob = (1 / 32) ** remaining_ivs  # Probability of rolling 31 for each
        probability_distribution[inherited_perfect_count] += (1 - remaining_perfect_prob)
        probability_distribution[inherited_perfect_count + remaining_ivs] += remaining_perfect_prob

    # Normalize probabilities
    total_cases = sum(probability_distribution.values())
    probability_distribution = {k: v / total_cases for k, v in probability_distribution.items()}

    return probability_distribution


if __name__ == "__main__":
    print(calculate_iv_probabilities(perfect_ivs_parent1=4, perfect_ivs_parent2=4, overlap=2, destiny_knot=True))
    print(calculate_iv_probabilities(perfect_ivs_parent1=4, perfect_ivs_parent2=4, overlap=3, destiny_knot=True))
    print(calculate_iv_probabilities(perfect_ivs_parent1=4, perfect_ivs_parent2=4, overlap=4, destiny_knot=True))
