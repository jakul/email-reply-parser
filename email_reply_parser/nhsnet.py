from email_reply_parser import EmailMessage


class NHSNETEmailReplyParser(object):
    """ Represents a email message that is parsed from an nhs.net email address.
    """

    @staticmethod
    def read(text):
        """ Factory method that splits email into list of fragments

            text - A string email body

            Returns an NHSNETEmailMessage instance
        """
        return NHSNETEmailMessage(text).read()

    @staticmethod
    def parse_reply(text):
        """ Provides the reply portion of email.

            text - A string email body

            Returns reply body message
        """
        return NHSNETEmailReplyParser.read(text).reply


class NHSNETEmailMessage(EmailMessage):
    """
    Emails from nhs.net don't include traditional quoting for the original
    message, so this class aims to properly detect and remove the message
    that was replied to.

    This class also detects a number of common signatures that the original
    didn't.

    Known limitations:
      * emails without a line break between the content and the signature
        do not detect the signature properly

    """

    # Detect various nhs.net quoted blocks of the format:
    #
    #    From: Company Name [mailto:address@domain.com]
    #    Sent: 29 March 2013 13:44
    #    To: recipient one (number one); recipient two (number two)
    #    Subject: Email subject
    #
    # These lines can appear in any order, and sometimes have different names
    # e.g. `Date` instead of `Sent`.
    MULTI_QUOTE_HDR_REGEX = r'(On\s.*?wrote:|From:\s.*?Sent:\s.*?To:\s.*?Subject:\s.*?\Z|From:\s.*?To:\s.*?Subject:\s.*?Date:\s.*?\Z|From:\s.*?Subject:\s.*?To:\s.*?Date:\s.*?\Z)'
    QUOTED_REGEX = r'(>+)|(From:\s.*?Sent:\s.*?To:\s.*?Subject:\s.*?)|(From:\s.*?To:\s.*?Subject:\s.*?Date:\s.*?|From:\s.*?Subject:\s.*?To:\s.*?Date:\s.*?)'
    # Be a bit more greedy in the signature parsing
    SIG_REGEX = r'--|__|-\w|^Sent from my (\w+\s*){1,3}|^Sent from Samsung Mobile|^[*][*][*][*][*][*][*][*][*]+$|^[\w ]*[Rr]egards[,]?$|^[\w ]*[Tt]hanks[,]?$|This email is intended for the addressee\(s\) named above|This email is confidential and may also be privileged. If you are not the i|E-MAIL DISCLAIMER - IMPORTANT INFORMATION'
