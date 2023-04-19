import pprint

def PrettyPrint(data, depth: int = 4):
    pp = pprint.PrettyPrinter(depth=depth)
    pp.pprint(data)