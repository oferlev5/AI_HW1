import json
import time
import search
import random
import math
import itertools

ids = ["318238839", "206968281"]


def possible_moves(loc, lenrow, lencol):
    lenrow -= 1
    lencol -= 1
    i = loc[0]
    j = loc[1]
    if i != 0 and i != lenrow and j != 0 and j != lencol:
        return [(i - 1, j), (i + 1, j), (i, j - 1), (i, j + 1)]
    if i == 0:
        if j == 0:
            return [(0, 1), (1, 0)]
        elif j == lencol:
            return [(1, j), (0, j - 1)]
        else:
            return [(0, j + 1), (0, j - 1), (1, j)]
    elif i == lenrow:
        if j == 0:
            return [(i - 1, 0), (i, 1)]
        elif j == lencol:
            return [(i - 1, j), (i, j - 1)]
        else:
            return [(i, j + 1), (i, j - 1), (i - 1, j)]

    if j == 0:
        return [(i - 1, j), (i, 1), (i + 1, j)]
    elif j == lencol:
        return [(i - 1, j), (i, j - 1), (i + 1, j)]


def man_distance(point1, point2):
    return abs(point1[0] - point2[0]) + abs(point1[1] - point2[1])


class TaxiProblem(search.Problem):
    """This class implements a medical problem according to problem description file"""

    def __init__(self, initial):
        """Don't forget to implement the goal test
        You should change the initial to your own representation.
        search.Problem.__init__(self, initial) creates the root node"""
        " 'we need to create frist node with state and deliver goal"

        for key in initial["taxis"].keys():
            initial["taxis"][key]['currCap'] = 0
            initial["taxis"][key]['initFuel'] = initial["taxis"][key]["fuel"]

        for key in initial["passengers"].keys():
            initial["passengers"][key]['onTaxi'] = None

        grid = initial["map"]
        g_locations = []
        lenrow = len(grid)
        lencol = len(grid[0])
        for i in range(lenrow):
            for j in range(lencol):
                if grid[i][j] == "G":
                    g_locations.append((i, j))
        initial["Gas_Stations"] = g_locations
        initial = json.dumps(initial)
        search.Problem.__init__(self, initial)

    def actions(self, state):
        """Returns all the actions that can be executed in the given
        state. The result should be a tuple (or other iterable) of actions
        as defined in the problem description file"""
        state = json.loads(state)
        actions_dict = {}
        lenrow, lencol = len(state["map"]), len(state["map"][0])
        for key in state["taxis"].keys():
            actions_dict[key] = []
            ## possible moves
            t_location = state["taxis"][key]["location"]
            moves = possible_moves(t_location, lenrow, lencol)
            for move in moves:
                tile_type = state["map"][move[0]][move[1]]
                if tile_type != 'I' and state["taxis"][key]['fuel'] > 0:
                    to_add = ('move', key, move)
                    actions_dict[key].append(to_add)

            ## pickup and drop off
            taxi_capacity = state['taxis'][key]['capacity']
            taxi_curr_capacity = state['taxis'][key]['currCap']

            for person in state["passengers"].keys():
                person_location = state["passengers"][person]["location"]
                person_dest = state["passengers"][person]["destination"]
                person_on_taxi = state["passengers"][person]["onTaxi"]
                if person_location == t_location and taxi_curr_capacity + 1 <= taxi_capacity and person_on_taxi is None:
                    to_add = ('pick up', key, person)
                    actions_dict[key].append(to_add)
                if person_on_taxi == key and person_dest == t_location:
                    to_add = ('drop off', key, person)
                    actions_dict[key].append(to_add)

            ## refuel
            curr_tile_type = state["map"][t_location[0]][t_location[1]]
            if curr_tile_type == 'G':
                to_add = ("refuel", key)
                actions_dict[key].append(to_add)

            ## wait
            to_add = ("wait", key)
            actions_dict[key].append(to_add)

        combined_actions = []
        for key in actions_dict.keys():
            combined_actions.append(actions_dict[key])
        if len(actions_dict.keys()) == 1:
            name_taxi = list(actions_dict.keys())[0]
            return tuple(actions_dict[name_taxi])

        else:
            ## need to check this!!!
            ## check for no conflict in tiles
            prod_actions = list(itertools.product(*combined_actions))
            final_prod_actions = []
            num_taxis = len(state["taxis"].keys())
            for i in range(len(prod_actions)):
                loc_set = set()
                for j in range(num_taxis):
                    verb = prod_actions[i][j][0]
                    if verb == "move":
                        loc_set.add(tuple(prod_actions[i][j][2]))
                    else:
                        taxi_name = prod_actions[i][j][1]
                        taxi_loc = state["taxis"][taxi_name]["location"]
                        loc_set.add(tuple(taxi_loc))
                if len(loc_set) == num_taxis:
                    final_prod_actions.append(prod_actions[i])

            return tuple(final_prod_actions)

    def result(self, state, action):
        """Return the state that results from executing the given
        action in the given state. The action must be one of
        self.actions(state)."""
        state = json.loads(state)
        num_taxis = len(state["taxis"].keys())
        if num_taxis == 1:
            action = [list(action)]
        else:
            action = list(action)  # []

        for act in action:
            verb = act[0]
            taxi_name = act[1]
            if verb == "move":
                dest = act[2]
                state["taxis"][taxi_name]["location"] = dest
                state["taxis"][taxi_name]["fuel"] -= 1

            elif verb == 'pick up':
                state["taxis"][taxi_name]["currCap"] += 1
                passenger = act[2]
                state["passengers"][passenger]["onTaxi"] = taxi_name
                # state["passengers"][passenger]["location"] = "onTaxi"

            elif verb == 'drop off':
                passenger = act[2]
                state["taxis"][taxi_name]["currCap"] -= 1
                state["passengers"][passenger]["onTaxi"] = "goal"
                state["passengers"][passenger]["location"] = state["taxis"][taxi_name]["location"]

            elif verb == 'refuel':
                state["taxis"][taxi_name]["fuel"] = state["taxis"][taxi_name]["initFuel"]
        # print(state)
        return json.dumps(state)

    def goal_test(self, state):
        """ Given a state, checks if this is the goal state.
         Returns True if it is, False otherwise."""
        state = json.loads(state)
        for passenger in state["passengers"].keys():
            if state["passengers"][passenger]["location"] != state["passengers"][passenger]["destination"]:
                return False
        return True

    def h(self, node):
        """ This is the heuristic. It gets a node (not a state,
        state can be accessed via node.state)
        and returns a goal distance estimate"""
        state = json.loads(node.state)
        D = 0
        T = 0
        h = 0
        dis_from_taxi = 0
        taxis_locations = set()
        cap = 0
        num_taxis = len(state["taxis"].keys())
        for key in state["taxis"].keys():
            cap += state["taxis"][key]["capacity"]
            taxi_location = state["taxis"][key]["location"]
            taxis_locations.add(tuple(taxi_location))
            if state["taxis"][key]["currCap"] != 0:
                min_dist = float('inf')
                for passenger in state["passengers"].keys():
                    if state["passengers"][passenger]["onTaxi"] == key:
                        pass_dest = state["passengers"][passenger]["destination"]
                        min_dist = min(man_distance(taxi_location, pass_dest), min_dist)
                if min_dist > state["taxis"][key]["fuel"]:
                    min_dis_from_gas = float('inf')
                    for station in state["Gas_Stations"]:
                        min_dis_from_gas = min(man_distance(taxi_location, station), min_dis_from_gas)
                    if min_dis_from_gas < state["taxis"][key]["fuel"]:
                        h+= float("-inf")
                    else:
                        h += min_dis_from_gas + 1


        for key in state["passengers"].keys():
            if state["passengers"][key]["onTaxi"] is None:
                h += 2
                loc = state["passengers"][key]["location"]
                dest = state["passengers"][key]["destination"]
                D += man_distance(loc, dest)
                min_val = float('inf')
                for val in taxis_locations:
                    min_val = min(man_distance(loc, val), min_val)
                dis_from_taxi += min_val

            elif state["passengers"][key]["onTaxi"] != 'goal':
                h += 1
                taxi_name = state["passengers"][key]["onTaxi"]
                taxi_loc = state["taxis"][taxi_name]["location"]
                dest = state["passengers"][key]["destination"]
                T += man_distance(taxi_loc, dest)

        h = (h + D + T + dis_from_taxi) / num_taxis
        # print(h)
        # if h > 13:
        #     print(state)
        #     print(h, D, T, dis_from_taxi)
        return h

    def h_1(self, node):
        """
        This is a simple heuristic
        """
        state = json.loads(node.state)
        unpicked = 0
        not_deliverd = 0
        for key in state["passengers"].keys():
            if state["passengers"][key]["onTaxi"] is None:
                unpicked += 1
            elif state["passengers"][key]["onTaxi"] != 'goal':
                not_deliverd += 1
        num_taxis = len(state["taxis"].keys())
        return (unpicked * 2 + not_deliverd) / num_taxis

    def h_2(self, node):
        """
        This is a slightly more sophisticated Manhattan heuristic
        """
        state = json.loads(node.state)
        D = 0
        T = 0
        for key in state["passengers"].keys():
            if state["passengers"][key]["onTaxi"] is None:
                loc = state["passengers"][key]["location"]
                dest = state["passengers"][key]["destination"]
                D += man_distance(loc, dest)
            elif state["passengers"][key]["onTaxi"] != 'goal':
                taxi_name = state["passengers"][key]["onTaxi"]
                taxi_loc = state["taxis"][taxi_name]["location"]
                dest = state["passengers"][key]["destination"]
                T += man_distance(taxi_loc, dest)
        num_taxis = len(state["taxis"].keys())
        return (D + T) / num_taxis

    """Feel free to add your own functions
    (-2, -2, None) means there was a timeout"""


def create_taxi_problem(game):
    return TaxiProblem(game)
