import plotly.express as px
from shinywidgets import render_plotly, output_widget, render_widget
from shiny.express import input, ui, render
from palmerpenguins import load_penguins
import seaborn as sns
from shiny import render, reactive, req

ui.page_opts(title="Filling layout", fillable=True)


penguins = load_penguins()

ui.page_opts(title="Andrea's Penguin Playground", fillable=False)

with ui.sidebar(open="open"):
    ui.h2("Sidebar")

    
    ui.input_selectize("selected_x_attribute","Select X Attribute",
                       ["bill_length_mm","bill_depth_mm","flipper_length_mm","body_mass_g"])

    ui.input_selectize("selected_y_attribute","Select Y Attribute",
                       ["bill_length_mm","bill_depth_mm","flipper_length_mm","body_mass_g"])
    
    ui.input_numeric("plotly_bin_count","Ploty Bins",10,min=1,max=20)
    ui.input_slider("seaborn_bin_count","Seaborn Bins",1,20,10)

    ui.input_checkbox_group("selected_island","Select Island",
                      ["Torgersen","Dream","Biscoe"],
                      selected=["Torgersen","Dream"],inline=False)
                
    
    ui.input_checkbox_group("selected_species_list","Choose Species",
                           ["Adelie", "Gentoo","Chinstrap"],
                           selected=["Adelie","Gentoo"],
                           inline=False)
    ui.hr()
    ui.a("Andrea's Github",href="https://github.com/andrea-shobe", target="_blank")


with ui.layout_columns():
    with ui.card():
        "Penguins Data Table"
        @render.data_frame
        def penguinstable_df():
            return render.DataTable(filtered_data(),selection_mode='row')
        

    with ui.card():
        "Penguins Data Grid"
        @render.data_frame
        def penguinsgrid_df():
            return render.DataGrid(filtered_island(),selection_mode="row")


with ui.layout_columns():
    with ui.card():
        @render.plot(alt="A Seaborn Histogram")
        def plot():
            df=penguins
            df[input.selected_x_attribute()].hist(grid=False)
            plt=sns.histplot(data=filtered_data(),x="body_mass_g",bins=input.seaborn_bin_count())
            plt.set_title("Palmer Penguins")
            plt.set_xlabel(input.selected_x_attribute())
            plt.set_ylabel("Count")
            return plt
            
    with ui.card():
        "Plotly Histogram"
        @render_plotly
        def plotlyhistogram():
            return px.histogram(filtered_data(),x=input.selected_x_attribute(),
                               nbins=input.plotly_bin_count(), color="species").update_layout(
                xaxis_title="Bill Length (mm)",
                yaxis_title="Count",)

with ui.card(full_screen=True):
    ui.card_header("Plotly Scatterplot: Species")
    @render_plotly
    def plotly_scatterplot():
        return px.scatter(
            data_frame=filtered_data(),
            x=input.selected_x_attribute(),
            y=input.selected_y_attribute(),
            color="species",
            color_discrete_sequence=["red","orange","blue"],
            labels={"body_mass_g": "Body Mass (g)",
                   "bill_depth_mm":"Bill Depth (mm):",
                   "flipper_length_mm":"Flipper Length (mm)",
                    "bill_length_mm":"Bill Length (mm)"},)

@reactive.calc
def filtered_data():
    req(input.selected_species_list())
    isSpeciesMatch=penguins["species"].isin(input.selected_species_list())
    return penguins[isSpeciesMatch]

def filtered_island():
    req(input.selected_island())
    isIslandMatch=penguins["island"].isin(input.selected_island())
    return penguins[isIslandMatch]
    
    
