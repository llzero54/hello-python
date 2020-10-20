import tkinter as Tk
import threading
import time
import pathlib
import browsermobproxy as bwsproxy
from selenium import webdriver
from selenium.webdriver.chrome.options import Options as ChromeOptions
from os import path
import json

_THE_NAME = '智慧树播放器'
_THE_AUTHOR = 'llZero'


class Conf:
    """ 配置 """
    BASE_PATH = pathlib.Path(__file__).resolve().parent
    CHROME_DRIVER = path.join(BASE_PATH, 'chromedriver.exe')
    BROWSER_MOB_PROXY = path.join(BASE_PATH, 'browsermob-proxy', 'bin', 'browsermob-proxy')
    APP_ICON = path.join(BASE_PATH, 'icon.ico')
    LOAD_PAGE_TIMEOUT = 60  # 页面请求超时
    SHOW_BROWSER = True  # 是否显示浏览器界面
    ZHS = {
        'home_url': 'https://www.zhihuishu.com/',
        'login_url': 'https://passport.zhihuishu.com/login?service=https://onlineservice.zhihuishu.com/login/gologin',
        'student_index': 'https://onlineh5.zhihuishu.com/onlineWeb.html#/studentIndex'
    }


class CourseArgs:
    """课程参数"""

    def __init__(self):
        self.username = ''  # 登录用户名
        self.password = ''  # 登录密码
        self.user_ok = False  # 用户信息是否准备成功
        self.user_info = {}  # 用户信息
        self.course_info = {}  # 课程信息


