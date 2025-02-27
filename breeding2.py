from itertools import combinations, product
from collections import Counter
from math import comb


def calculate_iv_probabilities(ivs_p1, ivs_p2, input_format="iv", destiny_knot=True, power_item=-1):
    total_ivs = 6
    inherited_iv_count = 5 if destiny_knot else 3  # Destiny Knot ensures 5 IVs are inherited, otherwise 3

    # List of all IV slots
    iv_slots = list(range(total_ivs))

    # Power item
    if power_item in range(1, 7):
        power_item_iv_slot = power_item - 1

        total_ivs -= 1
        inherited_iv_count -= 1
        iv_slots.remove(power_item_iv_slot)

        power_item_iv = max(ivs_p1[power_item_iv_slot], ivs_p2[power_item_iv_slot])

        if power_item_iv != 31:
            raise ValueError(f"power item {power_item} passed on a non-perfect IV of {power_item_iv}")

    # Store probability results
    probability_distribution = Counter()

    # Create keys in Counter in order
    for i in range(0, 7):
        probability_distribution[i] += 0

    # Iterate over all possible IV inheritance slot combinations
    for inheritable_iv_slots in combinations(iv_slots, inherited_iv_count):
        # Keep only inheritable IV slots
        inheritable_ivs_p1 = [ivs_p1[i] for i in inheritable_iv_slots]
        inheritable_ivs_p2 = [ivs_p2[i] for i in inheritable_iv_slots]

        # Iterate over all inheritable IV combinations
        for inherited_ivs in product(*zip(inheritable_ivs_p1, inheritable_ivs_p2)):
            inherited_perfect_count = sum(1 for iv in inherited_ivs if iv == 31)
            inherited_perfect_count += 1 if power_item in range(1, 7) else 0

            remaining_ivs = total_ivs - inherited_iv_count

            for perfect_remaining_ivs in range(remaining_ivs + 1):
                n = remaining_ivs
                k = perfect_remaining_ivs
                # n-k = non-perfect remaining ivs

                probability_distribution[inherited_perfect_count + perfect_remaining_ivs] \
                    += (31/32)**(n-k) * (1/32)**k * comb(n, k)

    # Normalize probabilities
    total_cases = sum(probability_distribution.values())
    probability_distribution = {k: round(v / total_cases, 3) for k, v in probability_distribution.items()}

    print(probability_distribution)


def slot_to_iv(slots):
    return [31 if slot in slots else 0 for slot in range(1, 7)]


def count_to_iv(perfect_p1, perfect_p2, overlap):
    ivs_p1 = [31] * perfect_p1 + [0] * (6 - perfect_p1)
    ivs_p2 = [0] * (perfect_p1 - overlap) + [31] * perfect_p2 + [0] * (6 - (perfect_p1 - overlap + perfect_p2))
    return ivs_p1, ivs_p2


if __name__ == "__main__":
    ivs_p1 = slot_to_iv([1, 2, 4])
    ivs_p2 = slot_to_iv([1, 3, 4, 5, 6])
    calculate_iv_probabilities(ivs_p1, ivs_p2, power_item=-1)
    calculate_iv_probabilities(ivs_p1, ivs_p2, destiny_knot=False, power_item=3)
    print()

    ivs_p1 = slot_to_iv([1, 2, 4, 5, 6])
    ivs_p2 = slot_to_iv([1, 3, 4, 5, 6])
    calculate_iv_probabilities(ivs_p1, ivs_p2, destiny_knot=True, power_item=3)
    print()

    n = 4
    m = 5
    for p in range(-1, -1):
        for overlap in range(max(0, m + n - 6), min(m, n) + 1):
            iv1, iv2 = count_to_iv(n, m, overlap)
            calculate_iv_probabilities(iv1, iv2, power_item=p)
        print()
