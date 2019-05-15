'''
Created on May 7, 2019

@author: Jordan
'''


class MonteCarlo(object):
    
    def __init__(self, root, **kwargs):
        # Takes an instance of a Board and optionally some keyword
        # arguments.  Initializes the list of game states and the
        # statistics tables.
        self.initial_node = root
    
    def best_action(self, num_simulations):
        
        for sim in range(0, num_simulations):
            selected_node = self.expand_tree()
            simulation_result = selected_node.rollout()
            selected_node.backpropogate(simulation_result)

        best_choice_node = self.initial_node.best_child(c_param = 0)
        return best_choice_node.generated_by
    
    def traverse(self):
        node = self.initial_node
        while node.has_children() and node.untried_actions == []:
            node = node.best_child()
        return node
    
    #TODO: Fix expansion of nodes, so far I don't think it goes deep enough 
    def expand_tree(self):
        current_node = self.traverse()
        if current_node.fully_expanded() == False:
            return current_node.expand()
        else:
            return current_node