import pandas as pd
import os


def calculate_demographic_data(print_data=True):

    data_path = os.path.join(os.path.dirname(__file__), "adult.data.csv")
    df = pd.read_csv(
        data_path,
        header=None,
        skiprows=1,                # drop the header line inside CSV
        skipinitialspace=True,     # trim spaces after commas
        names=[
            "age", "workclass", "fnlwgt", "education", "education-num",
            "marital-status", "occupation", "relationship", "race", "sex",
            "capital-gain", "capital-loss", "hours-per-week",
            "native-country", "salary"
        ]
    )

    race_count = df["race"].value_counts()

    average_age_men = round(df.loc[df["sex"] == "Male", "age"].mean(), 1)

    percentage_bachelors = round((df["education"] == "Bachelors").mean() * 100, 1)

    higher_education_mask = df["education"].isin(["Bachelors", "Masters", "Doctorate"])
    lower_education_mask = ~higher_education_mask

    higher_education = df[higher_education_mask]
    lower_education = df[lower_education_mask]

    higher_education_rich = round(
        (higher_education["salary"] == ">50K").mean() * 100, 1
    )
    lower_education_rich = round(
        (lower_education["salary"] == ">50K").mean() * 100, 1
    )

    min_work_hours = int(df["hours-per-week"].min())
    num_min_workers = df["hours-per-week"] == min_work_hours
    rich_percentage = round(
        (df[num_min_workers]["salary"] == ">50K").mean() * 100, 1
    )

    rich_share_by_country = (
        df.groupby("native-country")["salary"]
          .apply(lambda s: (s == ">50K").mean() * 100)
    )
    highest_earning_country = rich_share_by_country.idxmax()
    highest_earning_country_percentage = round(rich_share_by_country.max(), 1)

    top_IN_occupation = (
        df[(df["native-country"] == "India") & (df["salary"] == ">50K")]
          .occupation.value_counts()
          .idxmax()
    )

    if print_data:
        print("Number of each race:\n", race_count)
        print("Average age of men:", average_age_men)
        print(f"Percentage with Bachelors degrees: {percentage_bachelors}%")
        print(f"Percentage with higher education that earn >50K: {higher_education_rich}%")
        print(f"Percentage without higher education that earn >50K: {lower_education_rich}%")
        print(f"Min work time: {min_work_hours} hours/week")
        print(f"Percentage of rich among those who work fewest hours: {rich_percentage}%")
        print("Country with highest percentage of rich:", highest_earning_country)
        print(f"Highest percentage of rich people in country: {highest_earning_country_percentage}%")
        print("Top occupations in India:", top_IN_occupation)

    return {
        'race_count': race_count,
        'average_age_men': average_age_men,
        'percentage_bachelors': percentage_bachelors,
        'higher_education_rich': higher_education_rich,
        'lower_education_rich': lower_education_rich,
        'min_work_hours': min_work_hours,
        'rich_percentage': rich_percentage,
        'highest_earning_country': highest_earning_country,
        'highest_earning_country_percentage': highest_earning_country_percentage,
        'top_IN_occupation': top_IN_occupation
    }

