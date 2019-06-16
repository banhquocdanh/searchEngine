
from utilitiesFunction import getLineFromFile
from reverseIndexSearch import ReverseIndex
from bestMatch25 import BestMatch25
import time

if __name__ == '__main__':
    querys = getLineFromFile('../sanbox/100_query.txt')

    bestMatch25 = BestMatch25()
    File_object = open('./output_BM25_advance_full_document.txt', 'w', encoding="utf-8")
    tik = time.perf_counter()
    for query in querys:
        result = bestMatch25.search(query, -1)  #-1 is get full result
        File_object.write("{}: {}: {} \n\n".format(query, len(result), result))
    tok = time.perf_counter()
    time_result = (tok - tik)
    print('BestMatch time: ', time_result)
    File_object.write("time_report: {}".format(time_result))
    File_object.close()

    reverseIndex = ReverseIndex()
    File_object = open('./output_ReverseIndex_full_document.txt', 'w', encoding="utf-8")
    tik = time.perf_counter()
    for query in querys:
        result = reverseIndex.search(query)
        File_object.write("{}: {}: {} \n\n".format(query, len(result), result))
    tok = time.perf_counter()
    time_result = (tok - tik)
    print('ReverseIndex time: ', time_result)
    File_object.write("time_report: {}".format(time_result))
    File_object.close()
