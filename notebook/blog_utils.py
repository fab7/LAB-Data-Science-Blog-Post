"""
This module contains utilities and helper functions to plot the pie and bar charts of the Blog Post project.
"""

import matplotlib.pyplot as plt
import pandas as pd
import networkx as nx


def pie_chart(df, df_title, fig_save=False):
    """
    Plots a pie chart showing the proportions of the passed series.
    
    Parameters:
      df (DataFrame): A frame to visualize
      df_title (string): The title of the pie chart
      fig_save (boolean): Will keep a copy of the figure in the './images/' directory
    """
    (df.nlargest(10)/df.sum()).plot(kind='pie', autopct='%1.1f%%', ylabel='', legend=None);
    plt.title(df_title);
    if fig_save:
        plt.savefig('./images/' + df_title.replace(" ", "_") +'.jpg')
    plt.show();
    
help(pie_chart)


def two_pie_chart(df1, df1_title, df2, df2_title, mode, fig_title, fig_save=False):
    """
    Plots two pie charts together and showing the proportions of the passed series.
    
    Parameters:
      df1 (DataFrame): First data frame
      df1_title (string): The title of the 1st pie chart
      df2 (DataFrame): Second data frame
      df2_title (string): The title of the 2ndt pie chart
      mode (string): To display the sub-plots side-by-side (mode='row) or top-bottom (mode='col').
      fig_title(string): The name of the figure to save.
      fig_save (boolean): Will keep a copy of the figure in './images/' directory)
    """
    if mode == 'row':
        fig, axes = plt.subplots(nrows=1, ncols=2, sharey=True, figsize=(14, 12))
        fig.subplots_adjust(wspace=0.4)
    elif mode == 'col':
        fig, axes = plt.subplots(nrows=2, ncols=1, sharex=True, figsize=(14, 12))
        fig.subplots_adjust(wspace=0.4)
        
    fig.tight_layout()
    fig.subplots_adjust(top=0.9)
    
    # Only plot the 10 largest values
    (df1.nlargest(10)/df1.sum()).plot(ax=axes[0], kind='pie', autopct='%1.1f%%', ylabel='', title=df1_title, legend=None);
    (df2.nlargest(10)/df2.sum()).plot(ax=axes[1], kind='pie', autopct='%1.1f%%', ylabel='', title=df2_title, legend=None);

    if fig_save:
        plt.savefig('./images/' + fig_title.replace(" ", "_") +'.jpg')
    plt.show()
    
help(two_pie_chart)


def barh_chart(sr, fig_title, color, fig_save=False):
    """
    Plots an horizontal bar chart per job type.
    
    Parameters:
      sr (Series): A serie of values
      sr_title (string): The title of the bar chart figure
      color (string): The color of the bars in RGB color code
      fig_save (boolean): Will keep a copy of the figure in './images/' directory)
    """
    
    # [Credits] This code is inspired from https://mode.com/example-gallery/python_horizontal_bar/
    
    # Convert the serie into a DataFrame
    df = pd.DataFrame(sr)

    # Add a new column 'Percentage' to the DataFrame
    if 'count' in df.columns:
        total = df['count'].sum()
        df['Percentage'] = df['count'] / total * 100
    
    # Truncate the dataframe above 30
    if len(sr) > 30:
        sr = sr.head(30)
        df = df.head(30)
    ax = sr.plot(kind='barh', figsize=(8, 10), color=color, zorder=2, width=0.85)
          
    # Add a title
    plt.title(fig_title, loc='left');
   
    # Remove the lines that border the data area of a plot (aka spines)
    ax.spines['right'].set_visible(False)
    ax.spines['top'].set_visible(False)
    ax.spines['left'].set_visible(False)
    ax.spines['bottom'].set_visible(False)
   
    # Switch off the ticks
    ax.tick_params(axis="both", which="both", 
                   bottom="off", left="off", 
                   labelbottom="off", labelleft="off")

    # Draw vertical axis lines
    vals = ax.get_xticks()
    for tick in vals:
        ax.axvline(x=tick, linestyle='dashed', alpha=0.4, color='#eeeeee', zorder=1)

    # Set x-axis label
    if 'count' in df.columns:
        ax.set_xlabel("Number of Responses", labelpad=20, weight='bold', size=12)
    elif 'ConvertedCompYearly' in df.columns:
        ax.set_xlabel("Median salary (in USD)", labelpad=20, weight='bold', size=12)

    # Set y-axis label
    ax.set_ylabel("Job Type", labelpad=20, weight='bold', size=12)
    
    # Add percentages as text annotations
    if 'count' in df.columns and 'Percentage' in df:
        for i, value in enumerate(df['count']):
            ax.text(value, i, f' {df["Percentage"][i]:.1f}%', ha='left', va='center')
        
    if fig_save:
        plt.savefig('./images/' + fig_title.replace(" ", "_") +'.jpg')
        
