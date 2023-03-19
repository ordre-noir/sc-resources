#!/usr/bin/python
import csv
import getopt
import json
import shutil
import sys
from enum import Enum
from pathlib import Path

grid_radius = {
    "aberdeen": 548000,
    "arial": 689000,
    "arccorp": 1900000,
    "calliope": 480666,
    "cellin": 520666,
    "clio": 674334,
    "crusader": 15000000,
    "daymar": 590000,
    "euterpe": 425666,
    "hurston": 2000000,
    "ita": 650000,
    "lyria": 446000,
    "magda": 681666,
    "microtech": 2300000,
    "wala": 566300,
    "yela": 1016000,
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
        opts, args = getopt.getopt(argv, "hi:", ["ifile="])
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
            additional_properties = json.loads(system["AdditionalProperties"])
            results.append({"AdditionalProperties": additional_properties})

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
                                 grid_radius[entry["Key"]] if entry["Key"] in grid_radius else None])

    shutil.move(game_data_file, Path(__file__).parent.joinpath("nargit", inputfile))


if __name__ == '__main__':
    main(sys.argv[1:])
