import collections
import copy
import os
import random

from flask import Flask, escape, request, json, send_from_directory, redirect
import sqlite3
app = Flask(__name__, static_folder='static')

conn = sqlite3.connect('test.db', check_same_thread=False)
conn.execute('''DROP table if exists result;''')
conn.execute('''DROP table if exists answers;''')
conn.execute('''CREATE TABLE if not exists result
         (ID INTEGER PRIMARY KEY AUTOINCREMENT,
         subject          TEXT    NOT NULL,
         q1        CHAR(1),
         q2        CHAR(1),
         q3        CHAR(1),
         q4        CHAR(1),
         q5        CHAR(1),
         q6        CHAR(1),
         q7        CHAR(1),
         q8        CHAR(1),
         q9        CHAR(1),
         q10        CHAR(1),
         q11        CHAR(1),
         q12        CHAR(1),
         q13        CHAR(1),
         q14        CHAR(1),
         q15        CHAR(1),
         q16        CHAR(1),
         q17        CHAR(1),
         q18        CHAR(1),
         q19        CHAR(1),
         q20        CHAR(1),
         q21        CHAR(1),
         q22        CHAR(1),
         q23        CHAR(1),
         q24        CHAR(1),
         q25        CHAR(1),
         q26        CHAR(1),
         q27        CHAR(1),
         q28        CHAR(1),
         q29        CHAR(1),
         q30        CHAR(1),
         q31        CHAR(1),
         q32        CHAR(1),
         q33        CHAR(1),
         q34        CHAR(1),
         q35        CHAR(1),
         q36        CHAR(1),
         q37        CHAR(1),
         q38        CHAR(1),
         q39        CHAR(1),
         q40        CHAR(1),
         q41        CHAR(1),
         q42        CHAR(1),
         q43        CHAR(1),
         q44        CHAR(1),
         q45        CHAR(1),
         q46        CHAR(1),
         q47        CHAR(1),
         q48        CHAR(1),
         q49        CHAR(1),
         q50        CHAR(1),
         name       TEXT,
         url        TEXT,
         score      INTEGER);''')
conn.execute('''CREATE TABLE if not exists answers
         (test_id         INTEGER PRIMARY KEY AUTOINCREMENT,
         subject          TEXT    NOT NULL,
         q1        CHAR(1),
         q2        CHAR(1),
         q3        CHAR(1),
         q4        CHAR(1),
         q5        CHAR(1),
         q6        CHAR(1),
         q7        CHAR(1),
         q8        CHAR(1),
         q9        CHAR(1),
         q10        CHAR(1),
         q11        CHAR(1),
         q12        CHAR(1),
         q13        CHAR(1),
         q14        CHAR(1),
         q15        CHAR(1),
         q16        CHAR(1),
         q17        CHAR(1),
         q18        CHAR(1),
         q19        CHAR(1),
         q20        CHAR(1),
         q21        CHAR(1),
         q22        CHAR(1),
         q23        CHAR(1),
         q24        CHAR(1),
         q25        CHAR(1),
         q26        CHAR(1),
         q27        CHAR(1),
         q28        CHAR(1),
         q29        CHAR(1),
         q30        CHAR(1),
         q31        CHAR(1),
         q32        CHAR(1),
         q33        CHAR(1),
         q34        CHAR(1),
         q35        CHAR(1),
         q36        CHAR(1),
         q37        CHAR(1),
         q38        CHAR(1),
         q39        CHAR(1),
         q40        CHAR(1),
         q41        CHAR(1),
         q42        CHAR(1),
         q43        CHAR(1),
         q44        CHAR(1),
         q45        CHAR(1),
         q46        CHAR(1),
         q47        CHAR(1),
         q48        CHAR(1),
         q49        CHAR(1),
         q50        CHAR(1));''')
conn.execute("INSERT INTO answers (subject, q1,q2,q3,q4,q5,q6,q7,q8,q9,q10,q11,q12,q13,q14,q15,q16,q17,q18,q19,q20,q21,q22,q23,q24,q25,q26,q27,q28,q29,q30,q31,q32,q33,q34,q35,q36,q37,q38,q39,q40,q41,q42,q43,q44,q45,q46,q47,q48,q49,q50) VALUES ('Math', 'A','B','C','D','A','B','C','D','A','B','A','A','A','A','A','A','A','A','A','A','A','B','C','D','A','B','C','D','A','B','A','B','C','D','A','B','C','D','A','B','A','B','C','D','A','B','C','D','A','B' );")
conn.commit()

