####  ���ʴ���
####  ��ѡ�в������� ��ѡĿ������

import maya.cmds as mc

sel=mc.ls(sl=True)
sel_shape=mc.listRelatives(sel[0],ad=True,ni=True,f=True)
mat_data=mc.listConnections(sel_shape,c=True,s=False,type='shadingEngine')

##ֻѡ������ �޳�����
mat=[]
for i in range( 0, len(mat_data), 2):
    mat.append(mat_data[i+1])
mat_use=list(set(mat))  ##�޳��ظ��Ĳ�����

for each in mat_use:
    mc.hyperShade(objects=each)
    sel_mat_face=mc.ls(sl=True)
    
    ##�޳����Ǳ�������� ����������ѡ���棬�п���ѡ���������壩
    mat_face_use=[]  
    for each_face in sel_mat_face:
        if each_face.find(sel[0])!=-1:  ##û���ҵ��ͷ���-1
            mat_face_use.append(each_face)
            
    ##��ΪĿ���������
    mat_face_obj=[]  
    for each_new in mat_face_use:
        mat_face_obj.append( each_new.replace(sel[0],sel[1]) )   

    mc.select( mat_face_obj , r=True )
    mc.hyperShade( assign = each )
     
mc.select(cl=True)