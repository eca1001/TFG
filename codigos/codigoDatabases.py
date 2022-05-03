#!/usr/bin/env python
# coding: utf-8

import webbrowser
import pandas as pd
import networkx as nx
import matplotlib.pyplot as plt
import math as math
import community.community_louvain as com
import itertools
from bokeh.io import save
from bokeh.models import Range1d, Circle, ColumnDataSource, MultiLine, NodesAndLinkedEdges, LabelSet
from bokeh.plotting import figure
from bokeh.plotting import from_networkx
from bokeh.palettes import Spectral8
import xlsxwriter


def inicial(): #solo es necesario si no se tiene guardado el grafo
    path='stack-overflow-developer-survey-2021'
    public=pd.read_csv(path+'/survey_results_public.csv')
    G = nx.Graph()
    
    for a in range(len(public)):
        nodoDatabase = public.to_numpy()[a][18]
    
        if str(nodoDatabase) != "nan":
            listaDb = nodoDatabase.split(';')

            for e in itertools.combinations(listaDb,2):
                if G.has_edge(e[0],e[1]):
                    G.edges[e[0],e[1]]['weight']+=1 
                else:
                    G.add_edge(e[0],e[1],weight=1)

    #Guardar grafo
    nx.write_graphml(G, "grafosTecnologias/grafoDatabases.graphml")
    return G



def leerGrafo():
    #Cargar grafo
    G = nx.read_graphml("grafosTecnologias/grafoDatabases.graphml")
    return G



def poda(G, umbral):
    H = nx.Graph()
    for e in itertools.combinations(G.nodes(),2):
        peso = G.edges[e[0],e[1]]['weight']
        if peso >= umbral:
            H.add_edge(e[0],e[1],weight=peso)
    return H


def comunidades(G):
    partition = com.best_partition(G)
    partOrd = sorted(partition.items(), key=lambda x: x[1])
    comunidades = list()
    i=0

    while i <= partOrd[len(partOrd)-1][1]:
        listaNueva = list()
        comunidades.append(listaNueva)
        i+=1

    for p in partOrd:
        comunidades[p[1]].append(p[0])
        
    return comunidades



def gradosNodos(G, umbral):
    lista = list()
    for d in G.degree():
        lista.append(d[1])
    fig=plt.figure(figsize=(7,7))
    plt.pie(lista, labels=G.nodes(), autopct='%1.1f%%')
    plt.title('Porcentaje de relación de la Base de datos \n', fontsize = 20)
    plt.axis("equal")
    plt.savefig("static/images/graficosSectores/GraficoSectoresDb.jpg")



def propiedadesRed(G, umbral):
    eje_x = ['Densidad', 'Transitividad', 'Promedio de agrupación']
    eje_y = [round(nx.density(G)*100,2), round(nx.transitivity(G)*100,2), round(nx.average_clustering(G)*100,2)]
    fig=plt.figure()
    plt.title('Propiedades de la red', fontsize = 20)
    plt.bar(eje_x, eje_y)
    for i in range(len(eje_y)):
        plt.annotate(eje_y[i], (i, eje_y[i]+1))
    
    plt.savefig("static/images/histogramas/histogramaDb.jpg")



def calculaModularidad(G, particion):
    valor = 0
    i=0
    lista = []
    for i in particion:
        for j in i:
            lista.append(j)
    
    if len(lista)==len(G.nodes()) and len(particion)==1:
        return 0
    elif len(lista) == 1:
        valor = -1/math.pow(2*len(G.edges()),2)
        suma=0
        for i in lista:
            suma+=math.pow(G.degree(i),2)
        resultado = round(suma*valor , 5)
        return resultado
    else:
        suma=0
        x=0
        for i in particion:
            long=len(i)
            valA = long/len(G.edges())
            se = set()
            for j in i:
                se.add(j[0])
                se.add(j[1])
            
            su=0
            for s in se:
                su+=G.degree(s)
            valB=su/(2*len(G.edges()))
            
            valB = math.pow(valB,2)
            x = valA - valB
            suma+=x
        return round(suma, 5)