help(barh_chart)


def rust_dependency_graph(df_admirers, df_users, fig_title, render='both', seed=42, fig_save=False):
    """
    Builds a graph showing the daily programming language used by the Rust admirers, as well as the languages that the Rust users want to work with. 
    
    Parameters:
      df_admirers (DataFrame): The Rust admirers
      df_users (DataFrame): The Rust users
      render (string): The rendering mode (both|admirers|users) 
      fig_title(string): The name of the figure to plot and to save.
      fig_save (boolean): Will keep a copy of the figure in './images/' directory)
    
    Returns:
      A dataframe containing the nodes with columns: 'Names', 'Colors', 'Children' and 'Weights'   
    """
    
    # Create a pandas DataFrame with the dependencies
    Nodes = {
        'Names'    : [ 'Rust'  ],
        'Colors'   : ['#EBAA03'],
        'Children' : [   []  ],
        'Weights'  : [   []  ]
    }
   
    # Drop rows with missing language values
    df_users = df_users.dropna(subset=['LanguageWantToWorkWith'])
    
    # === RUST USERS ============================================
    if render == 'both' or render == 'users':
        for id, row in df_users.iterrows():
            # Access row values using row[column_name]
            next_languages = row['LanguageWantToWorkWith'].split(';')
            for language in next_languages:
                dst_lang = language + '_'
                if dst_lang in Nodes['Children'][0]:
                    # Retrieve the position in the list
                    index = Nodes['Children'][0].index(dst_lang)
                    Nodes['Weights'][0][index] += 1       
                else:
                    # Add a new child to the Rust node
                    Nodes['Children'][0].append(dst_lang)
                    Nodes['Weights'][0].append(1)
                   
    # === RUST ADMIRERS =========================================
    if render == 'both' or render == 'admirers': 
        for id, row in df_admirers.iterrows():
            # Access row values using row[column_name]
            curr_languages = row['LanguageHaveWorkedWith'].split(';')
            for language in curr_languages:
                src_lang = '_' + language
                if src_lang in Nodes['Names']:
                    # Retrieve the position in the list
                    index = Nodes['Names'].index(src_lang)
                    # Increment the 'Rust' child
                    Nodes['Weights'][index][0] += 1       
                else:
                    # Add a new node to the graph 
                    Nodes['Names'].append(src_lang)
                    Nodes['Colors'].append('#FF0000')  # Redish
                    # Create a 'Rust' child for this node
                    Nodes['Children'].append(['Rust'])
                    Nodes['Weights'].append([1])
              
    # === PREPARE FOR WEIGHT NORMALIZATION ======================
    # Note: We won't color the nodes accodingly because it becomes unreadable :-(
    # df_weights = pd.DataFrame(Nodes['Weights'], columns=['weights'])
    # min_weight = df_weights['weights'].min()
    # max_weight = df_weights['weights'].max()    
    
    # === DRAW GRAPH ============================================
    df = pd.DataFrame(Nodes)
      
    # Create an empty graph
    graph = nx.DiGraph()

    # Add the 'FROM-LANGUAGE' nodes to the graph
    for id, node, in enumerate(df['Names']):
        if node == 'Rust':
            graph.add_node(node, color='#EBAA03')  # Yellow/Brown
        else:         
            # Normalize the weight
            #  Note: We won't color the nodes accodingly because it becomes unreadable :-(
            #  norm_weight = (df['Weights'][id] - min_weight) / (max_weight - min_weight)
            # Generate a color between 50 and 250
            #  r_hex = hex(int(200 * norm_weight) + 50)
            #  rgb_hex = '#' + r_hex + '0000'
            graph.add_node(node, color='#FF5354')    # Redish ('#FF5354')
       
    # Add the 'TO_LANGUAGE' nodes to the graph
    for id1, children in enumerate(df['Children']):
        for id2, node in enumerate(children):
            if node != 'Rust':
                graph.add_node(node, color='#0095FF')  # Blueish ('#0095FF')
    
    # Add edges to the graph
    for node, children, weights in zip(df['Names'], df['Children'], df['Weights']):
        for child, weight in zip(children, weights):
            graph.add_edge(node, child, weight=weight)

    # Construct the color map for the nodes 
    color_map = list((nx.get_node_attributes(graph, 'color')).values())

    # Visualize the graph
    if render == "both" :
        plt.figure(figsize=(15, 10))
        #pos = nx.shell_layout(graph)
        pos = nx.random_layout(graph, seed=seed)
    elif render == "admirers":
        plt.figure(figsize=(16, 14))
        #pos = nx.spring_layout(graph, seed=seed)
        #pos = nx.shell_layout(graph)
        pos = nx.circular_layout(graph)
    elif render == "users":
        plt.figure(figsize=(16, 14))
        pos = nx.shell_layout(graph)
    nx.draw_networkx(graph, pos, with_labels=True, node_color=color_map, node_size=1000, edge_color='gray', arrows=True)

    # Add node labels
    # nx.draw_networkx_labels(graph, pos, font_size=10, font_family="sans-serif")
    # Add edge weight labels
    edge_labels = nx.get_edge_attributes(graph, "weight")
    nx.draw_networkx_edge_labels(graph, pos, edge_labels)
    
    # Save to file
    if fig_save:
        plt.savefig('./images/' + fig_title.replace(" ", "_") + "_" + str(seed) + '.jpg')

    # Plot
    plt.title(fig_title)
    plt.tight_layout()
    plt.show()
    
    return df
    

