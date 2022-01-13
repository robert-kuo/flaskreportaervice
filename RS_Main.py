from flask import Flask
from flask import abort  #, session

import os  #, datetime as dt
import Opt_func
import Opt_RS_Func

myapp = Flask(__name__)
if os.name == 'nt':
    mainpath = 'd:\\opt_web'
    ip = Opt_func.GetIP()
else:
    mainpath = '/aidata/DIPS'
    ip = ''

# @myapp.before_request
# def make_session_permanent():
#     session.permanent = True
#     myapp.permanent_session_lifetime = dt.timedelta(minutes=3)

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

@myapp.route('/RS/v0.1/<string:taskname>/<string:stagename>/<string:resultname>',  methods = ['GET'])
def RS_Download_PSRReport(taskname, stagename, resultname):
    sfile = resultname + '.xlsx'
    spath = os.path.join(os.path.join(mainpath, taskname), stagename)
    if not os.path.isfile(os.path.join(spath,  sfile)): abort(404)
    result = Opt_func.Download_EXCELFile(spath, sfile)
    return result