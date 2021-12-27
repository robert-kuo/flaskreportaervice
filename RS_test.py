import Opt_RS_Func
import Opt_func
import os

mainpath = '/aidata/DIPS'

def RS_Evaluate(taskname):
    s, ret = Opt_RS_Func.ExtractData(mainpath, taskname)
    if ret == 200:
        maxline_count = 4
        sfile, ret = Opt_RS_Func.Evaluation(mainpath, taskname, maxline_count)
        if ret == 201 or ret == 205:
            ret1 = Opt_func.TaskConfig_SaveFileAttrib(mainpath, taskname, os.path.basename(sfile), 'Evaluation', '')
            if ret1 > 205: ret = ret1
    return '', ret

s, ret = RS_Evaluate('Task1')

print(s, ret)