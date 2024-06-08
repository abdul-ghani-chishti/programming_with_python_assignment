from bokeh.plotting import figure, show

# prepare some data
x = [1, 2, 3, 4, 5]
y = [6, 7, 2, 4, 5]

# create a new plot with a title and axis labels
p = figure(title="Simple line example", x_axis_label="x", y_axis_label="y")

# add a line renderer with legend and line thickness
p.line(x, y, legend_label="Temp.", line_width=2)
c = p.line(x, y, legend_label="Temp 1.", line_width=4)

# show the results
show(p)
show(c)


#  ###############################################

# Graphing
def plot_data_with_bokeh(x_train, y_train, x_test, y_test, chosen_functions, mappings):
    try:
        p = figure(title="Training Data, Ideal Functions, Test Data, and Mappings",
            x_axis_label='x', y_axis_label='y', width=800, height=600)
        
        # Plot training data
        for i in range(y_train.shape[1]):
            p.circle(x_train, y_train[:, i], legend_label=f'Training y{
                    i+1}', size=6, alpha=0.6)
        print("ab")
        sys.exit()
        # Plot ideal functions
        x_range = np.linspace(min(x_train), max(x_train), 500)
        for i, params in enumerate(chosen_functions):
            y_range = ideal_function(x_range, *params)
            p.line(x_range, y_range, legend_label=f'Ideal Function {
                i+1}', line_width=2)

        # Plot test data
        p.circle(x_test, y_test, legend_label='Test Data',
                color='black', size=6, alpha=0.6)

        # Plot mappings with deviation
        mapped_x = [x for x, y, a, b,
                    deviation in mappings if a is not None and b is not None]
        mapped_y = [y for x, y, a, b,
                    deviation in mappings if a is not None and b is not None]
        deviations = [deviation for x, y, a, b,
                    deviation in mappings if a is not None and b is not None]
        source = ColumnDataSource(
            data=dict(x=mapped_x, y=mapped_y, deviation=deviations))
        p.circle('x', 'y', source=source, color='red', size=10,
                alpha=0.6, legend_label='Mapped Test Data')

        hover = HoverTool()
        hover.tooltips = [("x", "@x"), ("y", "@y"), ("deviation", "@deviation")]
        p.add_tools(hover)

        p.legend.location = "top_left"
        output_file("data_analysis.html")
        show(p)
    except Error as e:
        print(f"Wrong ! {e}")
