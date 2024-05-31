1. 下載Python
   https://www.python.org/getit/

2.用vscode開啟create_project_object 資料夾

3.Ctrl + ~ 開啟 cmd

4.安裝 virtualenv 
  執行> pip install virtualenv
  
  P.S.教學網站 https://medium.com/ai-for-k12/python-%E7%9A%84-virtualenv-%E8%99%9B%E6%93%AC%E7%92%B0%E5%A2%83%E5%AE%89%E8%A3%9D%E8%88%87%E4%BD%BF%E7%94%A8-8645f5884aac

5.新增虛擬機資料夾
  執行> virtualenv venv

6.執行> activate
  執行後開頭會顯示(venv) 路徑
  如果執行失敗，請將vscode重開，再Ctrl + ~ 開啟 cmd

7.安裝套件
  執行> py -m pip install -r requirements.txt

8.執行程式
  執行 py main.py
