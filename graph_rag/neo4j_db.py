from neo4j import GraphDatabase
import os
from load_dotenv import load_dotenv
load_dotenv()

NEO4J_CONNECTION_URI = os.getenv("NEO4J_URI")
NEO4J_USERNAME = os.getenv("NEO4J_USERNAME")
NEO4J_PASSWORD = os.getenv("NEO4J_PASSWORD")

class Neo4jHandler:
    def __init__(self, connection_url, username, password):
        self.driver = GraphDatabase.driver(connection_url, auth=(username, password))

    def close(self):
        self.driver.close()

    def store_entities_relationships(self, entities, relationships):
        with self.driver.session() as session:
            # store entities
            for entity in entities:
                session.execute_write(self._create_entity_node, entity)

            # store relationships
            for entity1, relationship, entity2 in relationships:
                session.execute_write(self._create_relationship, entity1, relationship, entity2)

    @staticmethod
    def _create_entity_node(tx, entity):
        query = "MERGE (e: Entity {name: $entity_name})"
        tx.run(query, entity_name= entity)

    @staticmethod
    def _create_relationship(tx, entity1, relationship, entity2):
        query = """
                MATCH (e1:Entity {name: $entity1})
                MATCH (e2:Entity {name: $entity2})
                MERGE (e1)-[:RELATION {type: $relationship}]->(e2)
                """
        tx.run(query, entity1=entity1, entity2=entity2, relationship=relationship)

if __name__ == '__main__':
    neo4j_uri = NEO4J_CONNECTION_URI
    print(f'neo4j_uri is {neo4j_uri}')
    neo4j_user = NEO4J_USERNAME
    neo4j_password = NEO4J_PASSWORD
    neo4j_handler = Neo4jHandler(neo4j_uri, neo4j_user, neo4j_password)
    entities = [ 'Abraham_Lincoln']
    relationships = [["Abraham_Lincoln", "was", "sixteenth President of the United States"]]
    neo4j_handler.store_entities_relationships(entities, relationships)
    neo4j_handler.close()

