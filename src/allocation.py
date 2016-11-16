import numpy as np

def allocator(units, y1, y2, y3, y4, y5, y6, y7):
    """
    Input:
    units = Integer number of emergency response units available
    y1 through y7 = Predicted responses in zones 1 through 7
    Output: Allocation dictionary with zones:units
    """
    total = y1 + y2 + y3 + y4 + y5 + y6 + y7
    preds = [y1, y2, y3, y4, y5, y6, y7]
    zones = ['z1', 'z2', 'z3', 'z4', 'z5', 'z6', 'z7']
    zipper = zip(zones, preds)
    zipper = sorted(zipper, key=lambda x: x[1], reverse=True)

    if units < 7:
        # Create allocation dict
        alloc = {'z1':0, 'z2':0, 'z3':0, 'z4':0, 'z5':0, 'z6':0, 'z7':0}
        slot = 0
        while units >= 1:
            # Assigns unit to highest predicted zone w/o a unit assigned
            alloc[zipper[slot][0]] += 1
            slot += 1
            units -= 1
        return alloc

    else:
        # Create allocation dict and distribute one unit to each zone
        alloc = {'z1':1, 'z2':1, 'z3':1, 'z4':1, 'z5':1, 'z6':1, 'z7':1}
        units -= 7
        # Portion out remaing units based on predicted responses
        for tup in zipper:
            alloc[tup[0]] += units * tup[1] // total
        # Adjust number of resources left
        units -= (sum(alloc.values()) - 7)
        # If resources all allocated, return results
        if units == 0:
            return alloc
        # If resources remain, assign to zone with least units
        else:
            while units >= 1:
                # Finds key with lowest value and adds unit
                alloc[min(alloc, key=alloc.get)] += 1
                units -= 1
            return alloc
