import pandas as pd

from planes import mean_routes


if __name__ == '__main__':
    airlines = pd.read_csv('airlines.csv')
    airports = pd.read_csv('airports.csv')
    routes = pd.read_csv('routes.csv')

    means = mean_routes(airlines, airports, routes)

    assert isinstance(means, pd.Series), 'Return value is no series.'
    assert means.index.name == 'country', 'Index is not the country.'

    print(means.head())
