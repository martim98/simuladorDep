import pandas as pd
import numpy as np


global data_test
data_test = {"PS":[39.16],
              "PSD":[28.02],
              "BE":[6.16],
              "CDS":[1.64],
              "CDU":[5.4],
              "PAN":[2.66],
              "A":[0],
              "Livre":[0.2],
              "IL":[4.1],
              "Chega":[7.36]}



def calculate_deps(data_input, rand, variation=0):
    data_input = pd.DataFrame(data_input)
    data_final_deps_tot = pd.DataFrame()
    dict_test = []
    for scenario in [0, 1, 2]:
        for circ in range(22):
            circ_elei = pd.read_csv("circ_elei.csv")
            res_elei = pd.read_csv("res_elei.csv")

            circ_selec = circ_elei.iloc[circ, 0]
            n_deps = circ_elei.iloc[circ, 1]
            votantes = circ_elei.iloc[circ, 2]

            tot_vec = res_elei[res_elei.circulo=="Total"].iloc[0, 1:11]

            last_sond = data_input.iloc[0, :]



            if scenario == 0:
                to_add = (last_sond - tot_vec)
                circ_baseline = res_elei[res_elei.circulo==circ_selec].iloc[0, 1:11] + to_add
                df_aux = votantes * circ_baseline/100
                df_aux = df_aux.apply(lambda x : x if x > 0  else 0)

                for deps in range(2, n_deps+1):
                    df_aux = pd.concat([df_aux, df_aux[0:10]/deps])

                df_aux = df_aux.sort_values(ascending=False)[:n_deps]

                df_test = pd.DataFrame(df_aux)
                df_test_count = df_test.groupby(by=df_test.index).count()

            elif scenario == 1:
                to_add = (last_sond / tot_vec)
                circ_baseline = res_elei[res_elei.circulo==circ_selec].iloc[0, 1:11] * to_add

                while sum(circ_baseline) > 92:
                    circ_baseline = circ_baseline - circ_baseline*0.1

                df_aux = votantes * (circ_baseline/100)
                df_aux = df_aux.apply(lambda x : x if x > 0  else 0)


                for deps in range(2, n_deps+1):
                    df_aux = pd.concat([df_aux, df_aux[0:10]/deps])

                df_aux = df_aux.sort_values(ascending=False)[:n_deps]

                df_test = pd.DataFrame(df_aux)
                df_test_count = df_test.groupby(by=df_test.index).count()

                df_test.columns = ["value"]
                df_test["Partido"] = df_test.index
                df_test["Circulo"] = circ_selec

                data_final_deps_tot = pd.concat([data_final_deps_tot, df_test])

            elif scenario == 10:
                to_add = (last_sond / tot_vec)
                circ_baseline = res_elei[res_elei.circulo==circ_selec].iloc[0, 1:11] * to_add

                while sum(circ_baseline) > 92:
                    circ_baseline = circ_baseline - circ_baseline*0.1

                df_aux = votantes * (circ_baseline/100)
                df_aux = df_aux.apply(lambda x : x if x > 0  else 0)

                for deps in range(2, n_deps+1):
                    df_aux = pd.concat([df_aux, df_aux[0:10]/deps])

                df_aux = df_aux.sort_values(ascending=False)[:n_deps]

                df_test = pd.DataFrame(df_aux)
                df_test_count = df_test.groupby(by=df_test.index).count()


            elif scenario == 2:
                to_add = (last_sond / tot_vec)
                circ_baseline = res_elei[res_elei.circulo==circ_selec].iloc[0, 1:11] * (to_add)
                while sum(circ_baseline) > 92:
                    circ_baseline = circ_baseline - 0.1
                    circ_baseline= circ_baseline.apply(lambda x : x if x > 0  else 0)

                df_aux = votantes * (circ_baseline/100)
                df_aux = df_aux.apply(lambda x : x if x > 0  else 0)


                for deps in range(2, n_deps+1):
                    df_aux = pd.concat([df_aux, df_aux[0:10]/deps])

                df_aux = df_aux.sort_values(ascending=False)[:n_deps]

                df_test = pd.DataFrame(df_aux)


                df_test_count = df_test.groupby(by=df_test.index).count()



            if circ==0:
                total_deps = df_test_count
            else:
                total_deps = pd.concat([total_deps, df_test_count])



        if scenario==0:
            total_deps_tot = total_deps.groupby(total_deps.index).sum()
            total_deps_tot["scenario"] = "Cenario 1"

        else:
            total_deps_tot_aux = total_deps.groupby(total_deps.index).sum()
            total_deps_tot_aux["scenario"] = "Cenario {}".format(scenario+1)

            total_deps_tot = pd.concat([total_deps_tot, total_deps_tot_aux])


    data_deps_list = []
    # Code to create the deps list

    data_final_deps_tot["rank por circulo"] = data_final_deps_tot.groupby(["Partido", "Circulo"])["value"].rank(ascending=False)
    data_final_deps_tot["rank Global Partido"] = data_final_deps_tot.groupby(["Partido"])["value"].rank(ascending=False)
    
    df_m = pd.read_csv("list_deps.csv")
    data_final_deps_tot_out = df_m.merge(data_final_deps_tot, on=["rank por circulo", "Partido", "Circulo"], how="outer")
    data_final_deps_tot_out = data_final_deps_tot_out.fillna("Nome do deputado por inserir")
    data_final_deps_tot_out = data_final_deps_tot_out[data_final_deps_tot_out.value_y != "Nome do deputado por inserir"]
    data_final_deps_tot_out["Deputado"] = data_final_deps_tot_out.value_x
    data_final_deps_tot_out = data_final_deps_tot_out[["rank por circulo", "Deputado", "Circulo", "Partido"]]

    total_deps_tot.columns = ["deputados", "scenario"]
    total_deps_tot.reset_index(inplace=True)
    total_deps_tot = total_deps_tot.sort_values("deputados", ascending=False)

    final_table = total_deps_tot.pivot(index='index', columns='scenario', values='deputados')

    final_table = final_table.fillna(int(0))
    final_table[final_table.columns] = final_table[final_table.columns].astype(int)
    final_table = final_table.sort_values("Cenario 3", ascending=False)

    final_table.columns = ["Cenário conservador",
                           "Cenário ajustado",
                           "Cenário mais provável"]
    final_table = final_table[["Cenário mais provável", "Cenário conservador","Cenário ajustado"]]


    return final_table, data_final_deps_tot_out






if __name__ == "__main__":
    calculate_deps(data_test, rand=1)



