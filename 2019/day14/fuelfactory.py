#!python3
import math
import collections


def count_fuels(ore_limit, base_chemicals, fuel_formula, leftovers):

    ore_consumed = iter = 0

    while ore_consumed < ore_limit:
        
        fuel_formula = fuel_formula_original.copy()
        
        while True:

            idx = next((index for index, k in enumerate(fuel_formula) if k[1] not in base_chemical_names), None)

            if idx is None:
                break

            count, name = fuel_formula[idx]

            base_idx = next(k for k in cookbook if k[1] == name)

            base_count, base_name = base_idx
            base_components = cookbook[base_idx]

            if name not in leftovers:
                leftovers[name] = 0
            elif leftovers[name] >= count:
                leftovers[name] -= count
                count = 0
                fuel_formula.pop(idx)
                continue
            elif leftovers[name]:
                count -= leftovers[name]
                leftovers[name] = 0

            multiple = math.ceil(count/base_count)
            base_required = multiple*base_count

            leftovers[base_name] += base_required-count
            fuel_formula += [(el[0]*multiple, el[1]) for el in base_components]
                              
            fuel_formula.pop(idx)

            #fuel_formula = sorted(fuel_formula, key=lambda x: relations_count[x[1]])
                              
#        required_counts = collections.OrderedDict()
#        for e in fuel_formula:
#            if e[1] not in required_counts:
#                required_counts[e[1]] = e[0]
#            else:
#                required_counts[e[1]] += e[0]
                
#            fuel_formula = [(c, v) for v, c in required_counts.items()]

#        import pdb; pdb.set_trace()

#        for chemical_name, required_count in required_counts.items():
        for required_count, chemical_name in fuel_formula:

            base_entry = next(e for e in base_materials if e[1] == chemical_name)
            base_count = base_entry[0]

            if chemical_name not in leftovers:
                leftovers[chemical_name] = 0

            if leftovers[chemical_name]:
                if required_count >= leftovers[chemical_name]:
                    required_count -= leftovers[chemical_name]
                    leftovers[chemical_name] = 0
                else:
                    leftovers[chemical_name] -= required_count
                    required_count = 0
                    
            if required_count == 0: continue
            produce_count = math.ceil(required_count/base_count)
            ore = produce_count * base_materials[base_entry]
            leftovers[chemical_name] += produce_count*base_count - required_count
            ore_consumed += ore

        if ore_consumed >= ore_limit:
            break
        iter += 1

        if iter % 10**5 == 0:
            print(f"ore_consumed: {ore_consumed}; fuel produced: {iter};")

    return iter, ore_consumed, leftovers


if __name__ == "__main__":

    cookbook = dict()
    base_materials = dict()
    base_materials_required = dict()
    leftovers = dict()
    converter = lambda v: (int(v[0]), v[1].strip())
    
    with open("input.txt") as f:

        for line in f:
            line = line.replace("=>", ",")
            materials = list(map(converter, (part.strip().split(" ") for part in line.split(","))))
            result = materials.pop()

            if result[1] == "FUEL":
                fuel_reqs = result

            if materials[0][1] == "ORE":
                base_materials[result] = materials[0][0]
            else:
                cookbook[result] = materials

    required_counts = dict()
    fuel_formula_original = cookbook.pop(fuel_reqs)
    base_chemical_names = frozenset(m[1] for m in base_materials)

#    relations_count = dict()
#    keys = fuel_formula_original.copy()
#    while keys:
#        _, name = keys.pop()
#        if name not in relations_count:
#            relations_count[name] = 0
#        relations_count[name] += 1
#        related_entry = next((e for e in cookbook if e[1] == name), None)
#        if related_entry is None:
#            continue
#        keys += cookbook[related_entry]

#    fuels, ore_consumed, leftovers = count_fuels(216477, base_chemical_names, fuel_formula_original, leftovers)
    fuels, ore_consumed, leftovers = count_fuels(10**12, base_chemical_names, fuel_formula_original, leftovers)
    print(f"fuels: {fuels}.")
    fuels_calculated = 10**12 // ore_consumed
    print(f"fuels_calculated: {fuels_calculated}.")
    ore_left = 10**12 - fuels_calculated * ore_consumed
    leftovers = {k: v*fuels_calculated for k,v in leftovers.items()}
    fuels, ore_consumed, leftovers = count_fuels(ore_left, base_chemical_names, fuel_formula_original, leftovers)
    print(fuels_calculated+fuels)
    
    
