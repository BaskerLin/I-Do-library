#coding=cp936
#coding=utf-8
import maya.cmds as cmds
import maya.mel as mm 
import sys
import os
import mtoa.aovs as aovs
import time
import socket                
def pySource(filePath):
    myFile = os.path.basename(filePath)
    dir = os.path.dirname(filePath)
    fileName = os.path.splitext(myFile)[0]
    if( os.path.exists( dir ) ):
        paths = sys.path
        pathfound = 0
        for path in paths:
            if(dir == path):
                pathfound = 1
            if not pathfound:
                sys.path.append( dir )
        exec('import ' +fileName) in globals()
        exec( 'reload( ' + fileName + ' )' ) in globals()
    return

def addfile(arg):
    path = cmds.textField('pathcmm',q=True,tx=True)
    filelist = cmds.getFileList(fld=path,filespec='*.mb')
    cmds.textScrollList("srcObjList",e=1,ra=1,a=filelist)
def openfile(arg):
    Vervalue= cmds.checkBox("batpychange" ,q=True,v=True)
    paths = cmds.textField('pathcmm',q=True,tx=True)
    pypaths = cmds.textField('pycmm',q=True,tx=True)
    path =paths.replace("\\","/")
    selit = cmds.textScrollList("srcObjList",q=1,si=1)   
    if selit ==None:
        print "·�����޿����ļ� \n",
    else:
        fullpath = path+"/"+selit[0]
        if Vervalue==False:
            cmds.deleteUI('fileBridge',wnd=True)
            cmds.file(fullpath,ignoreVersion=1, typ="mayaBinary", options="v=0;", o=1, f=1)
            if os.path.exists(paths+"/"+pypaths+u".py")==True:
                pySource(paths+pypaths+u".py")
        else:
            if os.path.exists(paths+pypaths+u".py")==True:
                pySource(paths+"/"+pypaths+u".py")
            cmds.deleteUI('fileBridge',wnd=True)
            cmds.file(fullpath,ignoreVersion=1, typ="mayaBinary", options="v=0;", o=1, f=1)
      
def reffile(arg):
#    moVervalue= cmds.checkBox("mover" ,q=True,v=True)
    refVervalue= cmds.checkBox("refshift" ,q=True,v=True)
    paths = cmds.textField('pathcmm',q=True,tx=True)
    path =paths.replace("\\","/")
    selit = cmds.textScrollList("srcObjList",q=1,si=1)
    if selit ==None:
        print "·�����޿����ļ� \n",
    else:
        fullpath = path+"/"+selit[0]
        refname =os.path.splitext(selit[0])[0]
        dirname = path.split("/")[-1]
        cmds.deleteUI('fileBridge',wnd=True)
        if refVervalue==True:
            refername =refname+"__"+dirname+"__Ref"
        else:
            refername =refname
        cmds.file(fullpath,ignoreVersion=1, type="mayaBinary", namespace=refername, r=1, gl=1, mergeNamespacesOnClash=False, options="v=0;")
def importfile(arg):
    paths = cmds.textField('pathcmm',q=True,tx=True)
    path =paths.replace("\\","/")
    selit = cmds.textScrollList("srcObjList",q=1,si=1)
    if selit ==None:
        print "·�����޿����ļ� \n",
    else:
        fullpath = path+"/"+selit[0]
        impname =os.path.splitext(selit[0])[0]
        dirname = path.split("/")[-1]
        cmds.deleteUI('fileBridge',wnd=True)
        importname = impname+"__"+dirname+"__Imp"
        cmds.file(fullpath,pr=1, ignoreVersion=1, i=1, type="mayaBinary", ra=True, mergeNamespacesOnClash=False, options="v=0;",namespace=importname)
