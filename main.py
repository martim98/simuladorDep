# Run this app with `python app.py` and
# visit http://127.0.0.1:8050/ in your web browser.


import pandas as pd
import dash
import dash_core_components as dcc
import dash_html_components as html
import dash_table
from dash.dependencies import Output, Input
import plotly.graph_objs as go
import plotly.express as px
from test_draw import data_test
from copy import deepcopy



df = pd.read_csv("data_sond.csv")
app = dash.Dash(__name__)

app.layout = html.Div([html.H1(["Politica",
                                html.Span(" 230", style={"color":"#e68200", "-webkit-text-stroke":"0.7px black"})], style={"text-align":"center",
                                                  "font-size":"50pt","background-color":"#7d98ba",
                                                  "padding":"15px","margin-top": "-10px", "margin-bottom":"-10px", "margin-left":"40px", "margin-right":"40px"}),

                       html.H2("Simulador de deputados eleitos"),
                       html.H2("Instruções", style={"color":"#e68200", "-webkit-text-stroke":"0.2px black"}),
                       html.H3("1º Coloque nas caixas em baixo a percentagem de intenção de voto para cada partido", style={"text-align":"center"}),
                       html.H3("2º As Tabelas atualizam automaticamente, calculando o numero de deputados para cada partido", style={"text-align":"center"}),
                       html.H3("3º O total de inteção de votos dos partidos em baixo tem que estar entre 88% e 95%", style={"text-align":"center"}),
                       html.Div([
                           html.Div([
                           html.H3("PS %"),
                           dcc.Input(className="sliders",
                               id='PS_v',
                                type="number",
                               min=0,
                               max=100,
                               step=1,
                               value=data_test["PS"][0])], style={"width":"10%","display":"inline-block"}),

                           html.Div([
                           html.H3("PSD %"),
                           dcc.Input(className="sliders",
                               id='PSD_v',
                               type="number",
                               min=0,
                               max=100,
                               step=1,
                               value=data_test["PSD"][0])], style={"width":"10%","display":"inline-block"}),

                           html.Div([
                           html.H3("BE %"),
                           dcc.Input(className="sliders",
                               id='BE_v',
                                     type="number",
                               min=0,
                               max=100,
                               step=1,
                               value=data_test["BE"][0])], style={"width":"10%", "display":"inline-block"}),
                           html.Div([
                           html.H3("CDS %"),
                           dcc.Input(className="sliders",
                               id='CDS_v',
                                     type="number",
                               min=0,
                               max=100,
                               step=1,
                               value=data_test["CDS"][0])], style={"width":"10%", "display":"inline-block"}),
                           html.Div([
                           html.H3("CDU %"),
                           dcc.Input(className="sliders",
                               id='CDU_v',
                                     type="number",
                               min=0,
                               max=100,
                               step=1,
                               value=data_test["CDU"][0])], style={"width":"10%","display":"inline-block"}),
                           html.Div([
                           html.H3("PAN %"),
                           dcc.Input(className="sliders",
                               id='PAN_v',
                                     type="number",
                               min=0,
                               max=100,
                               step=1,
                               value=data_test["PAN"][0])], style={"width":"10%","display":"inline-block"}),
                           html.Div([
                           html.H3("Livre %"),
                           dcc.Input(className="sliders",
                               id='Livre_v',
                                     type="number",
                               min=0,
                               max=100,
                               step=1,
                               value=data_test["Livre"][0])], style={"width":"10%","display":"inline-block"}),
                           html.Div([
                           html.H3("Iniciativa Liberal %"),
                           dcc.Input(className="sliders",
                               id='IL_v',
                                     type="number",
                               min=0,
                               max=100,
                               step=1,
                               value=data_test["IL"][0])], style={"width":"10%", "display":"inline-block"}),
                           html.Div([
                           html.H3("Chega %"),
                           dcc.Input(className="sliders",
                               id='Chega_v',
                                     type="number",
                               min=0,
                               max=100,
                               step=1,
                               value=data_test["Chega"][0])], style={"width":"10%","display":"inline-block"}),

                            html.Div([html.H2("88% < ", style={"display":"inline-block"}),
                                html.H2(id="disp_tot", style={"display":"inline-block", "color":"#e68200", "-webkit-text-stroke":"0.7px black"}),
                                      html.H2(" < 95%", style={"display":"inline-block"})
                            ], style = {"text-align":"center"})

                       ], style={ "background-color":"#7d98ba",
                                  "margin":"40px", "text-align":"left", "padding-left":"30px"}),

                        html.Div([

                        html.Div([
                        html.H3("Numero de deputados eleitos:", style={"text-align":"center"}),
                        html.P("Maioria absoluta >= 116 deputados"),
                        dash_table.DataTable(id="output-container", sort_action="native",
                                             style_cell={"text-align":"center","font-size":"15pt"})]),

                        html.Div([
                        html.H3("Deputados por circulo e partido:", style={"text-align":"center"}),
                        dash_table.DataTable(id="output-container2", sort_action="native",
                                             sort_mode="multi",
                                             style_table={'minWidth': '100%'},
                                             page_size= 15,
                                             style_cell={"text-align":"center" ,"font-size":"15pt"})]),

                        html.Div([
                        html.H2("Evolução das sondagens"),
                        dcc.Graph(figure= px.line(df[(df.Mês > "2016-01") & (df.Partido!="Outros") ], x="Mês", y="Intenção de voto", color="Partido"), style={"clear":"left"})]),

                       html.H1(id="a")], style={"margin-left": "40px",
                                                "margin-right":"40px"})



                   ], style={"font-family":"Helvetica",
                             "text-align":"center"})


