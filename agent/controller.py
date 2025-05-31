from utils.prolog_bridge import PrologBridge
import os

class SnakeController:
    def __init__(self):
        knowledge_base_path = os.path.join(os.path.dirname(__file__), '../prolog/snake_knowledge.pl')
        self.prolog = PrologBridge(knowledge_base_path)
    
    def get_next_move(self, snake_head, snake_body, food_pos, width, height):
        """Get the next move for the snake using Prolog reasoning"""
        # Convert positions to Prolog format
        head = [snake_head[0], snake_head[1]]
        body = [[x, y] for x, y in snake_body]
        food = [food_pos[0], food_pos[1]]
        
        # Query Prolog for best direction
        query = f"best_direction({head}, {food}, {body}, {width}, {height}, Direction)"
        results = self.prolog.query(query)
        
        if results:
            return results[0]['Direction']
        
        # If no valid move found, try to find any safe direction
        safe_query = "direction(Direction), not(unsafe(Direction))"
        safe_results = self.prolog.query(safe_query)
        
        if safe_results:
            return safe_results[0]['Direction']
        
        return None  # Return None if no valid move found
    
    def update_knowledge(self, game_state):
        """Update the knowledge base with new game state information"""
        # Add any new facts or rules based on game state
        pass 