"""IR System."""
from Parser.parser import parse

if __name__ == "__main__":

    # contains Bruto
    # ans = Sentence("Bruto").search()
    # pprint(parse("Bruto"))
    # pprint(parse("contains Bruto"))
    # pprint(parse("has contains Bruto"))
    # pprint(parse("just Bruto"))

    # # Bruto AND NOT Cesar
    # # ans = And("Bruto", Not("Cesar")).search()
    print(parse("batalla or merry and bárbol or algo"))

    # # Brutus AND Calpurnia AND Caesar
    # # ans = And("Brutus", "Calpurnia", "Caesar").search()
    # print(parse("Brutus AND Calpurnia AND Caesar"))
    #
    # # Bruto AND Cesar AND NOT Calpurnia
    # # ans = And("Brutus", "Caesar", Not("Calpurnia")).search()
    # print(parse("Brutus OR Caesar but not Calpurnia"))
    # print(parse("Brutus and Caesar and not Calpurnia"))
    # print(parse("Brutus and Caesar but not Calpurnia"))
