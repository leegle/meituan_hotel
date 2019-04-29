# coding=utf-8

"""承担的任务在于
    接收新的cookie值
    并写入 ./cookie/cookie.txt 中
"""

import tornado.web
from tornado.ioloop import IOLoop
from cookie_handler import receive_cookie_and_reload
from log_handler import log
from log_handler import output_log


class MainHandler(tornado.web.RequestHandler):
    # 需要对参数进行验证
    param_names = 'cookie_value'

    def get(self):

        page = """
        <h1>请在框内输入最新的cookie</h1>
        <form method="post" style="width:200px;height:100px;">
            <p><input type=text name=cookie_value></p>
            <p><input type=submit value=提交></p>
        </form>
        <meta http-equiv="refresh" content="10">
        <h2> 日志展示 </h2>
        <h2> 刷新时间为30秒 </h2>
        <h2> 展示最近30条日志 </p>
        <textarea style="width:900px;height:600px;"> {0} </textarea>
        """.format(output_log())
        self.write(page)

    def post(self):
        log.debug('web: 接收到新的cookie')
        try:
            cookie_ctx = self.get_argument(self.param_names)
        except Exception as e:
            log.warning('web: 接收到错误参数\t{0},'.format(e))
        else:
            final_page = """
                <h1>OK! 已经提交</h1>
                <meta http-equiv="refresh" content="10">
            """
            receive_cookie_and_reload(cookie_ctx)
            self.write(final_page)


application = tornado.web.Application([(r"/send_cookie", MainHandler), ])

if __name__ == "__main__":
    application.listen(24000)
    IOLoop.instance().start()
