from py2neo import Graph, Node, Relationship
graph = Graph("bolt://127.0.0.1:7687", username="neo4j", password='800515')

cypher = 'MATCH(p:Person) return p'

nodes_data = graph.run(cypher).data()

for node in nodes_data:
    print(node)