def setquick(arg):
    keyadj = cmds.hotkey( '1', query=True, ctl=True )
    if keyadj ==False:
        cmds.nameCommand( 'filebridgemanager', annotation='filebridgemanager',command='source"O:/mocap/SJ_ToolBox/mel_source/filebridge.mel"')
        cmds.hotkey(k='1',ctl=1,name='filebridgemanager')  
    else:
        print "�Ѿ����úÿ�ݼ�����\n",
def save(arg):
    path = cmds.file(q=1,expandName=1)
    dir =  os.path.dirname(path)
    myfile =os.path.basename(path)
    filetype =os.path.splitext(myfile)[-1]
    filename =myfile[0:(len(myfile)-len(filetype))]
    bakpath = dir+u"/bak"
    timename = time.strftime('_%m%d_(%Hh)',time.localtime(time.time()))
    timeinfo = time.strftime('20%y/%m/%d_%H:%M',time.localtime(time.time()))
    hostname = socket.gethostname()
    updateinfo =cmds.textField('updateInfo',tx=1,q=1)
    updateinfoEn =updateinfo.encode("gb2312")
    bakfinal = dir+"/bak/"+filename+timename+filetype
    if os.path.exists(bakpath)==True:
        if os.path.exists(dir+u"/����˵��.txt")==True:
            #�и���˵����
            wrtxt = open(dir+u"/����˵��.txt","a")
            wrtxt.write("||||"+timeinfo+"("+hostname+"):"+updateinfoEn+";    \n")
            wrtxt.close
            cmds.sysFile(path ,copy=bakfinal )
            cmds.file(s=1,f=1)
        else:
            #û�и���˵����
            wrtxt = open(dir+u"/����˵��.txt","w")
            wrtxt.write("||||"+timeinfo+"("+hostname+"):"+updateinfoEn+";    \n")
            wrtxt.close
            cmds.sysFile(path ,copy=bakfinal )
            cmds.file(s=1,f=1)
    else:
        if os.path.exists(dir+u"/����˵��.txt")==True:
            #�и���˵����
            wrtxt = open(dir+u"/����˵��.txt","a")
            wrtxt.write("||||"+timeinfo+"("+hostname+"):"+updateinfoEn+";    \n")
            wrtxt.close
            cmds.sysFile(bakpath,makeDir=1)
            cmds.sysFile(path ,copy=bakfinal )
            cmds.file(s=1,f=1)
        else:
            #û�и���˵����
            wrtxt = open(dir+u"/����˵��.txt","w")
            wrtxt.write("||||"+timeinfo+"("+hostname+"):"+updateinfoEn+";    \n")
            wrtxt.close
            cmds.sysFile(bakpath,makeDir=1)
            cmds.sysFile(path ,copy=bakfinal )
            cmds.file(s=1,f=1)
    
def saveas(arg):
    paths = cmds.textField('pathcmm',q=True,tx=True).replace("\\","/")
    oldpath = cmds.file(q=1,expandName=1).replace("\\","/")
    timename = time.strftime('_%m%d_(%Hh)',time.localtime(time.time()))
    timeinfo = time.strftime('20%y/%m/%d_%H:%M',time.localtime(time.time()))
    updateinfo =cmds.textField('updateInfo',tx=1,q=1)
    updateinfoEn =updateinfo.encode("gb2312")
    hostname = socket.gethostname()
    olddir =  os.path.dirname(oldpath)
    oldmyfile =os.path.basename(oldpath)
    oldfiletype =os.path.splitext(oldmyfile)[-1]
    oldfilename =oldmyfile[0:(len(oldmyfile)-len(oldfiletype))]
    newpath = paths+"/"+oldmyfile
    bakpath = paths+"/bak/"+oldfilename+timename+oldfiletype
    if os.path.exists(newpath)==False:
        cmds.sysFile(oldpath ,copy=newpath)
        print oldpath,newpath
        wrtxt = open(paths+u"/����˵��.txt","a")
        wrtxt.write("||||"+timeinfo+"("+hostname+"):"+updateinfoEn+";    \n")
        wrtxt.close
    else:
        bakpath = paths+"/bak"
        if os.path.exists(bakpath)==False:
            cmds.sysFile(bakpath,makeDir=1)
            cmds.sysFile(newpath ,copy=bakpath+"/"+oldfilename+timename+oldfiletype)
            cmds.sysFile(oldpath ,copy=newpath)
            wrtxt = open(paths+u"/����˵��.txt","a")
            wrtxt.write("||||"+timeinfo+"("+hostname+"):"+updateinfoEn+";    \n")
            wrtxt.close
        else:
            cmds.sysFile(newpath ,copy=bakpath+"/"+oldfilename+timename+oldfiletype)
            cmds.sysFile(oldpath ,copy=newpath)
            wrtxt = open(paths+u"/����˵��.txt","a")
            wrtxt.write("||||"+timeinfo+"("+hostname+"):"+updateinfoEn+";    \n")
            wrtxt.close

