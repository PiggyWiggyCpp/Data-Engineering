import pandas as pd
from bokeh.io import output_file, save
from bokeh.models import ColumnDataSource, HoverTool, Range1d, Select, CustomJS, Div
from bokeh.plotting import figure
from bokeh.layouts import column
from bokeh.transform import factor_cmap

color_palette = {
    'Child': 'orchid',
    'Young Adult': 'orange',
    'Adult': 'cyan',
    'Senior': 'blue',
    'female': 'pink',
    'male': 'skyblue',
    1: 'red',
    2: 'green',
    3: 'yellow'
}


def load_data(filepath):
    return pd.read_csv(filepath)


# Data Preparation
def prepare_data(data):
    data = data[data['Fare'] > 0].copy()
    data['Age'] = data['Age'].fillna(data['Age'].median())
    data['Cabin'] = data['Cabin'].fillna('Unknown')
    data['Embarked'] = data['Embarked'].fillna(data['Embarked'].mode()[0])

    bins = [0, 12, 24, 64, float('inf')]
    labels = ['Child', 'Young Adult', 'Adult', 'Senior']
    data['AgeGroup'] = pd.cut(data['Age'], bins=bins, labels=labels, right=False)

    survival_rate = data.groupby('AgeGroup', observed=False)['Survived'].mean() * 100
    data['SurvivalRate'] = data['AgeGroup'].map(survival_rate)

    return data


# Visualization
def age_group_survival(data):
    data_grouped = data.groupby('AgeGroup', observed=False)['Survived'].mean().reset_index()
    data_grouped['SurvivalRate'] = data_grouped['Survived'] * 100
    data_grouped['Color'] = data_grouped['AgeGroup'].map(color_palette)
    data_grouped = data_grouped.sort_values('SurvivalRate', ascending=False)

    age_group_source = ColumnDataSource(data_grouped)

    age_group_plot = figure(
        x_range=data_grouped['AgeGroup'].tolist(),
        height=700,
        width=900,
        title="Survival Rate by Age Group",
        toolbar_location=None,
        tools="hover",
        tooltips="@AgeGroup: @SurvivalRate%",
        x_axis_label='Age Group',
        y_axis_label='Survival Rate (%)'
    )

    age_group_plot.vbar(
        x='AgeGroup',
        top='SurvivalRate',
        width=0.9,
        source=age_group_source,
        legend_field="AgeGroup",
        line_color='white',
        fill_color='Color'
    )

    age_group_plot.add_tools(HoverTool(tooltips=[("Age Group", "@AgeGroup"), ("Survival Rate", "@SurvivalRate%")]))
    age_group_plot.xgrid.grid_line_color = None
    age_group_plot.y_range.start = 0
    age_group_plot.y_range.end = 100

    age_group_filter = Select(title="Age Group", value="All", options=["All"] + data['AgeGroup'].unique().tolist())
    age_group_filter.js_on_change('value', CustomJS(args=dict(source=age_group_source, plot=age_group_plot), code="""
        const value = cb_obj.value;
        const data = source.data;
        if (value === "All") {
            plot.x_range.factors = data['AgeGroup'];
        } else {
            plot.x_range.factors = [value];
        }
        plot.change.emit();
    """))

    return column(age_group_plot, age_group_filter)


def class_and_gender(data):
    class_gender_survival = data.groupby(['Pclass', 'Sex'])['Survived'].mean().unstack().reset_index()
    class_gender_survival.columns.name = None
    class_gender_survival = class_gender_survival.melt(id_vars='Pclass', var_name='Sex', value_name='SurvivalRate')
    class_gender_survival['x'] = class_gender_survival['Pclass'].astype(str) + '-' + class_gender_survival['Sex']

    class_gender_source = ColumnDataSource(class_gender_survival)
    color_mapper = factor_cmap('Sex', palette=[color_palette['female'], color_palette['male']],
                               factors=['female', 'male'])

    class_gender_plot = figure(
        x_range=class_gender_survival['x'].unique(),
        height=700,
        width=900,
        title="Survival Rate by Class and Gender",
        toolbar_location=None,
        tools="hover",
        tooltips="@x: @SurvivalRate%",
        x_axis_label='Class and Gender',
        y_axis_label='Survival Rate (%)'
    )

    class_gender_plot.vbar(
        x='x',
        top='SurvivalRate',
        width=0.4,
        source=class_gender_source,
        legend_field="Sex",
        line_color='white',
        fill_color=color_mapper
    )

    class_gender_plot.add_tools(HoverTool(tooltips=[("Class and Gender", "@x"), ("Survival Rate", "@SurvivalRate%")]))
    class_gender_plot.xgrid.grid_line_color = None
    class_gender_plot.y_range.start = 0
    class_gender_plot.y_range.end = class_gender_survival['SurvivalRate'].max() + 1
    class_gender_plot.legend.title = 'Gender'
    class_gender_plot.legend.location = 'top_left'
    class_gender_plot.legend.orientation = 'horizontal'

    class_gender_filter = Select(title="Class and Gender", value="All",
                                 options=["All"] + class_gender_survival['x'].unique().tolist())
    class_gender_filter.js_on_change('value',
                                     CustomJS(args=dict(source=class_gender_source, plot=class_gender_plot), code="""
        const value = cb_obj.value;
        const data = source.data;
        if (value === "All") {
            plot.x_range.factors = data['x'];
        } else {
            plot.x_range.factors = [value];
        }
        plot.change.emit();
    """))

    return column(class_gender_plot, class_gender_filter)


def fare_vs_survival(data):
    data['Color'] = data['Pclass'].map(color_palette)

    fare_survival_plot = figure(
        title="Fare vs Survival",
        x_axis_label='Fare',
        y_axis_label='Survived',
        width=1600,
        height=800,
        tools="hover"
    )

    for pclass in data['Pclass'].unique():
        subset = data[data['Pclass'] == pclass]
        source = ColumnDataSource(subset)
        fare_survival_plot.scatter(
            x='Fare',
            y='Survived',
            source=source,
            fill_color=color_palette[pclass],
            size=12,
            fill_alpha=0.6,
            legend_label=f"Class {pclass}"
        )

    fare_survival_plot.xaxis.axis_label = 'Fare'
    fare_survival_plot.yaxis.axis_label = 'Survival Status'
    fare_survival_plot.yaxis.ticker = [0, 1]
    fare_survival_plot.y_range = Range1d(start=-0.1, end=1.1)
    fare_survival_plot.x_range = Range1d(start=0, end=210)
    fare_survival_plot.legend.title = 'Class'

    fare_survival_plot.add_tools(
        HoverTool(tooltips=[("Fare", "@Fare"), ("Survived", "@Survived"), ("Class", "@Pclass")]))
    fare_survival_plot.legend.click_policy = "hide"

    legend_note = Div(text="<b>Legend is clickable!!!</b>", styles={'font-size': '30px', 'text-align': 'center'})

    return column(fare_survival_plot, legend_note)


# Output
def save_plots(age_group_plot, class_gender_plot, fare_survival_plot):
    output_file('age_group_survival.html')
    save(age_group_plot)
    output_file('class_gender_survival.html')
    save(class_gender_plot)
    output_file('fare_survival.html')
    save(fare_survival_plot)


def main():
    data = load_data('Titanic-Dataset.csv')
    data = prepare_data(data)
    age_group_plot = age_group_survival(data)
    class_gender_plot = class_and_gender(data)
    fare_survival_plot = fare_vs_survival(data)
    save_plots(age_group_plot, class_gender_plot, fare_survival_plot)


if __name__ == '__main__':
    main()
