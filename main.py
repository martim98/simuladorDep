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
                       html.H3("Mova os sliders conforme os resultados e a tabela atualiza automaticamente:", style={"text-align":"left", "margin-left":"10px"}),
                       html.P("Nota: os intervalos sugeridos em cada slider são apenas sugestivos para que a soma total não ultrapasse os 95% ou seja inferior a 88% ",
                              style={"text-align":"left", "margin-left":"10px"}),
                       html.Div([
                           html.H2(id="disp_tot", style={"text-align":"center"}),
                           html.P("O total deve estar entre 88% - 94%", style={"text-align":"center"}),
                           html.H3("PS %"),
                           dcc.Slider(className="sliders",
                               id='PS_v',
                               min=0,
                               max=100,
                               step=0.1,
                               value=data_test["PS"][0],
                               #marks={i:str(i) for i in range(0, 110, 10)},
                               tooltip={"placement": "top", "always_visible": True}),

                           html.H3("PSD %"),
                           dcc.Slider(className="sliders",
                               id='PSD_v',
                               min=0,
                               max=100,
                               step=0.1,
                               value=data_test["PSD"][0],
                               tooltip={"placement": "top", "always_visible": True}),

                           html.H3("BE %"),
                           dcc.Slider(className="sliders",
                               id='BE_v',
                               min=0,
                               max=100,
                               step=0.1,
                               value=data_test["BE"][0],
                               tooltip={"placement": "top", "always_visible": True}),

                           html.H3("CDS %"),
                           dcc.Slider(className="sliders",
                               id='CDS_v',
                               min=0,
                               max=100,
                               step=0.1,
                               value=data_test["CDS"][0],
                               tooltip={"placement": "top", "always_visible": True}),

                           html.H3("CDU %"),
                           dcc.Slider(className="sliders",
                               id='CDU_v',
                               min=0,
                               max=100,
                               step=0.1,
                               value=data_test["CDU"][0],
                               tooltip={"placement": "top", "always_visible": True}),

                           html.H3("PAN %"),
                           dcc.Slider(className="sliders",
                               id='PAN_v',
                               min=0,
                               max=100,
                               step=0.1,
                               value=data_test["PAN"][0],
                               tooltip={"placement": "top", "always_visible": True}),

                           html.H3("Livre %"),
                           dcc.Slider(className="sliders",
                               id='Livre_v',
                               min=0,
                               max=100,
                               step=0.1,
                               value=data_test["Livre"][0],
                               tooltip={"placement": "top", "always_visible": True}),

                           html.H3("Iniciativa Liberal %"),
                           dcc.Slider(className="sliders",
                               id='IL_v',
                               min=0,
                               max=100,
                               step=0.1,
                               value=data_test["IL"][0],
                               tooltip={"placement": "top", "always_visible": True}),

                           html.H3("Chega %"),
                           dcc.Slider(className="sliders",
                               id='Chega_v',
                               min=0,
                               max=100,
                               step=0.1,
                               value=data_test["Chega"][0],
                               tooltip={"placement": "top", "always_visible": True})

                       ], style={"float":"left", "width":"30%", "background-color":"#68C0E3", "margin":"10px", "text-align":"left", "padding":"10px"}),

                        html.Div([
                        html.H3("Numero de deputados eleitos:", style={"text-align":"left"}),

                        dash_table.DataTable(id="output-container", sort_action="native",
                                             style_cell={"text-align":"center"}),
                       html.H1(id="a")], style={"float":"left", "width":"65%"})



                   ], style={"font-family":"Helvetica",
                             "text-align":"center"})


from test_draw import calculate_deps
@app.callback(
    [Output(component_id="output-container", component_property="columns"),
     Output(component_id="output-container", component_property="data"),
     Output(component_id="disp_tot", component_property="children"),

     Output(component_id="PS_v", component_property="marks"),
     Output(component_id="PSD_v", component_property="marks"),
     Output(component_id="BE_v", component_property="marks"),
     Output(component_id="CDS_v", component_property="marks"),
     Output(component_id="CDU_v", component_property="marks"),
     Output(component_id="PAN_v", component_property="marks"),
     Output(component_id="Livre_v", component_property="marks"),
     Output(component_id="IL_v", component_property="marks"),
     Output(component_id="Chega_v", component_property="marks")],

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

    dicts_store = []
    for value in data_test.keys():

        if value == "A":
            continue
        perc = float(data_test[value][0])
        spare_max = 95 - total_n
        spare_min = total_n - 88
        val_max = round(perc + spare_max, 1)
        val_min = round(perc - spare_min, 1)


        if val_min <0:
            val_min=0
        if val_max > 100:
            val_max=100
        dict_aux = {val_min: {'label': "", "style": {'color':'#FF8700'}}, val_max:{'label': "", "style":{'color':'#FF8700'}}}
        dicts_store.append(dict_aux)

    if total_n <95 and total_n>=88:
        b = calculate_deps(data_test, 1)
        b.insert(0, 'Partidos', b.index)
        columns = [{"name":i, "id":i} for i in b.columns]
        data = b.to_dict("records")
    else:
        b = pd.DataFrame({"Erro":["Total acima de 95% ({})%, reduza algum dos valores até perfazer abaixo de 95".format(total_n)]})
        columns = [{"name":i, "id":i} for i in b.columns]
        data = b.to_dict("records")


    return columns, data, [total], dicts_store[0],dicts_store[1],dicts_store[2],dicts_store[3],dicts_store[4],dicts_store[5],dicts_store[6],dicts_store[7],dicts_store[8]



if __name__ == '__main__':
    app.run_server(host='0.0.0.0')