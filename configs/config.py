# encoding=utf-8

# base_dir = os.path.abspath(os.path.dirname(__file__))






#
# class UnixConfig(ProductionConfig):
#     @classmethod
#     def init_app(cls, app):
#         ProductionConfig.init_app(app)
#
#         # 写入系统日志 日志会写入 /var/log/messages
#         import logging
#         from logging.handlers import SysLogHandler
#         syslog_handler = SysLogHandler()
#         syslog_handler.setLevel(logging.WARNING)
#         app.logger.addHandler(syslog_handler)
