#!python3
import argparse
import os
import pathlib
import re
import networkx
import matplotlib.pyplot

MARKDOWN_LINK_REGEX = r"\[[\d\w ]*\]\([ ]?([\w/:\d.]*)[ ]?\)"

parser = argparse.ArgumentParser()
parser.add_argument("path", nargs="?", default=".")

links = {}


def check_dir(path):
    for file in os.listdir(path):
        filepath = os.path.join(path, file)
        if os.path.isfile(filepath) and \
                pathlib.Path(filepath).suffix == ".md":
            with open(filepath) as f:
                links[filepath] = [os.path.realpath(os.path.join(path, x)) for x in
                                   re.findall(MARKDOWN_LINK_REGEX, f.read())]
                f.close()
        elif os.path.isdir(filepath):
            check_dir(filepath)


def list_concat(list_of_lists):
    return [inner for outer in list_of_lists for inner in outer]


if __name__ == '__main__':
    args = parser.parse_args()
    if not os.path.exists(args.path):
        raise FileNotFoundError(f"The path {args.path} doesn't exist")
    check_dir(args.path)

    links = {os.path.relpath(x, args.path): [os.path.relpath(y, args.path) for y in links[x]] for x in links}

    nodes = list_concat([links[x] for x in links]) + [x for x in links]
    edges = list_concat([[(x, y) for y in links[x]] for x in links])

    matplotlib.pyplot.figure(figsize=(100, 100))

    graph = networkx.Graph()
    graph.add_nodes_from(nodes)
    graph.add_edges_from(edges)
    networkx.draw_shell(graph, with_labels=True)
    matplotlib.pyplot.show()
