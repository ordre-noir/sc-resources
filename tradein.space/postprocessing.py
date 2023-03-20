#!/usr/bin/python
import csv
import getopt
import json
import sys
from enum import Enum
from pathlib import Path

murphys_grid_radius = {
    "aberdeen ": 548 * 1000,
    "arccorp ": 1900 * 1000,
    "arial": 689 * 1000,
    "calliope": 480.666 * 1000,
    "cellin": 520.666 * 1000,
    "clio": 674.334 * 1000,
    "crusader": 14900 * 1000,
    "daymar": 590 * 1000,
    "delamar": 700 * 1000,
    "euterpe": 425.666 * 1000,
    "hurston": 2000 * 1000,
    "ita": 650 * 1000,
    "lyria": 446 * 1000,
    "magda": 681.666 * 1000,
    "microtech": 2300 * 1000,
    "wala": 566.3 * 1000,
    "yela": 1016.6 * 1000,
}


class LocationType(Enum):
    LAGRANGE = 4
    PLANET = 1
    MOON = 2
    STATION = 8
    SHOP_IN_STATION = 10
    COMM_ARRAY = 9
    GROUND_LOCATION = 7
    CITY = 6
    SUN = 0
    OTHER = 11


def main(argv):
    inputfile = ''
    try:
        opts, args = getopt.getopt(argv[1:], "hi:", ["ifile="])
    except getopt.GetoptError:
        print('extraction.py -i <inputfile>')
        sys.exit(2)
    for opt, arg in opts:
        if opt == '-h':
            print('extraction.py -i <inputfile>')
            sys.exit()
        elif opt in ("-i", "--ifile"):
            inputfile = arg

    results = []
    print(inputfile)
    game_data_file = Path(__file__).parent.parent.joinpath(inputfile)
    with open(game_data_file, "r", encoding="utf-8") as f:
        data = json.load(f)
        system_locations = data["SystemLocations"]
        for system in system_locations:
            if system["LocationType"] not in [LocationType.LAGRANGE.value, LocationType.PLANET.value,
                                              LocationType.MOON.value, LocationType.STATION.value,
                                              LocationType.SUN.value]:
                continue
            system["AdditionalProperties"] = json.loads(system["AdditionalProperties"])
            results.append(system)

    if len(results) == 0:
        raise ValueError("No results found")

    with open(Path(__file__).parent.parent.joinpath('nargit/qed-data.csv'), 'w', newline='', encoding='utf-8') as csvfile:
        spamwriter = csv.writer(csvfile, delimiter=',',
                                quotechar='"', quoting=csv.QUOTE_MINIMAL)
        spamwriter.writerow(
            ["Name", "Description", "X", "Y", "Z", "LocationType", "Radius", "OMRadius", "QTDistance",
             "GridRadius"])
        for entry in results:
            properties = entry["AdditionalProperties"]
            spamwriter.writerow([entry["Name"].strip(), entry["Description"],
                                 properties["GlobalPosition"]["X"],
                                 properties["GlobalPosition"]["Y"],
                                 properties["GlobalPosition"]["Z"],
                                 entry["LocationType"],
                                 properties["Radius"] if "Radius" in properties else None,
                                 properties["OMRadius"] if "OMRadius" in properties else None,
                                 entry["QTDistance"],
                                 murphys_grid_radius[entry["Key"]] if entry["Key"] in murphys_grid_radius else None])


if __name__ == '__main__':
    main(sys.argv)