def grafoInteractivo(G, umbral):
    edges = dict(nx.degree(G))
    nx.set_node_attributes(G, name='edge', values=edges)

    number_to_adjust_by = 5
    adjusted_node_size = dict([(node, edge+number_to_adjust_by) for node, edge in nx.degree(G)])
    nx.set_node_attributes(G, name='adjusted_node_size', values=adjusted_node_size)

    comun = comunidades(G)

    # Create empty dictionaries
    communityNumber = {}
    community_color = {}
    modularity = {}
    
    pagerank = nx.pagerank(G)
    degree = nx.degree_centrality(G)
    betweenness = nx.betweenness_centrality(G)
    closeness = nx.closeness_centrality(G)
    eigenvector = nx.eigenvector_centrality(G)

    #Loop through each community in the network
    for community_number, community in enumerate(comun):
        #For each member of the community, add their community number and a distinct color
        for name in community: 
            communityNumber[name] = community_number
            community_color[name] = Spectral8[community_number]
            modularity[name] = calculaModularidad(G,[{name}])
        

    #Choose colors for node and edge highlighting
    node_highlight_color = 'white'
    edge_highlight_color = 'black'

    nx.set_node_attributes(G, modularity, 'modularity')
    nx.set_node_attributes(G, pagerank, 'pagerank')
    nx.set_node_attributes(G, degree, 'degree')
    nx.set_node_attributes(G, betweenness, 'betweenness')
    nx.set_node_attributes(G, closeness, 'closeness')
    nx.set_node_attributes(G, eigenvector, 'eigenvector')
    nx.set_node_attributes(G, communityNumber, 'communityNumber')
    nx.set_node_attributes(G, community_color, 'community_color')

    #Choose attributes from G network to size and color by — setting manual size (e.g. 10) or color (e.g. 'skyblue') also allowed
    size_by_this_attribute = 'adjusted_node_size'
    color_by_this_attribute = 'community_color'

    #Choose a title!
    title = 'Red de Relación de Bases de datos'

    #Establish which categories will appear when hovering over each node
    HOVER_TOOLTIPS = [
        ("Base de datos", "@index"),
        ("Enlaces", "@edge"),
        ("Modularidad", "@modularity"),
        ("Influencia", "@pagerank"),
        ("Grado", "@degree"),
        ("Intermediación", "@betweenness"),
        ("Importancia", "@closeness"),
        ("Prestigio", "@eigenvector"),
        ("Número Comunidad", "@communityNumber"),
        ("Color Comunidad", "$color[swatch]:community_color"),
    ]

    #Crear grafo 
    grafo = figure(tooltips = HOVER_TOOLTIPS,tools="pan,wheel_zoom,save,reset", 
              active_scroll='wheel_zoom',x_range=Range1d(-12, 12), y_range=Range1d(-12, 12), title=title)

    network_graph = from_networkx(G, nx.circular_layout, scale=10, center=(0, 0))

    #Establecer los tamaños y colores de los nodos según su grado
    network_graph.node_renderer.glyph = Circle(size=size_by_this_attribute, fill_color=color_by_this_attribute)

    #Resaltar nodos seleccionado
    network_graph.node_renderer.hover_glyph = Circle(size=size_by_this_attribute, fill_color=node_highlight_color, line_width=2)
    network_graph.node_renderer.selection_glyph = Circle(size=size_by_this_attribute, fill_color=node_highlight_color, line_width=2)

    #Tamaño y Opacidad de los enlaces
    network_graph.edge_renderer.glyph = MultiLine(line_alpha=0.3, line_width=1)

    #Resaltar enlaces conectados sobre nodo seleccionado
    network_graph.edge_renderer.selection_glyph = MultiLine(line_color=edge_highlight_color, line_width=2)
    network_graph.edge_renderer.hover_glyph = MultiLine(line_color=edge_highlight_color, line_width=2)

    #Representación de nodos y enlaces
    network_graph.selection_policy = NodesAndLinkedEdges()
    network_graph.inspection_policy = NodesAndLinkedEdges()

    grafo.renderers.append(network_graph)

    #Añadir etiquetas de nombre a los nodos
    x, y = zip(*network_graph.layout_provider.graph_layout.values())
    node_labels = list(G.nodes())
    source = ColumnDataSource({'x': x, 'y': y, 'name': [node_labels[i] for i in range(len(x))]})
    labels = LabelSet(x='x', y='y', text='name', source=source, background_fill_color='white', text_font_size='10px', background_fill_alpha=.7)
    grafo.renderers.append(labels)

    #Mostrar grafo
    #show(grafo)
    save(grafo, filename=f"static/images/grafos/{title}.html")
    