class Player(threading.Thread):
    """播放 -> 线程"""

    def __init__(self, cf, ca):
        super().__init__()
        self.cf = cf
        self.ca = ca
        self.fun_msg = None  # 消息函数
        self.btn_start = None  # 启动按钮
        self.__running = False  # 线程运行标志
        self.__closed = True  # 线程关闭标志
        self.server = bwsproxy.Server(self.cf.BROWSER_MOB_PROXY)

    def run(self) -> None:
        self.msg('播放线程启动')
        try:
            self.__running = True
            self.__closed = False
            self.__starting()
        except Exception as e:
            self.__running = False
            self.msg('播放线程遇错误，终止线程。 => {}'.format(repr(e)), 'e')
        self.msg('关闭浏览器')
        try:
            self.browse.quit()
        except Exception as e:
            self.msg('浏览器关闭失败！=> {}'.format(repr(e)), 'e')
        self.msg('关闭代理服务')
        self.server.stop()
        self.msg('播放线程关闭')
        self.__closed = True
        # 启用登录按钮
        if self.btn_start:
            self.btn_start.config(state=Tk.NORMAL)

    def __starting(self):
        # 创建和启动代理服务
        self.msg('启动代理服务')
        self.server.start()
        self.proxy = self.server.create_proxy()
        # chrome启动参数
        chrome_options = ChromeOptions()
        chrome_options.add_argument('--proxy-server={0}'.format(self.proxy.proxy))
        if not self.cf.SHOW_BROWSER:
            chrome_options.add_argument('--no-startup-window')
        self.msg('打开浏览器')
        # self.browse = webdriver.Chrome(self.cf.CHROME_DRIVER, options=chrome_options)
        # self.proxy.new_har(options={'captureContent': True, 'captureHeaders': True})
        while self.__running:
            if not self.ca.user_ok and not self.__get_user_info():
                self.msg('获取用户信息失败！', 'e')
                self.__running = False
                break
            self.msg('播放器线程...')
            time.sleep(3)

    def __get_user_info(self):
        """登录账号并获取用户信息"""
        # if not self.__login_zhs():
        #     self.msg('用户名和密码验证失败！', 'e')
        #     return False
        # brw = self.browse
        # student_index = self.cf.ZHS['student_index']
        # # 跳转学生首页
        # if brw.current_url != student_index:
        #     brw.get(student_index)
        # res_user = None
        # res_course = None
        # while res_user is None or res_course is None:
        #     res_user = self.__find_har_entries_response(status=200, method='GET',
        #                                                 url='https://onlineservice.zhihuishu.com/login/getLoginUserInfo')
        #     res_course = self.__find_har_entries_response(status=200, method='POST',
        #                                                   url='https://onlineservice.zhihuishu.com/student/course/share/queryShareCourseInfo')
        # user = json.loads(res_user['content']['text'])
        # course_list = json.loads(res_course['content']['text'])
        user = json.loads(
            '{"result":{"realName":"王国富","headPicUrl":"https://image.zhihuishu.com/zhs/ablecommons/demo/201804/fd279ef12e514b4b9b7282ef27b1ae62.jpg","uuid":"E7q2lA08","username":"9205ffb5684b4257841a9837628a368e"},"code":200,"message":null}')
        course_list = json.loads(
            '{"result":{"totalCount":3,"courseOpenDtos":[{"courseId":2101131,"courseName":"设计创意生活","courseImg":"https://image.zhihuishu.com/download/upload/createcourse/image/159233511/777cb405-d6fd-4717-89ee-892942c5a371.jpg","teacherName":"王震亚","lessonName":null,"lessonNum":null,"progress":"0%","recruitId":32654,"lessonId":null,"courseCount":null,"schoolName":"山东大学","secret":"495a5f5d41524159454b595a59","courseStartTime":1600617600000,"courseEndTime":1605455999000,"status":0,"courseStatus":2,"courseType":1},{"courseId":2100337,"courseName":"从创意到创业","courseImg":"https://image.zhihuishu.com/zhs/createcourse/course/201903/3795381ad2aa44c0aff668009fee6cfd.jpg","teacherName":"孟奕爽","lessonName":null,"lessonNum":null,"progress":"0%","recruitId":32558,"lessonId":null,"courseCount":null,"schoolName":"湖南师范大学","secret":"495a5c5d4d524159454a5b5a5f","courseStartTime":1600617600000,"courseEndTime":1605455999000,"status":0,"courseStatus":2,"courseType":1},{"courseId":2097755,"courseName":"高效职场办公","courseImg":"https://image.zhihuishu.com/zhs/createcourse/course/201804/79605f1928414105950b3b6903206341.jpg","teacherName":"刘洋","lessonName":null,"lessonNum":null,"progress":"4.1%","recruitId":32443,"lessonId":null,"courseCount":null,"schoolName":"牡丹江大学","secret":"495a5d5c465241584c4d5f5c5d","courseStartTime":1600617600000,"courseEndTime":1605455999000,"status":0,"courseStatus":2,"courseType":1}]},"code":200,"message":null}')
        self.ca.user_info = user['result']
        self.ca.course_info = course_list['result']['courseOpenDtos']
        # 用户信息准备完成
        self.ca.user_ok = True
        return True

    def __login_zhs(self):
        """登录智慧树"""
        zhs_login_url = self.cf.ZHS['login_url']
        brw = self.browse
        # 访问登录页面
        self.msg('打开登录 => {}'.format(zhs_login_url))
        self.__get_sleep(zhs_login_url)
        login_username_input = brw.find_element_by_id('lUsername')
        login_password_input = brw.find_element_by_id('lPassword')
        login_btn = brw.find_element_by_class_name('wall-sub-btn')
        self.msg('输入用户名：{}'.format(self.ca.username))
        self.__input_content(login_username_input, self.ca.username, 3)
        self.msg('输入密码：***')
        self.__input_content(login_password_input, self.ca.password, 3)
        self.msg('点击登录！go go go ...')
        login_btn.click()
        time.sleep(5)
        # 页面未发生变化，用户名密码验证失败
        return brw.current_url != zhs_login_url

    @staticmethod
    def __input_content(tar, content, times=None, sp_times=0.5):
        """模拟内容输入"""
        if times is not None:
            time.sleep(times)
        for i in range(len(content)):
            time.sleep(sp_times)  # 每输入一个字符停止0.5s
            tar.send_keys(content[i])

    # 获取har中的请求返回内容
    def __find_har_entries_response(self, status=None, method=None, url=None):
        entries = self.proxy.har['log']['entries'].copy()
        entries.reverse()
        for e in entries:  # 倒序获取最新一条内容
            req = e['request']
            resp = e['response']
            s_true = status is None or status == resp['status']
            m_true = method is None or method == req['method']
            u_true = method is None or url == req['url']
            if s_true and m_true and u_true:
                return resp
        return None

    def __get_sleep(self, url, timer=5):
        self.browse.get(url)
        time.sleep(timer)

    def msg(self, text, t='i'):
        if self.fun_msg:
            self.fun_msg(text, t)

    def cancel(self):
        if not self.__running:
            return
        self.__running = False
        # 循环等待线程关闭
        while not self.__closed:
            pass


