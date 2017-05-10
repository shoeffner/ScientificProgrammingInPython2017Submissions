def first_gen(df):
    '''find the names of all Pokemon from generation 1
    returns: series containing names'''
    return df[df.Generation == 1]['Name']


def highest_hp(df):
    '''find the name(s) of the Pokemon with the highest HP
    returns: series containing names'''
    return df[df.HP == df.HP.max()]['Name']


def mean_attack_by_type(df):
    '''find the mean attack power of each type (just use Type 1), result will
    contain just type and attack columns
    returns: data frame with columns ('Type 1', 'Attack')
    '''
    return df.groupby('Type 1').Attack.mean().reset_index()


def high_defense(df):
    '''find just the Name and Defense rating of Pokemon that have an
    above average (>) Defense.
    returns: data frame with columns ('Name', 'Defense')
    '''
    return df[df.Defense > df.Defense.mean()][['Name', 'Defense']]


def deduplicated(df):
    '''some Pokemon are in the list multiple times with different names.
    Find the names of the pokemon but without these duplicates. You
    can use the # column to tell if they're the same pokemon. Example:
    "Venusaur" has # 3 and there is a "VenusaurMega Venusaur" also
    with # 3, the result should have just "Venusaur"
    returns: series containing names
    '''
    return df.drop_duplicates('#').Name