def vecinos(G, umbral):
    libro = xlsxwriter.Workbook('excel/vecinos/vecinosDb.xlsx')
    hoja = libro.add_worksheet()
    lista = {}

    for d in G.degree():
        lista[d[0]] = d[1]
    
    diccionario = {}
    for g in G.nodes():
        veci = list(G.neighbors(g))
        nLis = list()
        for v in veci:
            nNod = (v, round((lista[v]/(G.number_of_nodes()-1))*100),2)
            nLis.append(nNod)
        
        listaOrd = sorted(nLis, key=lambda x: x[1], reverse=True)
        diccionario[g]=listaOrd
    
    ma = 0
    row = 1
    col = 0
    for k, v in diccionario.items():
        hoja.write(row, col, k)
        for sp in v:
            col+=1
            hoja.write(row, col, sp[0])
        if col>ma:
            ma=col
        row+=1
        col=0
    
    i=1
    
    hoja.write(0, 0, "Base de datos")
    
    if ma > 3:
        ma = 3
    
    while i <= ma:
        hoja.write(0, i, "Recomendado"+" "+str(i))
        i+=1
    
    #Cerramos el libro
    libro.close()
    if ma==3:
        df = pd.read_excel("excel/vecinos/vecinosDb.xlsx", usecols=("A:D"))
    elif ma==2:
        df = pd.read_excel("excel/vecinos/vecinosDb.xlsx", usecols=("A:C"))
    else:
        df = pd.read_excel("excel/vecinos/vecinosDb.xlsx", usecols=("A:B"))

    df.fillna('', inplace=True)
    df.to_html('static/images/tablas/tablaVecinosDb.html', justify='center', col_space=100, table_id="myTable")

def crearTablaFiltro():
    a = open('static/images/tablas/tablaVecinosDb.html','r')
    f = open('static/images/tablaFiltro/tablaConFiltroDb.html','w')
    mensaje1="""
    <html>
    <head>
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <style>
    * {
    box-sizing: border-box;
    }

    #myInput {
    background-position: 10px 10px;
    background-repeat: no-repeat;
    width: 100%;
    font-size: 16px;
    padding: 12px 20px 12px 40px;
    border: 1px solid #ddd;
    margin-bottom: 12px;
    }

    #myTable {
    border-collapse: collapse;
    width: 100%;
    border: 1px solid #ddd;
    font-size: 18px;
    }

    #myTable th, #myTable td {
    text-align: left;
    background-color: #CEE4FF;
    padding: 12px;
    min-width: 150px;
    }

    #myTable th, #myTable td:first-child {
    text-align: center;
    background-color: #63A7F9;
    padding: 12px;
    min-width: 8px;
    max-width: 8px;
    }

    #myTable tr {
    border-bottom: 1px solid #ddd;
    }

    #myTable tr.header, #myTable tr:hover {
    background-color: #f1f1f1;
    }
    </style>
    </head>
    <body>

    <h2><b><center>RECOMENDADOR DE BASES DE DATOS</center></b></h2>

    <input type="text" id="myInput" onkeyup="myFunction()" placeholder="Filtrar por base de datos..." title="Type in a name">
    """
    f.write(mensaje1)

    for g in a:
        f.write(g)

    a.close()

    mensaje2="""
    <script>
    function myFunction() {
    var input, filter, table, tr, td, i, txtValue;
    input = document.getElementById("myInput");
    filter = input.value.toUpperCase();
    table = document.getElementById("myTable");
    tr = table.getElementsByTagName("tr");
    for (i = 0; i < tr.length; i++) {
        td = tr[i].getElementsByTagName("td")[0];
        if (td) {
        txtValue = td.textContent || td.innerText;
        if (txtValue.toUpperCase().indexOf(filter) > -1) {
            tr[i].style.display = "";
        } else {
            tr[i].style.display = "none";
        }
        }      
    }
    }
    </script>

    </body>
    </html>
    """
    f.write(mensaje2)
    f.close()


