import pandas as pd
from sklearn.preprocessing import StandardScaler
import statsmodels.api as sm
import seaborn as sns
import matplotlib.pyplot as plt
from scipy.stats import f_oneway
from statsmodels.stats.multicomp import MultiComparison


sat_df = pd.read_csv('/Users/joshy/Desktop/dai/daimil5/projects/final/'
                     'active_satellites/data/database.csv')


def drop_na(sat_df):
    """
    Drop rows with missing values in specific columns from a DataFrame.

    Parameters:
    - sat_df (DataFrame): Input DataFrame containing satellite data.

    Returns:
    - cleaned_df (DataFrame): DataFrame with rows containing missing values
      removed.
    """
    sat_df.dropna(subset=["Expected Lifetime (Years)",
                          "Launch Mass (Kilograms)"], inplace=True)
    return sat_df


def remove_extra_letters(col):
    """
    Remove extra letters and symbols from a DataFrame column containing
      time-related values.

    Parameters:
    - col (Series): A pandas Series representing the column with time-related
      values.

    Returns:
    - cleaned_col (Series): A pandas Series with extra letters and symbols
      removed.
    """
    return col.replace(' yr.', '') \
              .replace(' hrs.', '') \
              .replace(' trs', '') \
              .replace('yrs.', '') \
              .replace(',', '')


def convert_range_to_mean(col):
    """
    Convert a range-formatted value or single value in the DataFrame column to
      its mean value.

    Parameters:
    - col (Series): A pandas Series representing the column with
      range-formatted or single values.

    Returns:
    - mean_value (float): The mean value derived from the range or single
      value.
    """
    if '-' in col:
        low, high = col.split('-')
        return (float(low) + float(high)) / 2
    return float(col)


def process_expected_lifetime_column(df):
    """
    Process the 'Expected Lifetime (Years)' column in the DataFrame by
      removing extra letters and converting ranges to means.

    Parameters:
    - df (DataFrame): Input DataFrame with the 'Expected Lifetime (Years)'
      column.

    Returns:
    - df (DataFrame): DataFrame with the 'Expected Lifetime (Years)' column
      cleaned and processed.
    """
    df['Expected Lifetime (Years)'] = df['Expected Lifetime (Years)'] \
        .apply(remove_extra_letters)
    df['Expected Lifetime (Years)'] = df['Expected Lifetime (Years)'] \
        .apply(convert_range_to_mean)
    return df


def make_numeric(sat_df):
    """
    Convert the 'Launch Mass (Kilograms)' column in the DataFrame to numeric
      values.

    Parameters:
    - sat_df (DataFrame): Input DataFrame with the 'Launch Mass (Kilograms)'
      column.

    Returns:
    - sat_df (DataFrame): DataFrame with the 'Launch Mass (Kilograms)' column
      converted to numeric values.
    """
    pd.to_numeric(sat_df["Launch Mass (Kilograms)"],
                  errors='coerce')
    return sat_df


def remove_space(col):
    """
    Remove spaces from the given column values and return the cleaned column.

    Parameters:
    - col (Series): Input column with values containing spaces.

    Returns:
    - cleaned_col (Series): Column with spaces removed from its values.
    """
    return col.replace('LEO ', 'LEO')


def get_dummies(sat_df):
    """
    Create dummy variables for categorical column and return the updated
      DataFrame.

    Parameters:
    - sat_df (DataFrame): Input DataFrame containing categorical column.

    Returns:
    - updated_df (DataFrame): DataFrame with dummy variables created for the
      specified column.
    """
    sat_df_df = pd.get_dummies(sat_df, columns=["Class of Orbit"])
    return sat_df_df


def make_reg(X, y):
    """
    Create and return a linear regression model.

    Parameters:
    - X (array-like): Features (independent variables) for the regression.
    - y (array-like): Target variable (dependent variable) for the regression.

    Returns:
    - model (StatsModels OLS): Fitted linear regression model.
    """
    scaler = StandardScaler()
    X_scaled = scaler.fit_transform(X)

    X_scaled = sm.add_constant(X_scaled)

    model = sm.OLS(y, X_scaled).fit()
    return model


def plot_actual_vs_predicted(y_true, y_predicted, save_file=None):
    """
    Plot the actual versus predicted expected lifetime using a scatterplot.

    Parameters:
    - y_true (array-like): Array of true values (actual expected lifetimes).
    - y_predicted (array-like): Array of predicted values (predicted expected
      lifetimes).
    - save_file (str, optional): File path to save the plot. If not provided,
      the plot will be displayed.

    Returns:
    Plot or file if specified
    """
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


def create_boxplot(sat_df, save_file=None):
    """
    Create a box plot to visualize the distribution of expected lifetimes
    among different satellite orbits.

    Parameters:
    - sat_df (DataFrame): The DataFrame containing satellite data.
    - save_file (str, optional): File path to save the plot. If not provided,
        the plot will be displayed.

    Returns:
    - Plot or file if specified
    """
    sns.set_style("darkgrid")
    sat_df.groupby('Class of Orbit')['Expected Lifetime (Years)'].mean()
    fig, ax = plt.subplots(figsize=(8, 6))
    sns.boxplot(x='Class of Orbit',
                y='Expected Lifetime (Years)',
                data=sat_df,
                palette='Blues_r')
    ax.set_xlabel('Class of Orbit',
                  fontsize=15)
    ax.set_ylabel('Average Lifetime (Years)',
                  fontsize=15)
    ax.set_title('Average Lifetime of Satellites vs. sat_df',
                 fontsize=18)
    if save_file:
        plt.savefig(save_file, bbox_inches='tight')
    else:
        plt.show()


def perform_anova_and_posthoc(sat_df, orbit_df, alpha=0.05):
    """
    Perform ANOVA and post hoc analysis on satellite data.

    Parameters:
    - sat_df (DataFrame): The entire satellite data DataFrame.
    - subset_df (DataFrame): Subset of the satellite data for the analysis.
    - alpha (float): Significance level for post hoc analysis.

    Returns:
    - anova_statistic (float): The ANOVA test statistic.
    - p_value (float): The p-value from the ANOVA test.
    - posthoc_results (MultiComparison): Results of the post hoc Tukey's HSD.
    """
    anova_result = f_oneway(
        orbit_df[orbit_df['Class of Orbit_GEO'] == 1]
        ['Expected Lifetime (Years)'],
        orbit_df[orbit_df['Class of Orbit_LEO'] == 1]
        ['Expected Lifetime (Years)'],
        orbit_df[orbit_df['Class of Orbit_MEO'] == 1]
        ['Expected Lifetime (Years)'],
        orbit_df[orbit_df['Class of Orbit_Elliptical'] == 1]
        ['Expected Lifetime (Years)']
    )
    p_value = anova_result.pvalue

    multi_comp = MultiComparison(orbit_df['Expected Lifetime (Years)'], 
                                 sat_df['Class of Orbit'])
    posthoc_results = multi_comp.tukeyhsd(alpha=alpha)
    return anova_result.statistic, p_value, posthoc_results


if __name__ == '__main__':
    sat_df = drop_na(sat_df)
    sat_df['Class of Orbit'] = sat_df['Class of Orbit'].apply(remove_space)
    sat_df = process_expected_lifetime_column(sat_df)
    sat_df = make_numeric(sat_df)
    create_boxplot(sat_df, save_file='/Users/joshy/Desktop/dai/daimil5/'
                   'projects/final/active_satellites/img/'
                   'boxplot.png')
    orbit_df = get_dummies(sat_df)
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
    perform_anova_and_posthoc(sat_df, orbit_df)
