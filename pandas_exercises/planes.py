import pandas as pd


def mean_routes(airlines, airports, routes):
    '''
    Find the mean number of routes per airport by country. Use the source
    airport to determine the country and don't worry about whether the flight
    is interational or domestic.

    Example:
    Some country has 3 airports
    Airport1 is the source of 5 flights
    Airport2 is the source of 3 flights
    Airport3 is the source of 8 flights
    Average for the country: 5.333

    Returns: Series where the index is the country name and the values are the
    means rounded to 3 decimal places

    Other notes:
    It might be possible to do this using just one groupby but the solution
    used two
    '''
    # Select needed valid data.
    route_data = routes[['src_airport', 'dest_airport']]
    airport_data = airports[['country', 'iata']][airports['iata'] != "\\N"]

    # Join data
    joined_data = pd.merge_ordered(airport_data, route_data, how='left',
                                   left_on='iata', left_by='country',
                                   right_on='src_airport')
    # Reduce data
    joined_data = joined_data[['country', 'iata']]

    # Group, count per group
    joined_data = joined_data.groupby(['country', 'iata']).size().reset_index()
    joined_data = joined_data.groupby('country').mean().round(3)

    # Convert to Series and return
    return joined_data.iloc[:, 0]
