from pyswip import Prolog
import os

class PrologBridge:
    def __init__(self, knowledge_base_path):
        self.prolog = Prolog()
        # Convert path to forward slashes and make it absolute
        abs_path = os.path.abspath(knowledge_base_path)
        # Use forward slashes for Prolog
        prolog_path = abs_path.replace('\\', '/')
        try:
            self.prolog.consult(prolog_path)
        except Exception as e:
            print(f"Error consulting Prolog file: {e}")
            print(f"Attempted path: {prolog_path}")
    
    def query(self, query_str):
        """Execute a Prolog query and return results"""
        try:
            return list(self.prolog.query(query_str))
        except Exception as e:
            print(f"Error executing Prolog query: {e}")
            return []
    
    def assert_fact(self, fact):
        """Add a new fact to the knowledge base"""
        try:
            self.prolog.assertz(fact)
            return True
        except Exception as e:
            print(f"Error asserting fact: {e}")
            return False
    
    def retract_fact(self, fact):
        """Remove a fact from the knowledge base"""
        try:
            self.prolog.retract(fact)
            return True
        except Exception as e:
            print(f"Error retracting fact: {e}")
            return False
    
    def retract_all(self, predicate):
        """Remove all facts matching a predicate"""
        try:
            self.prolog.retractall(predicate)
            return True
        except Exception as e:
            print(f"Error retracting all facts: {e}")
            return False
    
    def assert_list(self, facts):
        """Add multiple facts to the knowledge base"""
        try:
            for fact in facts:
                self.prolog.assertz(fact)
            return True
        except Exception as e:
            print(f"Error asserting facts: {e}")
            return False 