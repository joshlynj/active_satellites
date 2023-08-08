import pandas as pd
from sklearn.preprocessing import StandardScaler
import statsmodels.api as sm

sat_df = pd.read_csv('/Users/joshy/Desktop/dai/daimil5/projects/final/'
                     'active_satellites/data/database.csv')


def drop_na(sat_df):
    ''' Function takes in a dataframe
        Returns a dataframe that drops duplicates for relevant columns '''
    sat_df.dropna(subset=["Expected Lifetime (Years)",
                          "Launch Mass (Kilograms)"], inplace=True)
    return sat_df


def clean_lifetime(value):
    ''' Function takes in a value
        Function replaces strings and takes mean value of ranges
        Returns a cleaned float value '''
    value = value.replace(' yr.', '') \
                 .replace(' hrs.', '') \
                 .replace(' trs', '') \
                 .replace('yrs.', '') \
                 .replace(',', '')
    if '-' in value:
        low, high = value.split('-')
        return (float(low) + float(high)) / 2
    return float(value)


def make_numeric(sat_df):
    ''' Function takes in a dataframe
        Returns a dataframe with the launch mass column as an int '''
    pd.to_numeric(sat_df["Launch Mass (Kilograms)"],
                  errors='coerce')
    return sat_df


def remove_space(value):
    ''' Function takes in a value
        Returns a value with the space removed '''
    return value.replace('LEO ', 'LEO')


def get_dummies(sat_df):
    ''' Function takes in a dataframe
        Returns a dataframe with dummies'''
    orbit_df = pd.get_dummies(sat_df, columns=["Class of Orbit"])
    return orbit_df


def make_reg(X, y):
    scaler = StandardScaler()
    X_scaled = scaler.fit_transform(X)

    X_scaled = sm.add_constant(X_scaled)

    model = sm.OLS(y, X_scaled).fit()
    return model


if __name__ == '__main__':
    print(drop_na(sat_df))
    print(sat_df['Expected Lifetime (Years)'].apply(clean_lifetime))
    print(make_numeric(sat_df))
    print(sat_df.apply(remove_space))
    print(get_dummies(sat_df))
    print(make_reg(sat_df[['Perigee (Kilometers)',
                           'Inclination (Degrees)']],
                   sat_df['Apogee (Kilometers)']))
