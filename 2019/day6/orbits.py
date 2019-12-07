#!python3

ORBIT_SEP = ')'


def build_orbits_map(orbits_input):

    orbits_centers = dict()

    for orbit_description in orbits_input:

        center, orbit = orbit_description.split(ORBIT_SEP)

        if orbit in orbits_centers:
            raise RuntimeError(
                "orbit {} around {} conflicts with what is already registered: {} around {}".format(
                    orbit, center, orbit, orbits_centers[orbit])
            )

        orbits_centers[orbit] = center

    orbits_paths = dict()

    for orbit in orbits_centers:
        orbits_paths[orbit], center = [], orbits_centers[orbit]
        orbits_paths[orbit].append(center)
        while center in orbits_centers:
            center = orbits_centers[center]
            orbits_paths[orbit].append(center)

        if len(orbits_paths[orbit]) == 1:
            root_center = orbits_paths[orbit][0]
            orbits_paths[root_center] = []

    return orbits_paths

def travel(orbits_relations, where, to):

    root_path_from_where, root_path_from_to  = orbits_relations[where], orbits_relations[to]

    closest_common_orbit = None
    for common_orbit in set(root_path_from_where) & set(root_path_from_to):
        if closest_common_orbit is None or len(orbits_relations[closest_common_orbit]) < len(orbits_relations[common_orbit]):
            closest_common_orbit = common_orbit

    dist = root_path_from_where.index(closest_common_orbit)
    dist += root_path_from_to.index(closest_common_orbit)
    orbits_relations[where] = root_path_from_to[:]

    return dist


if __name__ == "__main__":

    with open("input.txt") as f:
        orbits_input = tuple(line.strip() for line in f)

    orbits_relations = build_orbits_map(orbits_input)
    where, to = "YOU", "SAN"
    distance = travel(orbits_relations, where, to)
    print(f"total number of direct and indirect orbits: {sum(len(rel) for rel in orbits_relations.values())}")
    print(f"shortest dist. between {where} and {to}: {distance}.")