def nodosRestantes(G, H):
    nF = G.nodes()-H.nodes()
    libro = xlsxwriter.Workbook('excel/faltantes/faltantesDb.xlsx')
    hoja = libro.add_worksheet()
    
    row = 1
    col = 0
    for n in nF:
        hoja.write(row, col, n)
        row+=1
    
    hoja.write(0, 0, "Bases de datos No Conectadas")
    
    #Cerramos el libro
    libro.close()
    
    df = pd.read_excel("excel/faltantes/faltantesDb.xlsx")

    df.fillna('', inplace=True)
    df.to_html('static/images/tablas/tablaDbFaltantes.html', justify='center', col_space=100, table_id="myTable")

def crearTablaFiltroRestantes():
    a = open('static/images/tablas/tablaDbFaltantes.html','r')
    f = open('static/images/tablaFiltro/tablaConFiltroRestantesDb.html','w')
    mensaje1="""
    <html>
    <head>
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <style>
    * {
    box-sizing: border-box;
    }

    #myInput {
    background-position: 10px 10px;
    background-repeat: no-repeat;
    width: 100%;
    font-size: 16px;
    border: 1px solid #ddd;
    margin-bottom: 12px;
    }

    #myTable {
    border-collapse: collapse;
    width: 100%;
    border: 1px solid #ddd;
    font-size: 18px;
    }

    #myTable th, #myTable td {
    text-align: left;
    background-color: #CEE4FF;
    padding: 8px;
    }

    #myTable th, #myTable td:first-child {
    text-align: center;
    background-color: #63A7F9;
    padding: 8px;
    }

    #myTable tr {
    border-bottom: 1px solid #ddd;
    }

    #myTable tr.header, #myTable tr:hover {
    background-color: #f1f1f1;
    }
    </style>
    </head>
    <body>

    <input type="text" id="myInput" onkeyup="myFunction()" placeholder="Filtrar por base de datos..." title="Type in a name">
    """
    f.write(mensaje1)

    for g in a:
        f.write(g)

    a.close()

    mensaje2="""
    <script>
    function myFunction() {
    var input, filter, table, tr, td, i, txtValue;
    input = document.getElementById("myInput");
    filter = input.value.toUpperCase();
    table = document.getElementById("myTable");
    tr = table.getElementsByTagName("tr");
    for (i = 0; i < tr.length; i++) {
        td = tr[i].getElementsByTagName("td")[0];
        if (td) {
        txtValue = td.textContent || td.innerText;
        if (txtValue.toUpperCase().indexOf(filter) > -1) {
            tr[i].style.display = "";
        } else {
            tr[i].style.display = "none";
        }
        }      
    }
    }
    </script>

    </body>
    </html>
    """
    f.write(mensaje2)
    f.close()


def ejecutar(umbral):

    try:
        G = leerGrafo()
    except FileNotFoundError:
        G = inicial()
    
    peso = 0
    maxi = 0
    for e in itertools.combinations(G.nodes(),2):
        peso = G.edges[e[0],e[1]]['weight']
        if peso > maxi:
            maxi = peso
    
    H = poda(G, maxi * (umbral/100))
    gradosNodos(H,umbral)
    propiedadesRed(H,umbral)
    grafoInteractivo(H, umbral)
    vecinos(H, umbral)
    crearTablaFiltro()
    nodosRestantes(G,H)
    crearTablaFiltroRestantes()