if cmds.window('fileBridge',ex=True):
    cmds.deleteUI('fileBridge',wnd=True)
cmds.window('fileBridge',t='FileBridgeV5.0')
cmds.columnLayout(adj=True)
cmds.textScrollList("srcObjList",allowMultiSelection=1)
cmds.text(l='',fn='fixedWidthFont',h=30,annotation="�����ļ���·������ȡ�ļ����б�Ȼ��ִ�д򿪣������ο��ļ������� \n �����o�̻�ȡ�ļ��������⣩")
cmds.button(l='���ÿ�ݼ�',c =setquick,h=20,ann="���ÿ�ݼ���ctrl+1")

cmds.text(l='�ļ���·��',fn='fixedWidthFont',h=30,annotation="")
cmds.textField('pathcmm',tx="O:\projectname\scenes\hi",h=30,ann="�����ļ���·��")

cmds.text(l='Ԥ����ű�����',fn='fixedWidthFont',h=30,annotation="")
cmds.flowLayout( columnSpacing=0)
cmds.checkBox("batpychange" ,label='�л�ΪԤ����ű�',ann="Ĭ��Ϊ�����ļ���ִ�нű�",w=150)
cmds.checkBox("refshift" ,label='�ο��ļ�ģʽ',v=1,ann="����ģʽ����ɫ��+�汾���ͣ��ļ�������\n��װģʽ����ɫ��")
cmds.setParent( '..' )
cmds.textField('pycmm',tx=u"pyname",h=30,ann="����ű�����")
cmds.button(l='��ȡ�ļ��б�',c =addfile,h=50)
cmds.setParent( '..' )
cmds.flowLayout( columnSpacing=0)
cmds.button(l='���ļ�',c =openfile,h=50,w=85)
cmds.button(l='����ģ��',c =importfile,h=50,w=85)
cmds.button(l='�ο�ģ��',c =reffile,h=50,w=85)
cmds.setParent( '..' )
cmds.text(l='����˵�� ',fn='fixedWidthFont',h=30,w=10)
cmds.textField('updateInfo',tx="",h=30)
#cmds.flowLayout( columnSpacing=0)
#cmds.checkBox("mover" ,label='ģ��',ann="",w=50)
#cmds.checkBox("setver" ,label='����',ann="",w=50)
#cmds.checkBox("anver" ,label='����',v=1,ann="",w=130)
#cmds.checkBox("fxver" ,label='��Ч',ann="",w=50)
#cmds.checkBox("comver" ,label='��װ',ann="",w=130)
#cmds.setParent( '..' )
cmds.flowLayout( columnSpacing=0)

cmds.button(l='���沢����˵��',c =save,h=50,w=127.5)
cmds.button(l='��沢����˵��',c =saveas,h=50,w=127.5)
cmds.setParent( '..' )
cmds.button(l='���ٹر�maya',c ="pySource( 'O:/mocap/SJ_ToolBox/python_source_2015/maya2015quickquit.pyc')",h=50)

cmds.showWindow()