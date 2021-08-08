import itertools
import copy

def compile(seq1, seq2, score_dic, method):
    score_matrix = [[0 for column in range(len(seq1))]
                    for row in range(len(seq2))]
    trace_back = [[[]for column in range(len(seq1))]
                  for row in range(len(seq2))]
# 打分矩阵
# 回溯路径
    if method != 3:
        for i in range(len(score_matrix[0])):
            score_matrix[0][i] = score_dic['gap']+(i-1)*score_dic['extgap']
            if i > 0:
                trace_back[0][i].append('left')
        for i in range(len(score_matrix)):
            score_matrix[i][0] = score_dic['gap']+(i-1)*score_dic['extgap']
            if i > 0:
                trace_back[i][0].append('up')
    else:
        for i in range(2, len(score_matrix[0])):
            trace_back[0][i].append('left')
        for i in range(2, len(score_matrix)):
            trace_back[i][0].append('up')
    trace_back[0][0].append('done')
# 基本框架

    for i in range(1, len(score_matrix)):
        for j in range(1, len(score_matrix[0])):
            if seq1[j] == seq2[i]:
                char_score = score_dic['match']
            else:
                char_score = score_dic['mismatch']

            if 'up' in trace_back[i-1][j]:
                top_score = score_matrix[i - 1][j] + score_dic['extgap']
            else:
                top_score = score_matrix[i - 1][j] + score_dic['gap']

            if 'left' in trace_back[i][j-1]:
                left_score = score_matrix[i][j - 1] + score_dic['extgap']
            else:
                left_score = score_matrix[i][j - 1] + score_dic['gap']

            diag_score = score_matrix[i - 1][j - 1] + char_score
            score = max(top_score, left_score, diag_score)
            score_matrix[i][j] = score
            # 计算最大值
            if top_score == score:
                trace_back[i][j].append('up')
            if left_score == score:
                trace_back[i][j].append('left')
            if diag_score == score:
                trace_back[i][j].append('diag')
            # 反馈至路径
            if method == 3:
                if score_matrix[i][j] < 0:
                    score_matrix[i][j] = 0
            if method == 2:
                scup = score
                sclef = score
                up = i
                lef = j
                bl = 0
                for m in range(0, i):
                    sc = (i-m-1)*score_dic['extgap'] + \
                        score_dic['gap']+score_matrix[m][j]
                    if sc >= scup:
                        scup = sc
                        bl = 1
                for m in range(0, j):
                    sc = (j-m-1)*score_dic['extgap'] + \
                        score_dic['gap']+score_matrix[i][m]
                    if sc >= sclef:
                        sclef = sc
                        bl = 1
                if bl == 1:
                    if scup > sclef:
                        score_matrix[i][j] = scup
                        if scup == score:
                            for n in range(up, i+1):
                                trace_back[up][j].append('up')
                        elif scup > score:
                            for n in range(up, i+1):
                                trace_back[up][j] = 'up'
                    elif scup < sclef:
                        score_matrix[i][j] = sclef
                        if sclef == score:
                            for n in range(lef, j+1):
                                trace_back[i][lef].append('left')
                        elif sclef > score:
                            for n in range(lef, j+1):
                                trace_back[i][lef] = 'left'
    # 计算矩阵

    # 根据结果计算最优匹配的序列
    # pointer = [seq2_index, seq1_index]
    pointer = [len(score_matrix) - 1, len(score_matrix[0]) - 1]
    align_seq1 = []
    align_seq2 = []
    arrow = trace_back[pointer[0]][pointer[1]]

    def seq_letter_finder(current_arrow, current_pointer):
        if current_arrow == 'diag':
            letter = [seq1[current_pointer[1]], seq2[current_pointer[0]]]
            next_pointer = [current_pointer[0] - 1, current_pointer[1] - 1]
            next_arrow = trace_back[next_pointer[0]][next_pointer[1]]
            return letter, next_arrow, next_pointer
        elif current_arrow == 'left':
            letter = [seq1[current_pointer[1]], '-']
            next_pointer = [current_pointer[0], current_pointer[1] - 1]
            next_arrow = trace_back[next_pointer[0]][next_pointer[1]]
            return letter, next_arrow, next_pointer
        else:
            letter = ['-', seq2[current_pointer[0]]]
            next_pointer = [current_pointer[0] - 1, current_pointer[1]]
            next_arrow = trace_back[next_pointer[0]][next_pointer[1]]
            return letter, next_arrow, next_pointer

    def align_seq_finder(rec_arrow, rec_pointer, rec_ls):
        if rec_arrow[0] == 'done':
            rec_ls = [rec_ls[0][::-1], rec_ls[1][::-1]]
            return rec_ls
        else:
            if len(rec_arrow) == 1:
                letter, rec_arrow, rec_pointer = seq_letter_finder(
                    rec_arrow[0], rec_pointer)
                rec_ls[0] += letter[0]
                rec_ls[1] += letter[1]
                return align_seq_finder(rec_arrow, rec_pointer, rec_ls)

            elif len(rec_arrow) == 2:
                arrow1 = copy.deepcopy(rec_arrow[0])
                pointer1 = copy.deepcopy(rec_pointer)
                ls1 = copy.deepcopy(rec_ls)
                arrow2 = copy.deepcopy(rec_arrow[1])
                pointer2 = copy.deepcopy(rec_pointer)
                ls2 = copy.deepcopy(rec_ls)
                letter1, arrow1, pointer1 = seq_letter_finder(arrow1, pointer1)
                letter2, arrow2, pointer2 = seq_letter_finder(arrow2, pointer2)
                ls1[0] += letter1[0]
                ls1[1] += letter1[1]
                ls2[0] += letter2[0]
                ls2[1] += letter2[1]
                return list(itertools.chain(align_seq_finder(arrow1, pointer1, ls1),
                                            align_seq_finder(arrow2, pointer2, ls2)))
            else:
                arrow1 = copy.deepcopy(rec_arrow[0])
                pointer1 = copy.deepcopy(rec_pointer)
                pointer2 = copy.deepcopy(rec_pointer)
                pointer3 = copy.deepcopy(rec_pointer)
                ls1 = copy.deepcopy(rec_ls)
                ls2 = copy.deepcopy(rec_ls)
                ls3 = copy.deepcopy(rec_ls)
                letter, arrow1, pointer1 = seq_letter_finder(arrow1, pointer1)
                ls1[0] += letter[0]
                ls1[1] += letter[1]
                arrow2 = rec_arrow[1]
                letter, arrow2, pointer2 = seq_letter_finder(arrow2, pointer2)
                ls2[0] += letter[0]
                ls2[1] += letter[1]
                arrow3 = rec_arrow[2]
                letter, arrow3, pointer3 = seq_letter_finder(arrow3, pointer3)
                ls3[0] += letter[0]
                ls3[1] += letter[1]
                return list(itertools.chain(align_seq_finder(arrow1, pointer1, ls1),
                                            align_seq_finder(
                                                arrow2, pointer2, ls2),
                                            align_seq_finder(arrow3, pointer3, ls3)))
    return align_seq_finder(arrow, pointer, ['', ''])

