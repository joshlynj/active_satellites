import pandas as pd
from sklearn.preprocessing import StandardScaler
import statsmodels.api as sm
import seaborn as sns
import matplotlib.pyplot as plt

sat_df = pd.read_csv('/Users/joshy/Desktop/dai/daimil5/projects/final/'
                     'active_satellites/data/database.csv')


def drop_na(sat_df):
    ''' Function takes in a dataframe
        Returns a dataframe that drops duplicates for relevant columns '''
    sat_df.dropna(subset=["Expected Lifetime (Years)",
                          "Launch Mass (Kilograms)"], inplace=True)
    return sat_df


def remove_extra_letters(col):
    ''' Function takes in a df column
        Function returns the string with extra letters removed '''
    return col.replace(' yr.', '') \
              .replace(' hrs.', '') \
              .replace(' trs', '') \
              .replace('yrs.', '') \
              .replace(',', '')


def convert_range_to_mean(col):
    ''' Function takes in a df column
        Function returns the string with extra letters removed '''
    if '-' in col:
        low, high = col.split('-')
        return (float(low) + float(high)) / 2
    return float(col)


def process_expected_lifetime_column(df):
    ''' Function takes in a dataframe
        Function returns a dataframe that has been cleaned'''
    df['Expected Lifetime (Years)'] = df['Expected Lifetime (Years)'] \
        .apply(remove_extra_letters)
    df['Expected Lifetime (Years)'] = df['Expected Lifetime (Years)'] \
        .apply(convert_range_to_mean)
    return df


def make_numeric(sat_df):
    ''' Function takes in a dataframe
        Returns a dataframe with the launch mass column as an int '''
    pd.to_numeric(sat_df["Launch Mass (Kilograms)"],
                  errors='coerce')
    return sat_df


def remove_space(col):
    ''' Function takes in a col
        Returns a col with the space removed '''
    return col.replace('LEO ', 'LEO')


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


def plot_actual_vs_predicted(y_true, y_predicted, save_file=None):
    fig, ax = plt.subplots(figsize=(8, 6))
    sns.set_style("darkgrid")
    sns.scatterplot(x=y_true,
                    y=y_predicted, alpha=0.7,
                    color='#ac78bf', edgecolor='k',
                    ax=ax,
                    label='Predicted')
    sns.lineplot(x=y_true,
                 y=y_true,
                 color='#120a4d',
                 linestyle='dashed',
                 ax=ax,
                 label='Actual')
    ax.set_xlabel("Actual Expected Lifetime (Years)",
                  fontsize=15)
    ax.set_ylabel("Predicted Expected Lifetime (Years)",
                  fontsize=15)
    ax.set_title("Actual vs. Predicted Expected Lifetime"
                 " (Inferential Linear Regression)", fontsize=18)
    ax.legend()
    if save_file:
        plt.savefig(save_file, bbox_inches='tight')
    else:
        plt.show()


if __name__ == '__main__':
    (drop_na(sat_df))
    (process_expected_lifetime_column(sat_df))
    (make_numeric(sat_df))
    (sat_df.apply(remove_space))
    (get_dummies(sat_df))
    (make_reg(sat_df[['Perigee (Kilometers)',
                      'Apogee (Kilometers)',
                      'Launch Mass (Kilograms)',
                      'Inclination (Degrees)']],
              sat_df['Expected Lifetime (Years)']))
    model = make_reg(sat_df[['Perigee (Kilometers)',
                             'Apogee (Kilometers)',
                             'Launch Mass (Kilograms)',
                             'Inclination (Degrees)']],
                     sat_df['Expected Lifetime (Years)'])
    plot_actual_vs_predicted(sat_df['Expected Lifetime (Years)'],
                             model.fittedvalues,
                             save_file='/Users/joshy/Desktop/dai/daimil5/'
                             'projects/final/active_satellites/img/'
                             'actual_vs_predict.png')
