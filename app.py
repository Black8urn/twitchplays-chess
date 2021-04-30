import sys
import urllib
import requests
import webbrowser
import http.server

import chess
import chess.svg

from threading import Thread
from PyQt5 import QtWidgets, QtSvg, QtCore


class ChessWidget(QtWidgets.QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)

        self._board = chess.Board()
        self._svg = QtSvg.QSvgWidget()

        layout = QtWidgets.QGridLayout(self)
        layout.addWidget(self._svg)
        self.setLayout(layout)
        self.setGeometry(100, 100, 300, 300)

        self._timer = QtCore.QTimer()
        self._timer.setInterval(1000)
        self._timer.timeout.connect(self._update_board)
        self._timer.start()

        # self._draw_svg()

    def _draw_svg(self):
        print("Drew board")
        move = chess.Move.from_uci('g1f3')
        if move in self._board.legal_moves:
            self._board.push(move)
        board_svg = chess.svg.board(self._board)
        self._svg.renderer().load(bytearray(board_svg, encoding='utf-8'))
        self._svg.setGeometry(0, 0, 300, 300)

    @QtCore.pyqtSlot()
    def _update_board(self):
        # Get updates

        # Redraw board
        self._draw_svg()

        # pass


class TwitchApiResponseHandler(http.server.BaseHTTPRequestHandler):
    def do_GET(self):
        query_strings = urllib.parse.parse_qs(self.path.strip('/?'))
        token, = query_strings['access_token']

        response = requests.get(url='https://id.twitch.tv/oauth2/validate', headers={'Authorization': f"OAuth {token}"})

        self.send_response(200)
        self.end_headers()
        self.wfile.write(bytearray("You may now close this window", encoding='utf-8'))
        self.close_connection = True


def serve(addr, port):
    with http.server.ThreadingHTTPServer((addr, port), TwitchApiResponseHandler) as server:
        server.serve_forever(poll_interval=None)


if __name__ == "__main__":
    thread = Thread(target=serve, args=("", 3000), daemon=True).start()
    response = webbrowser.open(url='https://id.twitch.tv/oauth2/authorize?'
                                   'client_id=3nrwym93iwb6hogjmgesv8lbx9yrhb&'
                                   'redirect_uri=http://localhost:3000/&'
                                   'response_type=token&'
                                   'scope=channel:manage:redemptions', new=1)

    app = QtWidgets.QApplication(sys.argv)
    ui = QtWidgets.QMainWindow()
    ui.setWindowFlags(QtCore.Qt.FramelessWindowHint)
    widget = ChessWidget()
    widget.show()
    sys.exit(app.exec_())
    # board = chess.Board()
    # svg_board = chess.svg.board(board)
    # ba_svg = bytearray(svg_board, encoding='utf-8')
    #
    # svg_widget = QtSvg.QSvgWidget()
    # svg_widget.renderer().load(ba_svg)
    # svg_widget.setGeometry(100, 100, 300, 300)
    # svg_widget.show()
    # sys.exit(app.exec_())
    #
    # print('test')
