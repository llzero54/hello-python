import tkinter as Tk
import threading
import re
import time

_THE_NAME = '智慧树播放器'
_THE_AUTHOR = 'llZero'


# 配置
class Conf:
    pass


# 课程参数
class CourseArgs:
    def __init__(self):
        self.username = ''  # 登录用户名
        self.password = ''  # 登录密码


# 播放 -> 线程
class Player(threading.Thread):

    pass


class MainApp:
    """
    主程序
        __WIN_WIDTH : 主界面固定宽度
        __WIN_HEIGHT : 主界面固定高度
    """
    __WIN_WIDTH = 600
    __WIN_HEIGHT = 480

    def __init__(self, name, author):
        self.cf = Conf
        self.ca = CourseArgs
        self.win_title = '{0} By {1}'.format(name, author)
        self.top = Tk.Tk()
        self.top.wm_title(self.win_title)
        self.top.geometry('{}x{}'.format(self.__WIN_WIDTH, self.__WIN_HEIGHT))
        self.top.wm_resizable(width=False, height=False)

    def start(self):
        self.__create_frame()
        self.__top_show()
        self.__left_show()
        self.top.mainloop()

    def __create_frame(self):
        """创建布局，主界面分为三部分"""
        master = self.top
        f_top_w = self.__WIN_WIDTH
        f_top_h = 38
        f_left_w = 420
        f_left_h = self.__WIN_HEIGHT - f_top_h
        f_right_w = self.__WIN_WIDTH - f_left_w
        f_right_h = f_left_h
        self.__f_top = Tk.LabelFrame(master, width=f_top_w, height=f_top_h, borderwidth=3, relief=Tk.RIDGE)
        self.__f_left = Tk.Frame(master, background='#282a36', width=f_left_w, height=f_left_h)
        self.__f_right = Tk.Frame(master, width=f_right_w, height=f_right_h, borderwidth=3, relief=Tk.RIDGE)
        self.__f_top.pack(fill=Tk.X, side=Tk.TOP)
        self.__f_left.pack(fill=Tk.Y, side=Tk.LEFT)
        self.__f_right.pack(fill=Tk.Y, side=Tk.RIGHT)

    def __top_show(self):
        """
        顶部部件内容：
            * welcome文本
            * 登录表单
        """
        top = self.__f_top
        wel = Tk.Label(top, text='Hi, Are you not afraid!', font=('Microsoft YaHei', 10, 'bold')
                       , foreground='#21222c', padx=10)
        font = ('Microsoft YaHei', 12)
        self.__lbl_usn = Tk.Entry(top, width=15, font=font)
        self.__lbl_pwd = Tk.Entry(top, width=15, font=font, show='*')
        self.__btn_get = Tk.Button(top, text='获取', width=10, relief=Tk.GROOVE)
        wel.pack(fill=Tk.X, side=Tk.LEFT)
        self.__btn_get.pack(fill=Tk.X, side=Tk.RIGHT)
        self.__lbl_pwd.pack(fill=Tk.X, side=Tk.RIGHT)
        self.__lbl_usn.pack(fill=Tk.X, side=Tk.RIGHT)
        top.pack_propagate(0)
        self.__btn_get.bind('<Button-1>', self.__click_get_btn)

    def __click_get_btn(self, e):
        self.cf.username = self.__lbl_usn.get()
        self.cf.password = self.__lbl_pwd.get()

    def __left_show(self):
        """左边部件:实时打印消息"""
        f_left = self.__f_left
        self.__txt_msg = Tk.Text(self.__f_left, font=('SimSum', '10', 'bold'), foreground='#3fab36'
                                 , background=f_left.cget('background'), height=f_left.cget('height')
                                 , state=Tk.DISABLED)
        self.__add_txt_msg('程序启动...')
        self.__txt_msg.pack(fill=Tk.Y)
        f_left.pack_propagate(0)

    def __add_txt_msg(self, msg, t='i'):
        """
        添加消息到消息框中
        :param msg: 消息内容
        :param t: 消息类型，i=>info,w=>warning,e=>error
        """
        ty = 'INFO'
        if t == 'e':
            ty = 'ERROR'
        elif t == 'w':
            ty = 'WARNING'
        txt = '[{0}@{1}] {2}\n'.format(ty, time.strftime('%Y-%m-%d %H:%M:%S'), msg)
        self.__txt_msg.config(state=Tk.NORMAL)
        self.__txt_msg.insert('insert', txt)
        self.__txt_msg.config(state=Tk.DISABLED)

    def __right_show(self):
        """右边部件：控制参数"""
        pass

    def destroy(self):
        """释放资源"""
        pass


if __name__ == '__main__':
    app = MainApp(_THE_NAME, _THE_AUTHOR)
    app.start()
    app.destroy()
