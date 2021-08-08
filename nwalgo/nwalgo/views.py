from django.http.response import HttpResponse, JsonResponse
from django.shortcuts import render
from filter.nw import compile
import json
seq1 = '*TCTGCCTTCCCCCAAAGACCGCACTTCGCTG'
seq2 = '*TCGTCCTTCCGCCTACTTCCCGCCTCGACTG'

# 定义得分矩阵
score_dic = {'match': 5, 'mismatch': -7, 'gap': -5, 'extgap': -1}
method = 1


def index(request):
    context = {}
    context['hello'] = 'Hello World!'
    return render(request, 'index.html', context)


def runoob(request):
    print(request.body)
    data = json.loads(request.body)
    data = data['data']
    ls = compile(data['seq1'], data['seq2'], data['score_dic'], data['method'])
    print(ls)
    return JsonResponse({'ls': ls})
