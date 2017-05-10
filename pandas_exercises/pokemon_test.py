import pandas as pd

import pokemon


if __name__ == '__main__':
    df = pd.read_csv('Pokemon.csv')

    first_gen = pokemon.first_gen(df)
    assert isinstance(first_gen, pd.Series), 'first_gen is no Series'

    highest_hp = pokemon.highest_hp(df)
    assert isinstance(highest_hp, pd.Series), 'highest_hp is no Series'

    mean_attack = pokemon.mean_attack_by_type(df)
    assert isinstance(mean_attack, pd.DataFrame), 'mean_attack is no DataFrame'

    high_defense = pokemon.high_defense(df)
    assert isinstance(high_defense, pd.DataFrame), 'high_defense is no ' + \
        'DataFrame'

    deduped = pokemon.deduplicated(df)
    assert isinstance(deduped, pd.Series), 'mean_attack is no DataFrame'
