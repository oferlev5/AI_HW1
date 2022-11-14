import itertools

dict = {
    "map": [['P', 'P', 'P', 'P'],
            ['P', 'P', 'P', 'P'],
            ['P', 'I', 'G', 'P'],
            ['P', 'P', 'P', 'P'], ],
    "taxis": {'taxi 1': {"location": (3, 3),
                         "fuel": 15,
                         "capacity": 2}},
    "passengers": {'Yossi': {"location": (0, 0),
                             "destination": (2, 3)},
                   'Moshe': {"location": (3, 1),
                             "destination": (0, 0)}
                   }
}

dict["taxis"]["taxi 1"]["curCap"] = 0
# print(dict [0])


# print(dict)


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

        # print(possible_moves((2,1),3,4))



# actions_dict = {}
#
# for key in dict["taxis"].keys():
#     location = key["location"]
#     moves = possible_moves(location, lenrow, lencol)
#     for move in moves:
#          tile_type = dict["map"][location[0]][location[1]]
#          if move not in taxis_locations and tile_type != 'I':
#             to_add = ('move', key, move)
#             actions_dict[key].add(to_add)


list1 = [[(1,2),(3,4)], [(5,6),(7,8)]]

print(list(itertools.product(*list1)))
x = ((('move', 'taxi 1', (2, 3)), ('move', 'taxi 2', (1, 3))), (('move', 'taxi 1', (2, 3)), ('move', 'taxi 2', (2, 2))), (('move', 'taxi 1', (2, 3)), ('move', 'taxi 2', (3, 3))), (('move', 'taxi 1', (3, 2)), ('move', 'taxi 2', (1, 3))), (('move', 'taxi 1', (3, 2)), ('move', 'taxi 2', (2, 2))), (('move', 'taxi 1', (3, 2)), ('move', 'taxi 2', (3, 3))), (('move', 'taxi 1', (3, 2)), ('wait', 'taxi 2')), (('wait', 'taxi 1'), ('move', 'taxi 2', (1, 3))), (('wait', 'taxi 1'), ('move', 'taxi 2', (2, 2))), (('wait', 'taxi 1'), ('wait', 'taxi 2')))
