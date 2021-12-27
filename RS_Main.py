from flask import Flask
from flask import abort

import os
import Opt_func
import Opt_RS_Func

myapp = Flask(__name__)
if os.name == 'nt':
    mainpath = 'd:\\opt_web'
    ip = Opt_func.GetIP()
else:
    mainpath = '/aidata/DIPS'
    ip = ''


@myapp.route("/")
def hello():
    return 'RS Service...'

@myapp.route('/RS/v0.1/<string:taskname>/Evaluate',  methods = ['GET'])
def RS_Evaluate(taskname):
    s, ret = Opt_RS_Func.ExtractData(mainpath, taskname)
    if ret == 200:
        maxline_count = 4
        sfile, ret = Opt_RS_Func.Evaluation(mainpath, taskname, maxline_count)
        if ret == 201 or ret == 205:
            ret1 = Opt_func.TaskConfig_SaveFileAttrib(mainpath, taskname, os.path.basename(sfile), 'Evaluation', '')
            if ret1 > 205: ret = ret1
    if ret > 205: abort(ret)
    return '', ret