# Run this app with `python app.py` and
# visit http://127.0.0.1:8050/ in your web browser.


import pandas as pd
import dash
import dash_core_components as dcc
import dash_html_components as html
import dash_table
from dash.dependencies import Output, Input
from test_draw import data_test



app = dash.Dash(__name__)

app.layout = html.Div([html.H1("Politica 230", style={"text-align":"center", "font-size":"40pt","background-color":"#68C0E3",
                                                      "padding":"15px",
                                                      "margin-top": "-10px", "margin-bottom":"-10px", "margin-left":"10px", "margin-right":"10px"}),

                       html.H2("Simulador de deputados eleitos"),
                       html.H3("Insira aqui os resultados das sondagens:", style={"text-align":"left", "margin-left":"10px"}),
                       html.Div([
                           html.H3("PS"),
                           dcc.Slider(
                               id='PS_v',
                               min=0,
                               max=100,
                               step=0.1,
                               value=data_test["PS"][0],
                               #marks={i:str(i) for i in range(0, 110, 10)},
                               tooltip={"placement": "top", "always_visible": True}),

                           html.H3("PSD"),
                           dcc.Slider(
                               id='PSD_v',
                               min=0,
                               max=100,
                               step=0.1,
                               value=data_test["PSD"][0],
                               tooltip={"placement": "top", "always_visible": True}),

                           html.H3("BE"),
                           dcc.Slider(
                               id='BE_v',
                               min=0,
                               max=100,
                               step=0.1,
                               value=data_test["BE"][0],
                               tooltip={"placement": "top", "always_visible": True}),

                           html.H3("CDS"),
                           dcc.Slider(
                               id='CDS_v',
                               min=0,
                               max=100,
                               step=0.1,
                               value=data_test["CDS"][0],
                               tooltip={"placement": "top", "always_visible": True}),

                           html.H3("CDU"),
                           dcc.Slider(
                               id='CDU_v',
                               min=0,
                               max=100,
                               step=0.1,
                               value=data_test["CDU"][0],
                               tooltip={"placement": "top", "always_visible": True}),

                           html.H3("PAN"),
                           dcc.Slider(
                               id='PAN_v',
                               min=0,
                               max=100,
                               step=0.1,
                               value=data_test["PAN"][0],
                               tooltip={"placement": "top", "always_visible": True}),

                           html.H3("Livre"),
                           dcc.Slider(
                               id='Livre_v',
                               min=0,
                               max=100,
                               step=0.1,
                               value=data_test["Livre"][0],
                               tooltip={"placement": "top", "always_visible": True}),

                           html.H3("Iniciativa Liberal"),
                           dcc.Slider(
                               id='IL_v',
                               min=0,
                               max=100,
                               step=0.1,
                               value=data_test["IL"][0],
                               tooltip={"placement": "top", "always_visible": True}),

                           html.H3("Chega"),
                           dcc.Slider(
                               id='Chega_v',
                               min=0,
                               max=100,
                               step=0.1,
                               value=data_test["Chega"][0],
                               tooltip={"placement": "top", "always_visible": True})

                       ], style={"float":"left", "width":"30%", "background-color":"#68C0E3", "margin":"10px"}),

                        html.Div([
                        html.H2(id="disp_tot", style={"text-align":"center"}),
                        html.H3("O total deve estar entre 88% - 94%", style={"text-align":"center"}),
                        html.H3("Numero de deputados eleitos:", style={"text-align":"left"}),
                        dash_table.DataTable(id="output-container", sort_action="native", style_cell={"text-align":"center"}),
                       html.H1(id="a")], style={"float":"left", "width":"65%"})



                   ], style={"font-family":"Helvetica",
                             "text-align":"center"})


from test_draw import calculate_deps
@app.callback(
    [Output(component_id="output-container", component_property="columns"),
     Output(component_id="output-container", component_property="data"),
     Output(component_id="disp_tot", component_property="children")],
    [Input(component_id="PS_v", component_property="value"),
     Input(component_id="PSD_v", component_property="value"),
     Input(component_id="BE_v", component_property="value"),
     Input(component_id="CDS_v", component_property="value"),
     Input(component_id="CDU_v", component_property="value"),
     Input(component_id="PAN_v", component_property="value"),
     Input(component_id="Livre_v", component_property="value"),
     Input(component_id="IL_v", component_property="value"),
     Input(component_id="Chega_v", component_property="value")]
)

def create_table(a, b, c, d, e, f, g,h,i ):

    data_test = {"PS":[a],
                 "PSD":[b],
                 "BE":[c],
                 "CDS":[d],
                 "CDU":[e],
                 "PAN":[f],
                 "A":[0],
                 "Livre":[g],
                 "IL":[h],
                 "Chega":[i]}

    total_n =int(a+b+c+d+e+f+g+h+i)
    total =  "Total: " + str(total_n) + "%"

    if total_n <95 and total_n>=88:
        b = calculate_deps(data_test, 1)
        b.insert(0, 'Partidos', b.index)
        columns = [{"name":i, "id":i} for i in b.columns]
        data = b.to_dict("records")
    else:
        b = pd.DataFrame({"Erro":["Total acima de 95% ({})%, reduza algum dos valores até perfazer abaixo de 95".format(total_n)]})
        columns = [{"name":i, "id":i} for i in b.columns]
        data = b.to_dict("records")


    return columns, data, [total]



if __name__ == '__main__':
    app.run_server(debug=True, port=2000)