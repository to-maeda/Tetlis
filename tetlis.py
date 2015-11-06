# -*- coding: utf-8 -*-
"""
ライン消去処理から
"""
from PyQt4 import QtGui, QtCore
import numpy as np
import sys
import random
import time
import tetlisWidget

class Tetlis(QtGui.QWidget):
    def __init__(self):
        super(Tetlis, self).__init__()

        self.initUI()

        self.initGame()

    def initUI(self):
        self.setGeometry(100, 100, 300, 600)
        self.show()

    def initGame(self):
        #ゲーム内変数の初期化
        self.currentBar = tetlisWidget.BaseBar()
        self.hasCurenntBar = False
        self.blockList = []
        self.usedBarArray = np.zeros((20, 10))
        self.fps = 0
        self.fpsTime = 0.0
        self.enableKeyPress = False
        self.blockType = 0
        #self.barCount = 0

        #ゲームループの開始
        self.gameTimer = QtCore.QTimer(self)
        self.gameTimer.timeout.connect(self.gameLoop)
        self.gameTimer.start(1)

    #ゲームループ
    def gameLoop(self):
        currentTime = time.time()

        if not self.hasCurenntBar:
            self.makeBar()
        else:
            if self.currentBar.isInWindow(270, 570, 0, -100) and self.isNoBarUnderCurrentBar():
                self.enableKeyPress = True
                self.currentBar.downBar()
            else:
                self.addUsedBarArray()
                self.updateBlock()
                self.checkLineIsFull()
                self.enableKeyPress = False
                self.hasCurenntBar = False

        #FPS制御
        afterTime = time.time()
        betweenTime = afterTime - currentTime
        if betweenTime < 0.033:
            time.sleep(0.033 - betweenTime)

        #FPS描画
        if (currentTime - self.fpsTime) >= 1.0:
            self.fpsTime = currentTime
            self.fps = 0

        self.fps = self.fps + 1


    #ランダムでバーの生成
    def makeBar(self):
        if self.usedBarArray[0][4] != 0:
            print "game over"
            exit()
        barType = random.randint(1, 7)
        self.hasCurenntBar = True
        if barType == 1:
            self.blockType = 1
            self.currentBar = tetlisWidget.TBar(self, 120, 0)
        elif barType == 2:
            self.blockType = 2
            self.currentBar = tetlisWidget.KeyBar1(self, 120, 0)
        elif barType == 3:
            self.blockType = 3
            self.currentBar = tetlisWidget.KeyBar2(self, 120, 0)
        elif barType == 4:
            self.blockType = 4
            self.currentBar = tetlisWidget.LBar1(self, 120, 0)
        elif barType == 5:
            self.blockType = 5
            self.currentBar = tetlisWidget.LBar2(self, 120, 0)
        elif barType == 6:
            self.blockType = 6
            self.currentBar = tetlisWidget.RectBar(self, 120, 0)
        elif barType == 7:
            self.blockType = 7
            self.currentBar = tetlisWidget.TetlisBar(self, 120, 0)

    #バーを使用済配列に追加
    def addUsedBarArray(self):
        for block in self.currentBar.blockList:
            x = self.getBlockIndexX(block)
            y = self.getBlockIndexY(block)
            #self.usedBarArray[y][x] = self.barCount
            self.usedBarArray[y][x] = self.blockType
        else:
            self.currentBar.deleteLater()

    def updateBlock(self):
        for block in self.blockList[:]:
            self.blockList.remove(block)
            block.deleteLater()
        for y in range(19, -1, -1):
            for x in range(0, 10, 1):
                value = self.usedBarArray[y][x]
                posX = x * 30
                posY = y * 30
                if value == 1:
                    block = tetlisWidget.TBlock(self)
                    block.move(posX, posY)
                    self.blockList.append(block)
                elif value == 2:
                    block = tetlisWidget.KeyBlock1(self)
                    block.move(posX, posY)
                    self.blockList.append(block)
                elif value == 3:
                    block = tetlisWidget.KeyBlock2(self)
                    block.move(posX, posY)
                    self.blockList.append(block)
                elif value == 4:
                    block = tetlisWidget.LBlock1(self)
                    block.move(posX, posY)
                    self.blockList.append(block)
                elif value == 5:
                    block = tetlisWidget.LBlock2(self)
                    block.move(posX, posY)
                    self.blockList.append(block)
                elif value == 6:
                    block = tetlisWidget.RectBlock(self)
                    block.move(posX, posY)
                    self.blockList.append(block)
                elif value == 7:
                    block = tetlisWidget.TetlisBlock(self)
                    block.move(posX, posY)
                    self.blockList.append(block)

    def checkLineIsFull(self):
        #for y in range(19, -1, -1):
        y = 19
        while (y > -1):
            for x in range(0, 10, 1):
                value = self.usedBarArray[y][x]
                if value == 0:
                    break
            else:
                self.deleteLine(y)
                self.updateBlock()
                y = y + 1
            y = y - 1

    def deleteLine(self, y):
        for j in range(y, 0, -1):
            for x in range(0, 10):
                print x
                self.usedBarArray[j][x] = self.usedBarArray[j - 1][x]

    def isNoBarUnderCurrentBar(self):
        for block in self.currentBar.blockList:
            posX = block.getPostionX()
            posY = block.getPostionY()
