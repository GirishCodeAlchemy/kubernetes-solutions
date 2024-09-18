import json

import psycopg2
from flask import Flask, jsonify, request

app = Flask(__name__)


def get_db_connection():
    conn = psycopg2.connect(
        # if postgres is running on K8s cluster use the below hostname.
        host="postgres.postgres.svc.cluster.local",
        database="namespace",
        user="root",
        password="mypassword"
    )
    return conn

@app.route('/webhook', methods=['POST'])
def webhook():
    data = request.json
    namespace_name = data["request"]["object"]["metadata"]["name"]
    labels = data["request"]["object"]["metadata"]["labels"]
    status = data["request"]["object"]["status"]["phase"]

    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute(
        "INSERT INTO namespace_update (name, labels, status) VALUES (%s, %s, %s)",
        (namespace_name, json.dumps(labels), status))
    conn.commit()
    cur.close()
    conn.close()

    return jsonify({"status": "success"}), 200


@app.route('/delete', methods=['POST'])
def delete():
    data = request.json
    if data is None:
        return jsonify({"status": "error"}), 400
    else:
        print(data)
        namespace_name = data["request"]["object"]["metadata"]["name"]
        conn = get_db_connection()
        cur = conn.cursor()
        cur.execute("DELETE FROM namespace_update WHERE name = '%s'", (namespace_name))
        conn.commit()
        cur.close()
        conn.close()
        return jsonify({"status": "success"}), 200


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, ssl_context=('/etc/ssl/ca-certificates/tls.crt', '/etc/ssl/ca-certificates/tls.key'), debug=True)