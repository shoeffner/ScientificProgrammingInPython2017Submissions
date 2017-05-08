import pandas as pd

import pokemon


if __name__ == '__main__':
    df = pd.read_csv('Pokemon.csv')

    first_gen = pokemon.first_gen(df)
    print(first_gen)

    highest_hp = pokemon.highest_hp(df)
    print(highest_hp)

    mean_attack = pokemon.mean_attack_by_type(df)
    print(mean_attack)

    high_defense = pokemon.high_defense(df)
    print(high_defense)

    deduped = pokemon.deduplicated(df)
    print(deduped)
