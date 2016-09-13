# coding: utf-8
import os, argparse, datetime, time, json

jsonfile = 'language-codes-full.json'

appname = 'isolang'
appversion = '1.2.0  13-9-2016'
appdesc = 'Transforms ISO Language Codes JSON file'
appusage = 'Help:  py ' + appname + '.py -h \n'
appauthor = 'Filip Kriz (@filak)'
applicense = 'MIT License (MIT)'

sourcepath = '_download'
targetpath = '_output'
defcodes = 'all'

def main():

    print('\n')
    print('********************************************')
    print('*  ', appname, appversion)
    print('********************************************')
    print('*  ', appdesc)
    print('*  ', appusage)
    print('*   Author:   ', appauthor)
    print('*   License:  ', applicense)
    print('********************************************\n')

    parser = argparse.ArgumentParser(description=appdesc, prog=appname, usage='%(prog)s [options]')
    parser.add_argument('-f','--jsonfile', type=str, default=jsonfile,
                            help='JSON File name - default: '+jsonfile)
    parser.add_argument('-c','--codes', type=str, default=defcodes,
                            help='Comma separated 3-letter codes - default: '+defcodes)
    parser.add_argument('-s','--sourcedir', type=str, default=sourcepath,
                            help='Source dir path - full or relative to app dir - default: '+sourcepath)
    parser.add_argument('-t','--targetdir', type=str, default=targetpath,
                            help='Target dir path - full or relative to app dir - default: '+targetpath)

    args, unknown = parser.parse_known_args()

    if unknown:
        print('ERROR : Uknown arguments : ', unknown)
        print('Try help : py ' + appname  + '.py -h')
    else:
        spath = os.path.normpath(args.sourcedir)
        sourcefile = os.path.join(spath, args.jsonfile)
        tpath = os.path.normpath(args.targetdir)

        if os.path.isfile(sourcefile) and os.path.isdir(tpath):
            procFile(sourcefile, tpath, args.codes)
        else:
            print('ERROR : Bad path(s) : ', '\n', sourcefile, '\n', tpath)


def procFile(sourcefile, tpath, codes):

    t0 = time.clock()
    startTime = datetime.datetime.strftime(datetime.datetime.now(), '%Y-%m-%d %H:%M:%S')
    print('\nStarted : ', startTime, '\n')
    print('Source file : ', sourcefile)
    print('Target dir  : ', tpath)
    print('Code list   : ', codes)

    if codes == defcodes:
        subset = None
        fname = 'codes_lookup'
    else:
        codes = codes.replace(' ','')
        subset = codes.split(',')
        fname = 'codes_lookup_sub'

    code_dict = {}
    code_dict['codes'] = []
    with open(sourcefile, mode='r', encoding='utf-8') as fh:
        json_data = json.load(fh)

    for o in json_data:
        if subset:
            if o['alpha3-b'] in subset or o['alpha3-t'] in subset:
                if o['alpha2']:
                    code_dict['codes'].append(getCodes(o))
        else:
            if o['alpha2']:
                code_dict['codes'].append(getCodes(o))


    code_dict = getCustomCodes(code_dict)
    writeXml(code_dict, tpath, fname)
    writeJson(code_dict, tpath, fname)

    endTime = datetime.datetime.strftime(datetime.datetime.now(), '%Y-%m-%d %H:%M:%S')
    print('\nFinished : ', startTime, '\n')
    et = ('Elapsed time : ' + str((time.clock() - t0) / 60) + ' min\n')
    print(et)


def writeXml(code_dict, tpath, fname):
    fname += '.xml'
    fpath = os.path.join(tpath, fname)
    print('Output   : ', fpath)

    xml_data = ''
    for o in code_dict['codes']:
        xml_data += getXmlNode(o)

    with open(fpath, mode='w', encoding='utf-8') as ft:
        ft.write('<?xml version="1.0" encoding="UTF-8"?>\n')
        ft.write('<codes>\n')
        ft.write(xml_data)
        ft.write('</codes>')


def getXmlNode(o):
    return '<code a2="'+ o['a2'] +'" a3b="'+ o['a3b'] +'" a3t="'+ o['a3t'] +'" a3h="'+ o['a3h'] +'" lang="'+ o['lang'] +'"/>\n'


def writeJson(code_dict, tpath, fname):
    fname += '.json'
    fpath = os.path.join(tpath, fname)
    print('Output   : ', fpath)

    with open(fpath, mode='w', encoding='utf-8') as ft:
        ft.write(json.dumps(code_dict))


def getCodes(o):
    lang = o['English']
    a2 = o['alpha2']
    a3b = o['alpha3-b']
    a3t = o['alpha3-t']
    a3h = a3t
    if a3h == '':
        a3h = a3b

    node = {}
    node['a2'] = a2
    node['a3b'] = a3b
    node['a3t'] = a3t
    node['a3h'] = a3h
    node['lang'] = lang

    return node


def getCustomCodes(code_dict):

    node = {}
    node['a2'] = ''
    node['a3b'] = 'und'
    node['a3t'] = ''
    node['a3h'] = 'und'
    node['lang'] = 'Undetermined'

    code_dict['codes'].append(node)

    node = {}
    node['a2'] = 'de'
    node['a3b'] = 'ger_frak'
    node['a3t'] = 'deu'
    node['a3h'] = 'deu_frak'
    node['lang'] = 'German fracture'

    code_dict['codes'].append(node)

    node = {}
    node['a2'] = 'da'
    node['a3b'] = 'dan_frak'
    node['a3t'] = 'dan'
    node['a3h'] = 'dan_frak'
    node['lang'] = 'Danish fracture'

    code_dict['codes'].append(node)


    node = {}
    node['a2'] = 'sk'
    node['a3b'] = 'slo_frak'
    node['a3t'] = 'slk'
    node['a3h'] = 'slk_frak'
    node['lang'] = 'Slovak fracture'

    code_dict['codes'].append(node)

    return code_dict



if __name__ == '__main__':
    main()
