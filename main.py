#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# __author__ = 'Liantian'
# __email__ = "liantian.me+code@gmail.com"
#
# Copyright 2015-2016 liantian
#
# This is free and unencumbered software released into the public domain.
#
# Anyone is free to copy, modify, publish, use, compile, sell, or
# distribute this software, either in source code form or as a compiled
# binary, for any purpose, commercial or non-commercial, and by any
# means.
#
# In jurisdictions that recognize copyright laws, the author or authors
# of this software dedicate any and all copyright interest in the
# software to the public domain. We make this dedication for the benefit
# of the public at large and to the detriment of our heirs and
# successors. We intend this dedication to be an overt act of
# relinquishment in perpetuity of all present and future rights to this
# software under copyright law.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND,
# EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF
# MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT.
# IN NO EVENT SHALL THE AUTHORS BE LIABLE FOR ANY CLAIM, DAMAGES OR
# OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE,
# ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR
# OTHER DEALINGS IN THE SOFTWARE.
#
# For more information, please refer to <http://unlicense.org>


import os
import jieba
import jieba.posseg
import jieba.analyse
from flask import Flask, request, jsonify, render_template

app = Flask(__name__)
if 'SERVER_SOFTWARE' in os.environ and os.environ['SERVER_SOFTWARE'].startswith('Dev'):
    app.config['DEBUG'] = True
app.config['JSON_AS_ASCII'] = False


@app.errorhandler(404)
def page_not_found(e):
    return "Error : 404 - Page Not Found", 404


@app.route('/')
def index():
    return render_template("index.html")


@app.route('/cut', methods=['GET', 'POST'])
def cut():
    text = request.values.get('text', "text")
    cut_all = request.values.get("cut_all", default="0")
    if cut_all in ['0', '1']:
        cut_all = bool(int(cut_all))
    else:
        cut_all = False
    hmm = request.values.get("hmm", default="1")
    if hmm in ['0', '1']:
        hmm = bool(int(cut_all))
    else:
        hmm = True

    result = list(jieba.cut(text, cut_all=cut_all, HMM=hmm))
    return jsonify(text=text, cut_all=cut_all, hmm=hmm, result=result)



@app.route('/analyse_tfidf', methods=['GET', 'POST'])
def analyse_tfidf():
    text = request.values.get('text', "text")
    topK = request.values.get("topK", default="20")
    if topK in [str(x) for x in  range(3,41)]:
        topK = int(topK)
    else:
        topK = 20
    withWeight = request.values.get("withWeight", default="0")
    if withWeight in ['0', '1']:
        withWeight = bool(int(withWeight))
    else:
        withWeight = True

    result = list(jieba.analyse.extract_tags(text, topK=topK, withWeight=withWeight))
    return jsonify(text=text, topK=topK, withWeight=withWeight, result=result)


@app.route('/analyse_textrank', methods=['GET', 'POST'])
def analyse_textrank():
    text = request.values.get('text', "text")
    topK = request.values.get("topK", default="20")
    if topK in [str(x) for x in  range(3,41)]:
        topK = int(topK)
    else:
        topK = 20
    withWeight = request.values.get("withWeight", default="0")
    if withWeight in ['0', '1']:
        withWeight = bool(int(withWeight))
    else:
        withWeight = True
    result = list(jieba.analyse.textrank(text, topK=topK, withWeight=withWeight))
    return jsonify(text=text, topK=topK, withWeight=withWeight, result=result)