# coding: utf-8
import os
import subprocess

import sublime
import sublime_plugin


class UwscHelpCommand(sublime_plugin.TextCommand):
    def run(self, edit):
        point = self.view.sel()[0].begin()
        if self.view.scope_name(point).find('source.uwsc') == -1:
            return
        word_on_point = self.view.word(point)
        word = self.view.substr(word_on_point)

        def output(text):
            window = self.view.window()
            output_view = window.get_output_panel("textarea")
            window.run_command("show_panel", {"panel": "output.textarea"})
            output_view.set_read_only(False)
            if int(sublime.version()) < 3000:
                _edit = output_view.begin_edit()
                output_view.insert(_edit, output_view.size(), text)
                output_view.end_edit(_edit)
            else:
                output_view.insert(edit, output_view.size(), text)
            output_view.set_read_only(True)

        help_path = os.path.join(self.view.settings().get('uwsc_path'), 'uwsc.chm')
        if not os.path.exists(help_path):
            err = u'{0} が開けませんでした\nuwsc_pathの設定を確認して下さい'.format(help_path)
            output(err)
            return
        if word.upper() in self.keywords:
            url = self.keywords[word.upper()]
            args = '{0} {1}'.format(help_path, url)
            subprocess.Popen(['hh.exe', args], shell=False)
        else:
            reason = u'UwscHelp: {0} が見つかりませんでした'.format(word)
            output(reason)

    # For UWSC version 5
    keywords = {
        'ACW': '::/_RESOURCE/function.htm#acw',
        'ASC': '::/_RESOURCE/function.htm#asc',
        'BETWEENSTR': '::/_RESOURCE/function.htm#betweenstr',
        'BREAK': '::/_RESOURCE/syntax.htm#break',
        'BTN': '::/_RESOURCE/function.htm#btn',
        'CALCARRAY': '::/_RESOURCE/function.htm#calcarray',
        'CALL': '::/_RESOURCE/syntax.htm#call',
        'CHGMOJ': '::/_RESOURCE/function.htm#chgmoj',
        'CHKBTN': '::/_RESOURCE/function.htm#chkbtn',
        'CHKIMG': '::/_RESOURCE/function.htm#chkimg',
        'CHKNUM': '::/_RESOURCE/function.htm#chknum',
        'CHR': '::/_RESOURCE/function.htm#chr',
        'CLASS': '::/_RESOURCE/syntax.htm#class',
        'CLKITEM': '::/_RESOURCE/function.htm#clkitem',
        'COM_ERR_IGN': '::/_RESOURCE/function.htm#com_err_ign',
        'COMMENT': '::/_RESOURCE/syntax.htm#comment',
        'CONSTANT': '::/_RESOURCE/syntax.htm#constant',
        'CONSTDEF': '::/_RESOURCE/syntax.htm#constdef',
        'CONTINUE': '::/_RESOURCE/syntax.htm#continue',
        'COPY': '::/_RESOURCE/function.htm#copy',
        'CPUUSERATE': '::/_RESOURCE/function.htm#cpuuserate',
        'CREATEFORM': '::/_RESOURCE/function.htm#createform',
        'CREATEOLEOBJ': '::/_RESOURCE/function.htm#createoleobj',
        'CTRLWIN': '::/_RESOURCE/function.htm#ctrlwin',
        'DECODE': '::/_RESOURCE/function.htm#decode',
        'DEF_DLL': '::/_RESOURCE/syntax.htm#def_dll',
        'DELETEFILE': '::/_RESOURCE/function.htm#deletefile',
        'DELETEINI': '::/_RESOURCE/function.htm#deleteini',
        'DICTATE': '::/_RESOURCE/function.htm#dictate',
        'DOSCMD': '::/_RESOURCE/function.htm#doscmd',
        'DROPFILE': '::/_RESOURCE/function.htm#dropfile',
        'ENCODE': '::/_RESOURCE/function.htm#encode',
        'EVAL': '::/_RESOURCE/function.htm#eval',
        'EXCEL': '::/_RESOURCE/function.htm#excel',
        'EXCEPTION': '::/_RESOURCE/syntax.htm#exception',
        'EXEC': '::/_RESOURCE/function.htm#exec',
        'EXIT': '::/_RESOURCE/syntax.htm#exit',
        'FCLOSE': '::/_RESOURCE/function.htm#fclose',
        'FDELLINE': '::/_RESOURCE/function.htm#fdelline',
        'FGET': '::/_RESOURCE/function.htm#fget',
        'FOPEN': '::/_RESOURCE/function.htm#fopen',
        'FORM': '::/_RESOURCE/function.htm#form',
        'FORMAT': '::/_RESOURCE/function.htm#format',
        'FPUT': '::/_RESOURCE/function.htm#fput',
        'FUKIDASI': '::/_RESOURCE/function.htm#fukidasi',
        'FUNCTION': '::/_RESOURCE/syntax.htm#function',
        'GETACTIVEOLEOBJ': '::/_RESOURCE/function.htm#getactiveoleobj',
        'GETALLWIN': '::/_RESOURCE/function.htm#getallwin',
        'GETCTLHND': '::/_RESOURCE/function.htm#getctlhnd',
        'GETDIR': '::/_RESOURCE/function.htm#getdir',
        'GETFORMDATA': '::/_RESOURCE/function.htm#getformdata',
        'GETID': '::/_RESOURCE/function.htm#getid',
        'GETITEM': '::/_RESOURCE/function.htm#getitem',
        'GETKEYSTATE': '::/_RESOURCE/function.htm#getkeystate',
        'GETOLEITEM': '::/_RESOURCE/function.htm#getoleitem',
        'GETSLCTLST': '::/_RESOURCE/function.htm#getslctlst',
        'GETSLIDER': '::/_RESOURCE/function.htm#getslider',
        'GETSTR': '::/_RESOURCE/function.htm#getstr',
        'GETTIME': '::/_RESOURCE/function.htm#gettime',
        'HASHTABLE': '::/_RESOURCE/syntax.htm#hashtable',
        'HEXADECIMAL': '::/_RESOURCE/syntax.htm#hexadecimal',
        'IDTOHND': '::/_RESOURCE/function.htm#idtohnd',
        'IEGETDATA': '::/_RESOURCE/function.htm#iegetdata',
        'IEGETSRC': '::/_RESOURCE/function.htm#iegetsrc',
        'IELINK': '::/_RESOURCE/function.htm#ielink',
        'IEOPERATION': '::/_RESOURCE/function.htm#ieoperation',
        'IESETDATA': '::/_RESOURCE/function.htm#iesetdata',
        'IESETSRC': '::/_RESOURCE/function.htm#iesetsrc',
        'IF': '::/_RESOURCE/syntax.htm#if',
        'IFB': '::/_RESOURCE/syntax.htm#ifb',
        'INIFILE': '::/_RESOURCE/function.htm#inifile',
        'INPUT': '::/_RESOURCE/function.htm#input',
        'ISUNICODE': '::/_RESOURCE/function.htm#isunicode',
        'JOIN': '::/_RESOURCE/function.htm#join',
        'KBD': '::/_RESOURCE/function.htm#kbd',
        'KINDOFOS': '::/_RESOURCE/function.htm#kindofos',
        'LENGTH': '::/_RESOURCE/function.htm#length',
        'LOCKHARD': '::/_RESOURCE/function.htm#lockhard',
        'LOCKHARDEX': '::/_RESOURCE/function.htm#lockhardex',
        'MATHFUNC': '::/_RESOURCE/function.htm#mathfunc',
        'MMV': '::/_RESOURCE/function.htm#mmv',
        'MONITOR': '::/_RESOURCE/function.htm#monitor',
        'MOUSEORG': '::/_RESOURCE/function.htm#mouseorg',
        'MSGBOX': '::/_RESOURCE/function.htm#msgbox',
        'MUSCUR': '::/_RESOURCE/function.htm#muscur',
        'OLEEVENT': '::/_RESOURCE/function.htm#oleevent',
        'OPTION': '::/_RESOURCE/syntax.htm#option',
        'PEEKCOLOR': '::/_RESOURCE/function.htm#peekcolor',
        'POFF': '::/_RESOURCE/function.htm#poff',
        'POPUPMENU': '::/_RESOURCE/function.htm#popupmenu',
        'POS': '::/_RESOURCE/function.htm#pos',
        'POSACC': '::/_RESOURCE/function.htm#posacc',
        'POWERSHELL': '::/_RESOURCE/function.htm#powershell',
        'PRINT': '::/_RESOURCE/syntax.htm#print',
        'PROCEDURE': '::/_RESOURCE/syntax.htm#procedure',
        'QSORT': '::/_RESOURCE/function.htm#qsort',
        'READINI': '::/_RESOURCE/function.htm#readini',
        'RECOSTATE': '::/_RESOURCE/function.htm#recostate',
        'RESIZE': '::/_RESOURCE/function.htm#resize',
        'SAFEARRAY': '::/_RESOURCE/function.htm#safearray',
        'SAVEIMG': '::/_RESOURCE/function.htm#saveimg',
        'SCKEY': '::/_RESOURCE/function.htm#sckey',
        'SENDSTR': '::/_RESOURCE/function.htm#sendstr',
        'SENSOR': '::/_RESOURCE/function.htm#sensor',
        'SETCLEAR': '::/_RESOURCE/function.htm#setclear',
        'SETFORMDATA': '::/_RESOURCE/function.htm#setformdata',
        'SETHOTKEY': '::/_RESOURCE/function.htm#sethotkey',
        'SETSLIDER': '::/_RESOURCE/function.htm#setslider',
        'SHIFTARRAY': '::/_RESOURCE/function.htm#shiftarray',
        'SLCTBOX': '::/_RESOURCE/function.htm#slctbox',
        'SLEEP': '::/_RESOURCE/function.htm#sleep',
        'SLICE': '::/_RESOURCE/function.htm#slice',
        'SOUND': '::/_RESOURCE/function.htm#sound',
        'SPEAK': '::/_RESOURCE/function.htm#speak',
        'SPLIT': '::/_RESOURCE/function.htm#split',
        'STATUS': '::/_RESOURCE/function.htm#status',
        'STOPFORM': '::/_RESOURCE/function.htm#stopform',
        'STRCONV': '::/_RESOURCE/function.htm#strconv',
        'STRINGS': '::/_RESOURCE/syntax.htm#strings',
        'TEXTBLOCK': '::/_RESOURCE/syntax.htm#textblock',
        'THREAD': '::/_RESOURCE/syntax.htm#thread',
        'TOKEN': '::/_RESOURCE/function.htm#token',
        'TRIM': '::/_RESOURCE/function.htm#trim',
        'VAL': '::/_RESOURCE/function.htm#val',
        'VARIABLE': '::/_RESOURCE/syntax.htm#variable',
        'VARTYPE': '::/_RESOURCE/function.htm#vartype',
        'VOICERECOGNITION': '::/_RESOURCE/function.htm#voicerecognition',
        'WITH': '::/_RESOURCE/syntax.htm#with',
        'WRITEINI': '::/_RESOURCE/function.htm#writeini',
        'XLACTIVATE': '::/_RESOURCE/function.htm#xlactivate',
        'XLCLOSE': '::/_RESOURCE/function.htm#xlclose',
        'XLGETDATA': '::/_RESOURCE/function.htm#xlgetdata',
        'XLOPEN': '::/_RESOURCE/function.htm#xlopen',
        'XLSETDATA': '::/_RESOURCE/function.htm#xlsetdata',
        'XLSHEET': '::/_RESOURCE/function.htm#xlsheet',
    }