#            if not (posY % 30 == 0):
#                print posY
#                return True
            x = self.pos2index(posX)
            y = self.pos2index(posY) + 1
            if y > 19:
                return True
            if not(self.usedBarArray[y][x] == 0):
                print 'false'
                return False
        else:
            return True

    def barCanMoveToRight(self):
        for block in self.currentBar.blockList:
            x = self.getBlockIndexX(block)
            y = self.getBlockIndexY(block)
            right = x + 1
            if right > 9:
                return False
            if not(self.usedBarArray[y][right] == 0):
                return False
        else:
            return True

    def barCanMoveToLeft(self):
        for block in self.currentBar.blockList:
            x = self.getBlockIndexX(block)
            y = self.getBlockIndexY(block)
            left = x - 1
            if left < 0:
                return False
            if not(self.usedBarArray[y][left] == 0):
                return False
        else:
            return True

    def barCanRotate(self, blockList):
        for block in blockList:
            vector = block.getVector()
            x = vector[0] * 30
            y = vector[1] * 30
            barPosX = self.currentBar.getBarPostionX()
            barPosY = self.currentBar.getBarPostionY()
            blockPosX = x + barPosX
            blockPosY = y + barPosY
            indexX = self.pos2index(blockPosX)
            indexY = self.pos2index(blockPosY)
            if indexX == -1 or indexX == 10:
                return False
            elif indexY == -1 or indexY == 20:
                return False
            elif not(self.usedBarArray[indexY][indexX] == 0):
                return False
        else:
            return True

    def getBlockIndexX(self, block):
        posX = block.getPostionX()
        x = self.pos2index(posX)
        return x

    def getBlockIndexY(self, block):
        posY = block.getPostionY()
        y = self.pos2index(posY)
        return y

    def pos2index(self, pos):
        index = pos / 30.0
        return int(index)

    def drawGrid(self, qp):
        pen = QtGui.QPen()
        penColor = QtGui.QColor(0, 0, 0)
        pen.setColor(penColor)
        qp.setPen(pen)
        for x in range(0, 300, 30):
            qp.drawLine(x, 0, x, 600)
        for y in range(0, 600, 30):
            qp.drawLine(0, y, 300, y)

    def paintEvent(self, e):
        qp = QtGui.QPainter()
        qp.begin(self)
        self.drawGrid(qp)
        qp.end()

    def keyPressEvent(self, e):
        if e.key() == QtCore.Qt.Key_Space and self.enableKeyPress:
            if self.barCanRotate(self.currentBar.testRotate()):
                self.currentBar.rotate()

        if e.key() == QtCore.Qt.Key_Right and self.enableKeyPress:
            if self.barCanMoveToRight():
                self.currentBar.moveRight()
        if e.key() == QtCore.Qt.Key_Left and self.enableKeyPress:
            if self.barCanMoveToLeft():
                self.currentBar.moveLeft()

    def mousePressEvent(self, e):
        print e.pos().x(), e.pos().y()


def main():
    app = QtGui.QApplication(sys.argv)
    tetlis = Tetlis()
    sys.exit(app.exec_())

if __name__ == '__main__':
    main()
