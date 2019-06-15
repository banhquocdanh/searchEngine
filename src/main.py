
from utilitiesFunction import getLineFromFile
from reverseIndexSearch import ReverseIndex


if __name__ == '__main__':
    querys = getLineFromFile('../sanbox/100_query.txt')
    reverseIndexSearch = ReverseIndex()
    File_object = open('./output.txt', 'w', encoding="utf-8")
    for query in querys:
        result = reverseIndexSearch.search(query)
        File_object.write("{}: {} \n\n".format(query, result))
    File_object.close()