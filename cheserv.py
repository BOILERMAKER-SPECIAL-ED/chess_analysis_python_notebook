import sqlite3
import hashlib
import chess
import chess.pgn
import chess.svg
from  sqlite3  import  Error
from hashlib import blake2b
from http.server import HTTPServer, SimpleHTTPRequestHandler
import ssl
class ChessDB2HTTPService(SimpleHTTPRequestHandler):
    def do_GET(self):
        if self.path.startswith("/index.htm") and self.path.endswith("/index.htm"):
          self.send_response(200)
          self.send_header("Content-type", "text/html")
          self.end_headers()
          return self.wfile.write(b'OK')
        elif self.path.startswith("/favicon.ico") and self.path.endswith("/favicon.ico"):
          self.send_response(200)
          self.send_header("Content-type", "image/x-icon")
          self.end_headers()
          return self.wfile.write(b'OK')
        elif self.path.startswith("/favicon.png") and self.path.endswith("/favicon.png"):
          self.send_response(200)
          self.send_header("Content-type", "image/png")
          self.end_headers()
          return self.wfile.write(b'OK')
        elif self.path.startswith("/favicon.jpg") and self.path.endswith("/favicon.jpg"): 
          self.send_response(200)
          self.send_header("Content-type", "image/jpeg")
          self.end_headers()
          return self.wfile.write(b'OK')
        elif self.path.startswith("/favicon.gif") and self.path.endswith("/favicon.gif"): 
          self.send_response(200)
          self.send_header("Content-type", "image/gif")
          self.end_headers()
          return self.wfile.write(b'OK')
        elif self.path.startswith("/favicon.svg") and self.path.endswith("/favicon.svg"):
          self.send_response(200)
          self.send_header("Content-type", "image/svg+xml")
          self.end_headers()
          return self.wfile.write(b'OK')
        elif self.path.startswith("/favicon.ico") and self.path.endswith("/favicon.ico"):
          self.send_response(200)
          self.send_header("Content-type", "image/x-icon")
          self.end_headers()
          return self.wfile.write(b'OK')
        elif self.path.startswith("/favpos.svg") and self.path.endswith("/favpos.svg"):
          self.get_fav_pos()
          self.send_response(200)
          self.send_header("Content-type", "image/png")
          self.end_headers()
          return self.wfile.write(b'OK')
        elif self.path.startswith("/2favpos.svg") and self.path.endswith("/2favpos.svg"):
          self.get_2fav_pos()
          self.send_response(200)
          self.send_header("Content-type", "image/png")
          self.end_headers()
          return self.wfile.write(b'OK')
        elif self.path.startswith("/index.html") and self.path.endswith("/index.html"):
          self.send_response(200)
          self.send_header("Content-type", "text/html")
          self.end_headers()
          f = open("index.html", "r")
          self.wfile.write(f.read().encode())
          f.close()
          return self.wfile.write(b'OK')
        else:
          return self.wfile.write(bytes(self.path.encode()))
        
    def do_POST(self):
        content_payload = int(self.headers['Content-Length'])
        body = self.rfile.read(content_payload)
        print(self.command+":\t"+self.path)
        print(body)
        self.send_response(200)
        self.end_headers()
        response = BytesIO()
        response.write(b'<H1>vvvvvvv POST Request("+str(content_payload)+") vvvvvvv</H1>')
        response.write(body)
        response.write(b'<H1>^^^^^^^ End of POST ^^^^^^^</H1>')
        self.wfile.write(response.getvalue())
    def get_2fav_pos (self): 
        conn = sqlite3.connect('/Users/edgarjohnson/Desktop/twic1450-2GamesPositions.db')
        cur = conn.cursor()
        sql = ( "select id, move, pposition, rposition, total01, total, CAST(total01 as REAL)/CAST(total as REAL) as m from positions where total > 10 and m > .8;")
        print(sql)
        cur.execute(sql)
        #cur.execute( "SELECT MAX(total), * FROM positions where move == '"+move+"';" )
        rows = cur.fetchall()
        for r in rows:
            print(r)
            board = chess.Board(r[2])
            self.log(chess.svg.board(board,size=320))
            board = chess.Board(r[3])
            self.log(chess.svg.board(board,size=320))
            self.log_br()
        #if len(rows)>0:
        #    board = chess.Board(rows[0][2])
        #    self.log(chess.svg.board(board,size=320))
        return rows
    def get_fav_pos (self): 
        conn = sqlite3.connect('/Users/edgarjohnson/Desktop/twic1450-2GamesPositions.db')
        cur = conn.cursor()
        sql="select id, move, pposition, rposition, total10, total, CAST(total10 as REAL)/CAST(total as REAL) as m from positions where total > 10 and m > .8;"
        print(sql)
        cur.execute(sql)
        #cur.execute( "SELECT MAX(total), * FROM positions where move == '"+move+"';" )
        rows = cur.fetchall()
        for r in rows:
            print(r)
            board = chess.Board(r[2])
            self.log(chess.svg.board(board,size=320))
            board = chess.Board(r[3])
            self.log(chess.svg.board(board,size=320))
            self.log_br()
        #if len(rows)>0:
        #    board = chess.Board(rows[0][2])
        #    self.log(chess.svg.board(board,size=320))
        return rows

    def log(self, line):
        f = open("index.html", "a+")
        f.write(line)
        f.close()

    def log_br(self):
        f = open("index.html", "a+")
        f.write("\n<br/>\n")
        f.close()

httpd = HTTPServer(('127.0.0.1', 8484), ChessDB2HTTPService)
httpd.serve_forever()
