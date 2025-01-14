"""Compare neighbours from catwalk vs. findneighbour3, a 
   python based server implementing reference based compression and
   SNV computation https://github.com/davidhwyllie/findNeighbour3 
   """

import collections
import json
import argh
import requests


def cw_all_guids(cw_host, cw_port):
    """Get all samples names, which are usually uuids, or guids as they call them here."""
    xs = requests.get(f"http://{cw_host}:{cw_port}/list_samples").json()
    return xs


def cw_neighbours(cw_host, cw_port, guid, max_distance):
    """Get catwalk neighbours for guid at distance."""
    xs = requests.get(
        f"http://{cw_host}:{cw_port}/neighbours/{guid}/{max_distance}"
    ).json()
    return [[g, int(d)] for [g, d] in xs]


def cwn(max_distance, cw_host="localhost", cw_port=5000):
    """Print neighbours for all samples from catwalk."""
    out = dict()
    for guid in cw_all_guids(cw_host, cw_port):
        out[guid] = cw_neighbours(cw_host, cw_port, guid, max_distance)
    print(json.dumps(out))


def fn3_all_guids(fn3_host, fn3_port):
    """Get all findneighbour3 guids."""
    return requests.get(f"http://{fn3_host}:{fn3_port}/api/v2/guids").json()


def fn3_neighbours(fn3_host, fn3_port, guid, max_distance):
    """Get findneighbour3 neighbours for guid at distance."""
    xs = requests.get(
        f"http://{fn3_host}:{fn3_port}/api/v2/{guid}/neighbours_within/{max_distance}"
    ).json()
    return [[g, int(d)] for [g, d] in xs]


def fn3n(fn3_host, fn3_port):
    """Print neighbours for all samples from fn3"""
    out = dict()
    for guid in fn3_all_guids(fn3_host, fn3_port):
        out[guid] = fn3_neighbours(fn3_host, fn3_port, guid)
    print(json.dumps(out))


def compare(f1, f2):
    """compare neighbours from two files (saved from fn3n or cwn) for equality."""
    ns1 = json.loads(open(f1).read())
    ns2 = json.loads(open(f2).read())

    for n in ns1.keys():
        if n not in ns2.keys():
            print(f"Error: sample {n} from {f1} missing from {f2}")
            return
    for n in ns2.keys():
        if n not in ns1.keys():
            print(f"Error: sample {n} from {f2} missing from {f1}")
            return

    sns1 = collections.defaultdict(set)
    for k, n in ns1.items():
        for ne in n:
            sns1[k].add((ne[0], ne[1]))

    sns2 = collections.defaultdict(set)
    for k, n in ns2.items():
        for ne in n:
            sns2[k].add((ne[0], ne[1]))

    for k in ns1.keys():
        diff = sns2[k].symmetric_difference(sns1[k])
        if diff:
            print(k, diff)


def main():
    """Main function."""
    parser = argh.ArghParser()
    parser.add_commands([cwn, fn3n, compare])
    parser.dispatch()


if __name__ == "__main__":
    main()
