#!python3

import sys

_BAG_SPLIT_TEXT = "bags contain"


def parse_bags(inp) -> dict:

    bags_descriptions = {}

    for line in map(str.strip, inp):

        bag_type, bag_contents = tuple(map(str.strip, line[:-1].split(_BAG_SPLIT_TEXT)))

        for bag_content in map(str.strip, bag_contents.split(',')):

            bag_content = bag_content[:bag_content.rfind(' ')]
            content_bag_count = 0

            if bag_content[0].isnumeric():
                end_idx = bag_content.index(' ')
                content_bag_count = int(bag_content[0:end_idx])
                bag_content = bag_content[end_idx+1:]

            content_bag_type = bag_content

            if content_bag_count == 0:
                continue

            bags_descriptions.setdefault(bag_type, dict())[content_bag_type] = content_bag_count

    return bags_descriptions


def calculate_inner_bags(bags_tree: dict, bag_type: str) -> int:

    if bag_type not in bags_tree:
        return 0

    sub_tree = bags_tree[bag_type]

    s = sum(
        bags_count if bag_type not in bags_tree
        else bags_count + bags_count * calculate_inner_bags(bags_tree, bag_type)
        for bag_type, bags_count in sub_tree.items()
    )

    return s


def main(args):

    if len(args) != 3:
        print(f"Cmd line: {args[0]} <input_file> <bag_type>")
        return 1

    bags = {}
    
    with open(args[1]) as inp:
        bags = parse_bags(inp)

    starting_bag = args[2]
    
    print(f"Answer: {calculate_inner_bags(bags, starting_bag)}.")

    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
