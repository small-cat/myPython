# -*- encoding: utf-8 -*-
import hashlib
import re


def gen_md5(url):
    """
    generate md5 sequence of url
    :param url:
    :return:
    """
    # check the encodings of url, in python3, all the data is unicode, maybe, you should encode
    # into utf8 first
    if isinstance(url, str):
        url = url.encode("utf-8")

    m = hashlib.md5()
    m.update(url)

    return m.hexdigest()


def extract_nums(text):
    """
    从字符串中提取 数字
    """
    re_match = re.match(".*?(\d+).*", text)
    if re_match:
        nums = (int)(re_match.group(1))
    else:
        nums = 0

    return nums


if __name__ == "__main__":
    print(gen_md5("https://www.jobbole.com"))