@app.route('/api/tests', methods=['POST'])
def saveAnswer():
    data = {}
    akeys = {}
    conn = sqlite3.connect('test.db')
    cc = request.get_json()
    subject = cc['subject']
    answer = cc['answer_keys']
    keyz = list(answer.keys())
    keys = ["q" + suit for suit in keyz]
    values = list(answer.values())
    values = ["'" + suit + "'" for suit in values]
    sql = "INSERT INTO answers (subject, %s) VALUES ('%s', %s );"%(",".join(keys), subject, ",".join(values))
    print(sql)
    conn.execute(sql)
    curso = conn.execute("select * from answers order by test_id desc;")
    rows = curso.fetchall()
    print("ROWS: ", rows)
    data['test_id'] = rows[0][0]
    data['subject'] = rows[0][1]
    for x in range(1, 51):
        akeys["{0}".format(x)] = rows[0][x+1]
    data['answer_keys'] = akeys
    data['submissions'] = ""
    return json.dumps(data), 201

@app.route('/api/tests/<test_id>/scantrons', methods=['POST'])
def saveSubmission(test_id):
    test_id = request.view_args['test_id']
    result = {}
    sth = {}
    marks = 0
    file = request.files['data']
    root_dir = os.path.dirname(os.getcwd())
    no = random.randrange(1, 50)
    fname = "scantron" + str(no) + ".json"
    url = "http://localhost:5000/static/" + fname
    print("URL: ", url)
    file.save(os.path.join(root_dir, 'Assignment2', 'static', fname))
    file.seek(0)
    data = json.loads(file.read())
    answers = (data['answers'])
    subject = (data['subject'])
    name = (data['name'])
    conn = sqlite3.connect('test.db', check_same_thread=False)
    sql = "select * from answers where subject like '%s';"%(subject)
    cursor = conn.execute(sql)
    rows = cursor.fetchall()
    for x in range(1, 51):
        xx = {}
        xx['actual'] = answers['{0}'.format(x)]
        xx['expected'] = rows[0][x+1]
        if answers['{0}'.format(x)] == rows[0][x+1]:
            marks += 1
        result['{0}'.format(x)] = xx

    keyz = list(answers.keys())
    keys = ["q" + suit for suit in keyz]
    values = list(answers.values())
    values = ["'" + suit + "'" for suit in values]
    sql = "insert into result(subject, name, url, %s, score) values('%s', '%s', '%s', %s, %s);" %(",".join(keys), subject, name, url, ",".join(values), marks)

    conn.execute(sql)
    conn.commit()
    sql = "select * from result order by ID desc"
    c = conn.execute(sql)
    rows = c.fetchall()
    sth['scantron_id'] = rows[0][0]
    sth['result'] = result
    sth['score'] = marks
    sth['name'] = name
    sth['subject'] = subject
    sth['scantron_url'] = url
    return sth

@app.route('/api/tests/<test_id>', methods=['GET'])
def getSubmission(test_id):
    data = {}
    akeys = {}
    result = {}
    sth = {}
    test_id = request.view_args['test_id']
    conn = sqlite3.connect('test.db', check_same_thread=False)
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()
    sql = "select * from answers where test_id = %s;" %(test_id)
    c = conn.execute(sql)
    rows = c.fetchall()
    data['test_id'] = rows[0][0]
    data['subject'] = rows[0][1]
    for x in range(1, 51):
        akeys["{0}".format(x)] = rows[0][x + 1]
    data['answer_keys'] = akeys
    sql = "select * from result where subject = '%s';" %(rows[0][1])
    cursor.execute(sql)
    rows = cursor.fetchall()
    print(len(rows))
    submissions = []
    for row in rows:
        for x in range(1, 51):
            xx = {'actual': akeys['{0}'.format(x)], 'expected': row[x + 1]}
            result['{0}'.format(x)] = xx
        sth['scantron_id'] = row[0]
        sth['score'] = row["score"]
        sth['name'] = row["name"]
        sth['subject'] = data['subject']
        sth['scantron_url'] = row["url"]
        sth['result'] = result
        submissions.append(copy.deepcopy(sth))
    print(submissions)
    data['submissions'] = submissions
    return data

@app.route('/')
def hello_world():
    return 'Hello World!'

if __name__ == '__main__':
    app.run()
