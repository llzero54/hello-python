from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as ec
from selenium.webdriver.common.by import By
from browsermobproxy import Server
from time import sleep
from platform import system

'''
 * 常量
'''
# User Info
U_USERNAME = '18212295325'  # 用户名

U_PASSWORD = '245679009As'  # 密码

# Setting

LOAD_PAGE_TIMEOUT = 60  # 页面请求超时

COURSE_DEGREE_OF_COMPLETION = '100%'  # 课程达到多少算完成

# 智慧树首页地址
ZHS_INDEX_URL = 'https://www.zhihuishu.com/'

# 智慧树登录地址
ZHS_LOGIN_URL = 'https://passport.zhihuishu.com/login?service=https://onlineservice.zhihuishu.com/login/gologin'

# 学生首页
ZHS_STUDENT_INDEX_URL = 'https://onlineh5.zhihuishu.com/onlineWeb.html#/studentIndex'

# 题目获取URL
ZHS_LESSON_POPUP_EXAM = 'https://studyservice.zhihuishu.com/popupAnswer/lessonPopupExam'

# browsermob-proxy path, 旧版本对ssl支持不好
BROWSERMOB_PROXY = '../inc/browsermob-proxy/bin/browsermob-proxy'

'''
 * 函数
'''


# 模拟输入内容
def input_content(tar, content, times=None, sp_times=0.5):
    if times is not None:
        sleep(times)
    for i in range(len(content)):
        sleep(sp_times)  # 每输入一个字符停止0.5s
        tar.send_keys(content[i])


# 获取har中的请求返回内容
def find_har_entries_response(status=None, method=None, url=None):
    entries = proxy.har['log']['entries'].copy()
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


# 答题答题
def auto_answer():
    try:
        answer_dialog = browse.find_element_by_tag_name('div[aria-label="弹题测验"]')
        # 从network中获取答案信息
        response = find_har_entries_response(status=200, url=ZHS_LESSON_POPUP_EXAM)
        assert response is not None
    except NoSuchElementException:
        print('There is no quiz...')


# 页面加载等待
def load_page_wait(url=None):
    tip = 'Page failed to load...'
    if url is not None:
        WebDriverWait(browse, LOAD_PAGE_TIMEOUT).until(lambda d: url == browse.current_url, tip)
    WebDriverWait(browse, LOAD_PAGE_TIMEOUT).until(ec.presence_of_all_elements_located((By.TAG_NAME, 'script'))
                                                   and ec.presence_of_element_located((By.TAG_NAME, 'html')), tip)


'''
 * 执行
'''
if system() == 'Windows':
    BROWSERMOB_PROXY = BROWSERMOB_PROXY.replace('/', '\\')
server = Server(BROWSERMOB_PROXY)
server.start()

proxy = server.create_proxy()
chrome_options = Options()
# 设置chrome代理
chrome_options.add_argument('--proxy-server={0}'.format(proxy.proxy))
# 启动时不创建窗口
# chrome_options.add_argument(' --no-startup-window');

browse = webdriver.Chrome('../chromedriver.exe', options=chrome_options)
proxy.new_har(options={'captureContent': True, 'captureHeaders': True})

# 跳转登录地址
browse.get(ZHS_LOGIN_URL)

# 填写登录信息
load_page_wait()
login_username_input = browse.find_element_by_id('lUsername')
login_password_input = browse.find_element_by_id('lPassword')
input_content(login_username_input, U_USERNAME, 3)
input_content(login_password_input, U_PASSWORD, 3)

# 点击登录按钮
sleep(3)
login_btn = browse.find_element_by_class_name('wall-sub-btn')
login_btn.click()

# 是否自动跳转到学生首页
load_page_wait(ZHS_STUDENT_INDEX_URL)
if browse.current_url != ZHS_STUDENT_INDEX_URL:
    browse.get(ZHS_STUDENT_INDEX_URL)  # 跳转至学生首页
load_page_wait(ZHS_STUDENT_INDEX_URL)
assert browse.current_url == ZHS_STUDENT_INDEX_URL

# 获取未完成的课程列表
share_course_data_list = browse.find_elements_by_class_name('datalist')  # 获取所有课程信息
current_course_data_list = []  # 未完成的课程信息
for share_course in share_course_data_list:
    if float(share_course.find_element_by_class_name('processNum').text.replace('%', '')) < float(
            COURSE_DEGREE_OF_COMPLETION.replace('%', '')):
        current_course_data_list.append(share_course)
assert len(current_course_data_list) != 0

for current_course in current_course_data_list:
    # 进入课程
    current_course.find_element_by_class_name('courseName').click()
    load_page_wait()
    sleep(2)
    # 关闭可能出现的dialog
    # #智慧树警告dialog
    try:
        zhs_warring_dialog = browse.find_element_by_tag_name('div[aria-label="智慧树警告"]')
        if zhs_warring_dialog.text != '':
            sleep(5)
            zhs_warring_dialog.find_element_by_tag_name('button').click()  # #关闭警告dialog
    except NoSuchElementException:
        print('No wisdom tree warning dialog...')
    # #学前必读dialog
    try:
        zhs_read_dialog = browse.find_element_by_tag_name('div[class="dialog-read"]')
        if zhs_read_dialog.text != '':
            sleep(5)
            zhs_read_dialog.find_element_by_tag_name('i').click()
    except NoSuchElementException:
        print('There is no required dialog...')

    # 获取未完成的章节信息

# proxy.close()
# browse.close()
# server.stop()
