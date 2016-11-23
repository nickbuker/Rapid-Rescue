import numpy as np


def allocator(units, preds):
    """
    Input:
    units = Integer number of emergency response units available
    preds = Dictionary with predictions by zone
    Output: Allocation dictionary with zones:units
    """
    # Determine total predicted responses for later proportioning
    total = sum(tup[1] for tup in preds)
    # Sort preds for allocation priority if units < 7
    preds = sorted(preds, key=lambda x: x[1], reverse=True)

    if units < 7:
        # Create allocation dict
        alloc = {'zone1':0, 'zone2':0, 'zone3':0, 'zone4':0,
                 'zone5':0, 'zone6':0, 'zone7':0}
        slot = 0
        while units >= 1:
            # Assigns unit to highest predicted zone w/o a unit assigned
            alloc[preds[slot][0]] += 1
            slot += 1
            units -= 1
        return alloc

    else:
        # Create allocation dict and distribute one unit to each zone
        alloc = {'zone1':1, 'zone2':1, 'zone3':1, 'zone4':1,
                 'zone5':1, 'zone6':1, 'zone7':1}
        units -= 7
        # Portion out remaing units based on predicted responses
        for tup in preds:
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
