# -*- encoding: utf-8 -*-
import hashlib


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

if __name__ == "__main__":
    print(gen_md5("https://www.jobbole.com"))