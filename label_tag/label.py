import tkinter as tk
from tkinter import  ttk
import tkinter.messagebox
import  json
from tkinter.scrolledtext import ScrolledText
import  re
win=tk.Tk()
win.title('high_light')
win.geometry('1300x800')

frametop=tk.Frame(win,width=1500,height=600)
frametop.grid()
framedown=tk.Frame(win,width=1500,height=100)
framedown.grid()

combox_v=tk.StringVar()
combox=ttk.Combobox(framedown,textvariable=combox_v)
combox.place(x=350,y=10)

t = ScrolledText(frametop,width=100,height=60,font=('黑体',18),background='#ffffff')
t.place(x=10,y=10)
#一版一个文件一个案例还是一行一个案例

text=''

text_label=[]#全局变量
number=0

output_file=open(r'result.txt', 'a',encoding='utf-8')

text_buffer=[]
flag=False

def delete_item(list,item,nunber):
	global text
	global number1
	for i,k in enumerate(list[number-1]):  #这个number要减一卧槽
		if k==item:
			del list[number-1][i]
	combox['value'] = list[number - 1]
	pattern = re.compile(r'{0}'.format(item))
	it = re.search(pattern, text)
	t.tag_add('tag{0}'.format(number+3), "%d.%d" % (1, it.span()[0]), "%d.%d" % (1, it.span()[1]))
	t.tag_config('tag{0}'.format(number+3), background='#ffffff', foreground='black')
	tk.messagebox.showinfo(title='delete success', message='删除成功')




def add_item(list,item,number):
	global  text
	list[number-1].append(item)
	combox['value'] = list[number-1]
	pattern = re.compile(r'{0}'.format(item))
	it = re.search(pattern, text)
	t.tag_add('tag1', "%d.%d" % (1, it.span()[0]), "%d.%d" % (1, it.span()[1]))
	t.tag_config('tag1', background='yellow', foreground='red')
	tk.messagebox.showinfo(title='add success', message='增加成功')





e=tk.IntVar()



def change_text(file):
	global  flag
	if flag==True:
		tkinter.messagebox.showinfo(message='请先导出该条信息')
		return
	t.delete(1.0,'end')
	global text
	text = file.readline()
	global number               #在函数内使用全局变量需要在函数内定义global关键字
	global combocitem
	if text:
		t.insert(tk.INSERT, text)
	else:
		t.insert(tk.INSERT, '已经是最后一页了')
	keyword_label = []
	with open(r"keyword_test.txt",encoding='utf-8') as keyfile:
		keyword = keyfile.readline().strip('\n')
		while keyword:
			pattern = re.compile(r'{0}'.format(keyword))
			it=re.search(pattern,text)
			if it!=None:
				t.tag_add('tag1', "%d.%d" % (1, it.span()[0]), "%d.%d" % (1, it.span()[1]))
				t.tag_config('tag1', background='yellow', foreground='red')
				keyword_label.append(keyword)
			keyword=keyfile.readline().strip('\n')
	if len(keyword_label)==0:
		keyword_label.append(0)
	combox['value']=keyword_label
	text_label.append(keyword_label)
	number+=1
	e.set(number)
	flag=True




file=open(r"123.txt",encoding='gbk')

button1=ttk.Button(framedown,text='下一条',command=lambda :change_text(file))
button1.place(x=10,y=10)



label1=tk.Label(framedown,textvariable=e).place(x=650,y=10)


button_add=ttk.Button(framedown,text='增加',command=lambda :add_item(text_label,combox_v.get(),number))
button_add.place(x=150,y=10)



button_delete=ttk.Button(framedown,text='删除',command=lambda :delete_item(text_label,combox_v.get(),number))
button_delete.place(x=250,y=10)


def write(list,output_file,text):
	global flag
	flag=False
	dict={}
	dict['text']=text.strip()
	if list==[]:
		dict['keyword']=list
	else:
		dict['keyword']=list[-1]
	output_file.write(json.dumps(dict,ensure_ascii=False)+'\n')



button_out=ttk.Button(framedown,text='导出',command=lambda :write(text_label,output_file,text))
button_out.place(x=350,y=40)











label1=tk.Label(framedown,text='文档路径:').place(x=10,y=40)
label2=tk.Label(framedown,text='关键词路径:').place(x=10,y=80)



e1=tk.StringVar()
e2=tk.StringVar()
entry1=tk.Entry(framedown,textvariable=e1).place(x=100,y=40)
entry2=tk.Entry(framedown,textvariable=e2).place(x=100,y=80)


win.mainloop()


file.close()
output_file.close()



