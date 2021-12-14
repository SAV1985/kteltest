import re

'''Проверка на соответствие шаблону'''

def mask_check(mask, sn):
    try:
        X = '[0-9A-Z]'
        N = '[0-9]'
        a = '[a-z]'
        A = '[A-Z]'
        Z = r'[_,-,@]'
        ind = 0
        if len(mask) != len(sn):
            return (False, 'Серийный номер \"{}\" не совпадает с шаблоном по количесту символов '.format(sn))
        for i in sn:
            if mask[ind] == 'X' and re.match(X, i):
                ind += 1
                continue
            elif mask[ind] == 'a' and re.match(a, i):
                ind += 1
                continue
            elif mask[ind] == 'N' and re.match(N, i):
                ind += 1
                continue
            elif mask[ind] == 'A' and re.match(A, i):
                ind += 1
                continue
            elif mask[ind] == 'Z' and re.match(Z, i):
                ind += 1
                continue
            else:
                return (False, 'Ошибка проверки, серийный номер \"{}\" не совпадает с шаблоном {}'.format(sn, mask))

        return (True, sn)
    except Exception as err:
        print(err)

