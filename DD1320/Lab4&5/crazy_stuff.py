import networkx as nx
import pickle


def create_graph(words):
    graph = nx.Graph()
    length = len(words)
    for i in range(len(words)):
        print("create_graph", i, "/", length, end='\r')
        for j in range(i + 1, len(words)):
            if abs(len(words[i]) - len(words[j])) <= 1:
                differences = 0
                k = l = 0
                while k < len(words[i]) and l < len(words[j]) and differences <= 1:
                    if words[i][k] != words[j][l]:
                        differences += 1
                        if len(words[i]) > len(words[j]):
                            k += 1
                        elif len(words[i]) < len(words[j]):
                            l += 1
                        else:
                            k += 1
                            l += 1
                    else:
                        k += 1
                        l += 1
                if differences <= 1:
                    graph.add_edge(words[i], words[j])
    print("\n")
    return graph

def main():
    # with open('svenska-ord.txt', 'r', encoding='utf-8') as f:
    #     words = [word.strip() for word in f.readlines()]
    # graph = create_graph(words)
    # with open('graph.pickle', 'wb') as f:
    #     pickle.dump(graph, f)
    with open('graph.pickle', 'rb') as f:
        graph = pickle.load(f)
    print("Finished creating graph", graph.number_of_nodes(), graph.number_of_edges())
    connected_components = nx.connected_components(graph)
    print("Finished finding connected components")
    longest_path = []
    diameters = []
    biggest_diameter = 0
    biggest_subgraph: nx.Graph = None
    for component in connected_components:
        subgraph = graph.subgraph(component)
        diameter = nx.diameter(subgraph)
        diameters.append(diameter)
        if diameter > biggest_diameter:
            biggest_diameter = diameter
            biggest_subgraph = subgraph
    print(diameters)

    periphery_nodes = nx.periphery(biggest_subgraph)
    for i in range(len(periphery_nodes)):
        for j in range(i + 1, len(periphery_nodes)):
            current_path = nx.shortest_path(biggest_subgraph, source = periphery_nodes[i], target = periphery_nodes[j])
            if len(current_path) > len(longest_path):
                longest_path = current_path
                if len(longest_path) - 1 == biggest_diameter:
                    break
    print("\n")
    print("Diameters:", diameters)
    print("Longest path:", longest_path)
    

if __name__ == '__main__':
    main()

# ['avredning', 'avledning', 'anledning', 'inledning', 'inredning', 'inridning', 'inritning', 'inrutning', 'inmutning', 'inmatning', 'imatning', 'matning', 'maning', 'aning', 'ening', 'enig', 'evig', 'vig', 'vag', 'var', 'far', 'för', 'före', 'förse', 'först', 'försåt', 'förlåt', 'förlåta', 'förlita', 'förlisa', 'förläsa', 'förläna', 'förlänga', 'förlägga', 'förelägga', 'föreligga']
# avredning -> avledning -> anledning -> inledning -> inredning -> inridning -> inritning -> inrutning -> inmutning -> inmatning -> imatning -> matning -> maning -> aning -> ening -> enig -> evig -> vig -> vag -> var -> far -> för -> före -> förse -> först -> försåt -> förlåt -> förlåta -> förlita -> förlisa -> förläsa -> förläna -> förlänga -> förlägga -> förelägga -> föreligga