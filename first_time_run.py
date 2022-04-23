import osmnx as ox
import networkx as nx


baseGraph = ox.graph_from_place(["Jurong West, Singapore"],network_type="drive")
patch_1 = ox.graph_from_bbox(1.355281,1.350249,103.727885,103.714557,network_type='bike')
mainGraph = nx.compose(baseGraph,patch_1)
ox.io.save_graphml(mainGraph,"jurong.graphml")
