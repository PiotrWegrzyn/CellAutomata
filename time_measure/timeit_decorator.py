import time


def timeit(method):
    def timed(*args, **kw):
        ts = time.time()
        result = method(*args, **kw)
        if True:
            watched_functions = {"update_energy_in_row", "draw_data_frame"}
            te = time.time()
            if 'log_time' in kw:
                name = kw.get('log_name', method.__name__.upper())
                kw['log_time'][name] = int((te - ts) * 1000)
            else:
                delta = te - ts
                if delta*1000>20 and method.__name__ in watched_functions:
                    print('%r  %2.2f ms' % (method.__name__.upper(), delta * 1000))#, args[1]))
                if delta * 1000 > 100:
                    print('%r  %2.2f ms' % (method.__name__.upper(), delta * 1000))
                else:
                    pass
                    # print('%r  %2.2f ms' % (method.__name__, delta * 1000))
        return result

    return timed