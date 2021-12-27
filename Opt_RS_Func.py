import os
import warnings, json
import pandas as pd
import Opt_func

def Evaluation(mainpath, taskname, maxline_count):
    warnings.filterwarnings("ignore")
    ret, demand_start, demand_end, begin_day, end_day, df_orders, df_products, df_lines, df_molds, df_orderdata = Opt_func.LoadData_FromDataset(mainpath, taskname)
    lst_onstock_prodcode, lst_onstock_qty, df_orders = Opt_func.Orders_On_Stock(df_products, df_orders)
    df_orders = Opt_func.Orders_Overdue(df_lines, df_orders)
    sfile, ret = Opt_func.Evaluation_Report(mainpath, taskname, demand_start, demand_end, end_day, maxline_count, lst_onstock_prodcode, lst_onstock_qty, df_orders, df_lines, df_molds)
    if not os.path.isfile(sfile): ret = 404
    return sfile, ret

def Evaluate(mainpath, taskname):
    fn = open(os.path.join(os.path.join(mainpath, taskname), 'TaskConfig.json'), 'r')
    json_data = json.load(fn)
    fn.close()
    lst_file = [] if 'Files' not in json_data else json_data['Files']
    cfile = ''
    sfile = ''
    for x in lst_file:
        if x['Attribute'] == 'Calendar':
            cfile = os.path.join(os.path.join(mainpath, taskname), x['FileName'])
            if not os.path.isfile(cfile): cfile = ''
        elif  x['Attribute'] == 'Setting':
            sfile = os.path.join(os.path.join(mainpath, taskname), x['FileName'])
            if not os.path.isfile(sfile): sfile = ''
        else:
            continue
    return cfile, sfile

def ExtractData(mainpath, taskname):
    cfile, sfile = Evaluate(mainpath, taskname)
    if cfile != '' and sfile != '':
        warnings.filterwarnings('ignore')
        df_productdata, df_linedata, df_molddata, df_orderdata, dm_start, dm_end = Opt_func.Read_OriginData(cfile, sfile)

        # Merge stock data to products
        df_stockdata = Opt_func.readstock(df_orderdata, dm_start)

        #print('read product', df_stockdata.shape[0])
        df_products = Opt_func.readproducts(df_stockdata, df_productdata)
        df_stockdata = Opt_func.updatestock(df_stockdata, df_products)
        df_products = pd.merge(df_products, df_stockdata, how='left', on=['product_code', 'part_no'])
        df_products.fillna(0, inplace=True)

        #print(df_products[ df_products['part_no'] == '9G.02K6S.P5A'])
        #print(df_orderdata[df_orderdata['Product_id'] == 2])

        # Merge products to orderdata
        df_orderdata.drop(columns=[df_orderdata.columns[2]], axis=1, inplace=True)
        df_orderdata = Opt_func.order_droprows(df_orderdata)
        df_orderdata = Opt_func.updateorderdata(df_products, df_orderdata)
        df_orderdata = pd.merge(df_products, df_orderdata, on=['product_code', 'part_no'])

        # Generate df_orders
        df_lines = Opt_func.readlines(df_linedata, df_products)
        df_molds = Opt_func.readmolds(df_lines, df_molddata)
        df_lines = Opt_func.updatelines(df_lines, df_molds, 0)
        begin_day, end_day, df_orders = Opt_func.readorders(df_orderdata, df_products, df_lines, df_molds)
        Opt_func.SaveData_toDataset(mainpath, taskname, dm_start, dm_end, begin_day, end_day, df_orders, df_products, df_lines, df_molds, df_orderdata)
        return 'OK', 200
    else:
        return 'file incorrect.', 404