from test_draw import calculate_deps
@app.callback(
    [Output(component_id="output-container", component_property="columns"),
     Output(component_id="output-container", component_property="data"),
     Output(component_id="disp_tot", component_property="children"),

     # Output(component_id="PS_v", component_property="marks"),
     # Output(component_id="PSD_v", component_property="marks"),
     # Output(component_id="BE_v", component_property="marks"),
     # Output(component_id="CDS_v", component_property="marks"),
     # Output(component_id="CDU_v", component_property="marks"),
     # Output(component_id="PAN_v", component_property="marks"),
     # Output(component_id="Livre_v", component_property="marks"),
     # Output(component_id="IL_v", component_property="marks"),
     # Output(component_id="Chega_v", component_property="marks"),

     Output(component_id="output-container2", component_property="columns"),
     Output(component_id="output-container2", component_property="data")],

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

    data_p= {"PS":[a],
                 "PSD":[b],
                 "BE":[c],
                 "CDS":[d],
                 "CDU":[e],
                 "PAN":[f],
                 "A":[0],
                 "Livre":[g],
                 "IL":[h],
                 "Chega":[i]}


    data_test = deepcopy({i:[round(data_p[i][0], 2)] for i in data_p.keys()})

    total_n =int(a+b+c+d+e+f+g+h+i)
    total = " " + str(round(a+b+c+d+e+f+g+h+i, 1)) + "% "

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
        b, c = calculate_deps(data_test, 1)
        b.insert(0, 'Partidos', b.index)
        columns = [{"name":i, "id":i} for i in b.columns]
        data = b.to_dict("records")

        columns2 = [{"name":i, "id":i} for i in c.columns]
        data2 = c.to_dict("records")

    else:
        b = pd.DataFrame({"Erro":["Total acima de 95% ({})%, reduza algum dos valores até perfazer abaixo de 95".format(total_n)]})
        columns = [{"name":i, "id":i} for i in b.columns]
        data = b.to_dict("records")
        columns2 = columns
        data2 = data



    return columns, data, [total], \
           columns2, data2
           #dicts_store[0],dicts_store[1],dicts_store[2],dicts_store[3],dicts_store[4],dicts_store[5],dicts_store[6],dicts_store[7],dicts_store[8],\





if __name__ == '__main__':
    app.run_server(host="0.0.0.0")