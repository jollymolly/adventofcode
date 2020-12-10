#!python3

import sys

_BAG_SPLIT_TEXT = "bags contain"


def main(args):

    if len(args) != 3:
        print(f"Cmd line: {args[0]} <input_file> <bag_type>")
        return 1

    with open(args[1]) as inp:

        bags_descriptions = {}

        for line in map(str.strip, inp):

            bag_type, bag_contents = tuple(map(str.strip, line[:-1].split(_BAG_SPLIT_TEXT)))

            bags_descriptions[bag_type] = {}

            for bag_content in map(str.strip, bag_contents.split(',')):

                bag_content = bag_content[:bag_content.rfind(' ')]
                content_bag_count = 0

                if bag_content[0].isnumeric():
                    end_idx = bag_content.index(' ')
                    content_bag_count = int(bag_content[0:end_idx])
                    bag_content = bag_content[end_idx+1:]

                content_bag_type = bag_content

                bags_descriptions[bag_type][content_bag_type] = content_bag_count

    target_bag = args[2]
    
    bags = [b for b in bags_descriptions if target_bag in bags_descriptions[b]]
    looked_up_bags = set()

    while bags:
        target_bag = bags.pop(0)
        if target_bag in looked_up_bags:
            continue
        looked_up_bags.add(target_bag)
        bags += {b for b in bags_descriptions if target_bag in bags_descriptions[b]}
        
    print(f"Answer: {len(looked_up_bags)}.")
    return 0

if __name__ == "__main__":
    sys.exit(main(sys.argv))
