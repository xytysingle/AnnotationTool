import logging
import logging.handlers
import sys
import os
import yaml


def setup_logging(name):
    FORMAT = '[%(asctime)s] %(levelname)s %(filename)s:%(lineno)4d: [%(name)s] %(message)s'
    # Manually clear root loggers to prevent any module that may have called
    # logging.basicConfig() from blocking our logging setup
    logging.root.handlers = []
    logging.basicConfig(level=logging.INFO, format=FORMAT, stream=sys.stdout)
    logger = logging.getLogger(name)

    if os.path.exists('mail.yaml'):
        mail = yaml.load(open('mail.yaml'))
        logging.handlers.SMTPHandler.emit = emit
        mail_handler = logging.handlers.SMTPHandler(
            mailhost=(mail['host'], mail['port']),
            fromaddr=mail['from'],
            toaddrs=[mail['to']],
            subject=mail['subject'],
            credentials=(mail['username'], mail['password']),
        )
        mail_handler.setFormatter(logging.Formatter(FORMAT))
        mail_handler.setLevel(logging.WARNING)
        logger.addHandler(mail_handler)
    return logger


def emit(self, record):
    """
    Overwrite the logging.handlers.SMTPHandler.emit function with SMTP_SSL.
    Emit a record.
    Format the record and send it to the specified addressees.
    """
    try:
        import smtplib
        from email.utils import formatdate
        port = self.mailport
        if not port:
            port = smtplib.SMTP_PORT
        smtp = smtplib.SMTP_SSL(self.mailhost, port, timeout=self._timeout)
        msg = self.format(record)
        msg = "From: %s\r\nTo: %s\r\nSubject: %s\r\nDate: %s\r\n\r\n%s" % (self.fromaddr, ", ".join(self.toaddrs), self.getSubject(record), formatdate(), msg)
        if self.username:
            smtp.ehlo()
            smtp.login(self.username, self.password)
        smtp.sendmail(self.fromaddr, self.toaddrs, msg)
        smtp.quit()
    except (KeyboardInterrupt, SystemExit):
        raise
    except:
        self.handleError(record)
