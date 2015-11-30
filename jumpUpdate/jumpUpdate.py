import os
import re
import pCfg

indexP = pCfg.indexP
jumpP = pCfg.jumpP

cmdStr = 'svn revert ' + indexP + '\index.jsp'
os.system(cmdStr)
cmdStr = 'svn update ' + indexP + '\index.jsp'
os.system(cmdStr)

versionStr = ''
loaderName = ''
content = ''
with open(indexP + '\index.jsp', 'r', encoding='utf-8') as tpF:
    content = tpF.read()
    versionStr = re.search(',version:"(.*?)"', content).group(1)
    loaderName = re.search('"<%=flashAddress%>/(.*?).swf"', content).group(1)

cmdStr = 'svn revert ' + jumpP + '\jump.jsp'
os.system(cmdStr)
cmdStr = 'svn update ' + jumpP + '\jump.jsp'
os.system(cmdStr)
replaceContent = ''
with open(jumpP + '\jump.jsp', 'r', encoding='utf-8') as tpF:
    content = tpF.read()
    replaceContent = re.sub('version:"(.*?)"', 'version:"'+versionStr+'"', content)
    replaceContent = re.sub('<%=address%>/(.*?).swf', '<%=address%>/'+loaderName+'.swf', replaceContent)

with open(jumpP + '\jump.jsp', 'w', encoding='utf-8') as tpF:
    tpF.write(replaceContent)

os.system('TortoiseProc.exe /command:commit /path:"'+jumpP+'" /logmsg:"lalal"')