help(rust_dependency_graph)



###############################
##     A NETWORKX EXAMPLE    ##
###############################

def a_networkx_exemple():
    # Create a pandas DataFrame with the dependencies
    data = {
        'Node'      : ['A', 'B', 'C', 'D'],
        'Dependency': [['B', 'C'], ['B','D'], [], []]
    }
    df = pd.DataFrame(data)

    # Create an empty graph
    graph = nx.DiGraph()

    # Add nodes to the graph
    graph.add_nodes_from(df['Node'])

    # Add edges to the graph
    for node, dependencies in zip(df['Node'], df['Dependency']):
        for dependency in dependencies:
            graph.add_edge(node, dependency)

    # Visualize the graph
    plt.figure(figsize=(8, 6))
    pos = nx.spring_layout(graph)
    nx.draw_networkx(graph, pos, with_labels=True, node_color='lightblue', node_size=1000, edge_color='gray', arrows=True)
    plt.title('Dependency Graph')
    plt.show()
    
    
###################################
##  A WEIGHTED NETWORKX EXAMPLE  ##
###################################

def a_weighted_networkx_exemple():
    G = nx.Graph()

    G.add_edge("a", "b", weight=0.6)
    G.add_edge("a", "c", weight=0.2)
    G.add_edge("c", "d", weight=0.1)
    G.add_edge("c", "e", weight=0.7)
    G.add_edge("c", "f", weight=0.9)
    G.add_edge("a", "d", weight=0.3)

    elarge = [(u, v) for (u, v, d) in G.edges(data=True) if d["weight"] > 0.5]
    esmall = [(u, v) for (u, v, d) in G.edges(data=True) if d["weight"] <= 0.5]

    pos = nx.spring_layout(G, seed=7)  # positions for all nodes - seed for reproducibility

    # nodes
    nx.draw_networkx_nodes(G, pos, node_size=700)

    # edges
    nx.draw_networkx_edges(G, pos, edgelist=elarge, width=6)
    nx.draw_networkx_edges(
        G, pos, edgelist=esmall, width=6, alpha=0.5, edge_color="b", style="dashed"
    )

    # node labels
    nx.draw_networkx_labels(G, pos, font_size=20, font_family="sans-serif")
    # edge weight labels
    edge_labels = nx.get_edge_attributes(G, "weight")
    nx.draw_networkx_edge_labels(G, pos, edge_labels)

    ax = plt.gca()
    ax.margins(0.08)
    plt.axis("off")
    plt.tight_layout()
    plt.show()
