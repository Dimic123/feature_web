import pprint


def PrettyPrint(data, depth: int = 4):
    try:
        pp = pprint.PrettyPrinter(depth=depth)
        pp.pprint(data)
    except:
        print("Can't encode characters")