class MainApp:
    """
    主程序
        __WIN_WIDTH : 主界面固定宽度
        __WIN_HEIGHT : 主界面固定高度
    """
    __WIN_WIDTH = 650
    __WIN_HEIGHT = 480

    def __init__(self, name, author):
        self.cf = Conf
        self.ca = CourseArgs()
        self.player = None
        self.win_title = '{0} By {1}'.format(name, author)
        self.top = Tk.Tk()
        self.top.wm_title(self.win_title)
        self.top.wm_iconbitmap(default=self.cf.APP_ICON)
        self.top.geometry('{}x{}'.format(self.__WIN_WIDTH, self.__WIN_HEIGHT))
        self.top.wm_resizable(width=False, height=False)

    def start(self):
        self.__create_frame()
        self.__top_show()
        self.__left_show()
        self.__right_show()
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
        wel = Tk.Label(top, text='Hi, Are you not afraid!', font=('Microsoft YaHei', 10, 'bold'), foreground='#e33e33',
                       padx=10)
        ety_font = ('Microsoft YaHei', 12)
        self.__ety_usn = Tk.Entry(top, width=15, font=ety_font)
        self.__ety_pwd = Tk.Entry(top, width=15, font=ety_font, show='*')
        lbl_usn = Tk.Label(top, text='  USN')
        lbl_pwd = Tk.Label(top, text='  PWD')
        self.__btn_start = Tk.Button(top, text='启动', width=10, relief=Tk.GROOVE, command=self.__click_start_btn)
        wel.pack(fill=Tk.X, side=Tk.LEFT)
        self.__btn_start.pack(fill=Tk.X, side=Tk.RIGHT)
        self.__ety_pwd.pack(fill=Tk.X, side=Tk.RIGHT)
        lbl_pwd.pack(fill=Tk.X, side=Tk.RIGHT)
        self.__ety_usn.pack(fill=Tk.X, side=Tk.RIGHT)
        lbl_usn.pack(fill=Tk.X, side=Tk.RIGHT)
        top.pack_propagate(0)
        self.__ety_usn.insert('end', '18886096594')
        self.__ety_pwd.insert('end', 'RYEd6fSErumNTeh')

    def __click_start_btn(self):
        self.ca.username = self.__ety_usn.get()
        self.ca.password = self.__ety_pwd.get()
        if self.ca.username == '' or self.ca.password == '':
            self.__add_txt_msg('用户名或者密码不能为空！', 'e')
            return
        # 禁用按钮
        self.__btn_start.config(state=Tk.DISABLED)
        self.__create_player()
        # 开始播放
        self.player.start()

    def __create_player(self):
        """创建新的player线程"""
        self.__destroy_player()
        self.player = Player(self.cf, self.ca)
        self.player.fun_msg = self.__add_txt_msg
        self.player.btn_start = self.__btn_start

    def __destroy_player(self):
        """销毁播放器"""
        if self.player:
            self.player.fun_msg = None  # 消息框已被释放
            self.player.btn_start = None  # 启动按钮释放
            self.player.cancel()  # 退出线程
            self.player = None

    def __left_show(self):
        """左边部件:实时打印消息"""
        f_left = self.__f_left
        self.__txt_msg = Tk.Text(self.__f_left, font=('SimSum', '10', 'bold'), background=f_left.cget('background'),
                                 height=f_left.cget('height'), state=Tk.DISABLED)
        self.__txt_msg.pack(fill=Tk.Y)
        # INFO STYLE
        self.__txt_msg.tag_add('INFO', 'end')
        self.__txt_msg.tag_config('INFO', foreground='#3fab36')
        # WARNING STYLE
        self.__txt_msg.tag_add('WARNING', 'end')
        self.__txt_msg.tag_config('WARNING', foreground='#ffc107')
        # ERROR STYLE
        self.__txt_msg.tag_add('ERROR', 'end')
        self.__txt_msg.tag_config('ERROR', foreground='#f14336')
        self.__add_txt_msg('程序启动...')
        f_left.pack_propagate(0)

    def __add_txt_msg(self, msg, t='i'):
        """
        添加消息到消息框中
        :param msg: 消息内容
        :param t: 消息类型，i=>info,w=>warning,e=>error
        """
        t = t.lower()
        ty = 'INFO'
        if t == 'e':
            ty = 'ERROR'
        elif t == 'w':
            ty = 'WARNING'
        txt = '[{0}@{1}] {2}\n'.format(ty, time.strftime('%Y-%m-%d %H:%M:%S'), msg)
        self.__txt_msg.config(state=Tk.NORMAL)
        self.__txt_msg.insert('0.0', txt, ty)
        self.__txt_msg.config(state=Tk.DISABLED)

    def __right_show(self):
        """右边部件：控制参数"""

        pass

    def destroy(self):
        """释放资源"""
        self.__destroy_player()


if __name__ == '__main__':
    app = MainApp(_THE_NAME, _THE_AUTHOR)
    app.start()
    app.destroy()
