#  MIT License
#
#  Copyright (c) 2021 Jinho Ko
#
#  Permission is hereby granted, free of charge, to any person obtaining a copy
#  of this software and associated documentation files (the "Software"), to deal
#  in the Software without restriction, including without limitation the rights
#  to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
#  copies of the Software, and to permit persons to whom the Software is
#  furnished to do so, subject to the following conditions:
#
#  The above copyright notice and this permission notice shall be included in all
#  copies or substantial portions of the Software.
#
#  THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
#  IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
#  FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
#  AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
#  LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
#  OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
#  SOFTWARE.

import sys
from flask import Flask, render_template, request, jsonify
from flask_bootstrap import Bootstrap

from forms import InputOutputForm
from DB2Connector import executionContext

app = Flask(__name__)
app.config.from_mapping(
    SECRET_KEY=b'\xd6\x04\xbdj\xfe\xed$c\x1e@\xad\x0f\x13,@G')
Bootstrap(app)

def toHTMLStr(s):
    return s
    return s.replace('\n', '<br>').replace(' ', '&nbsp')

@app.route("/", methods=['GET', 'POST'])
def home():
    form = InputOutputForm(request.form)
    return render_template('form.html', form=form)


@app.route('/process', methods=['POST'])
def process():
    inputSQL = request.form['inputSQL']
    rewrittenSQL = executionContext(inputSQL)
    response = {'response': toHTMLStr(rewrittenSQL) }
    return jsonify(response)


if __name__ == "__main__":
    app.run(host='localhost', port=50001)
