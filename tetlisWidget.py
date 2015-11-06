# -*- coding: utf-8 -*-
from PyQt4 import QtGui, QtCore
import sys
import copy
import numpy as np

class BaseBlock(QtGui.QWidget):
    def __init__(self, parent = None):
        super(BaseBlock, self).__init__(parent)

        #ブロックの位置
        self._postionX = 0
        self._postionY = 0

        #ブロックの位置ベクトル
        self._postionVector = np.array([0,0])

        #描画色
        self._blockColor = QtGui.QColor(0, 0, 0)

        #ブロックサイズ
        self.setFixedSize(30, 30)
        self.show()

    def paintEvent(self, e):
        painter = QtGui.QPainter()
        painter.begin(self)
        self.brushBlock(painter)
        self.update()
        painter.end()

    def brushBlock(self, painter):
        painter.setBrush(self._blockColor)
        painter.drawRect(0, 0, 30, 30)

    def setBlockColor(self, color):
        self._blockColor = color

    def setPostion(self, x, y):
        self._postionX = x
        self._postionY = y

    def getPostionX(self):
        return self._postionX

    def getPostionY(self):
        return self._postionY

    def setVector(self, x, y):
        self._postionVector = np.array([x, y])

    def getVector(self):
        return self._postionVector

class TBlock(BaseBlock):
    def __init__(self, parent = None):
        super(TBlock, self).__init__(parent)
        self._blockColor = QtGui.QColor(195, 81, 143)

class KeyBlock1(BaseBlock):
    def __init__(self, parent = None):
        super(KeyBlock1, self).__init__(parent)
        self._blockColor = QtGui.QColor(131, 180, 150)

class KeyBlock2(BaseBlock):
    def __init__(self, parent = None):
        super(KeyBlock2, self).__init__(parent)
        self._blockColor = QtGui.QColor(151, 0, 50)

class LBlock1(BaseBlock):
    def __init__(self, parent = None):
        super(LBlock1, self).__init__(parent)
        self._blockColor = QtGui.QColor(0, 122, 153)

class LBlock2(BaseBlock):
    def __init__(self, parent = None):
        super(LBlock2, self).__init__(parent)
        self._blockColor = QtGui.QColor(203, 58, 17)

class RectBlock(BaseBlock):
    def __init__(self, parent = None):
        super(RectBlock, self).__init__(parent)
        self._blockColor = QtGui.QColor(236, 208, 0)

class TetlisBlock(BaseBlock):
    def __init__(self, parent = None):
        super(TetlisBlock, self).__init__(parent)
        self._blockColor = QtGui.QColor(159, 204, 215)

class BaseBar(QtGui.QWidget):
    def __init__(self, parent = None):
        super(BaseBar, self).__init__(parent)

        #オブジェクトナンバー
        #self._myNumber = 0

        #バーのポジション
        self._barPostionX = 0
        self._barPostionY = 0

        #回転行列
        self.rotateMatrix = np.matrix((
            (0, -1),
            (1, 0)
        ))

        #ブロックを入れるリスト
        self.blockList = []

        #座標変換用定数
        self._offsetX = 0
        self._offsetY = 0

        #速度定数
        self._speed = 5

    def setBarPostion(self, x, y):
        if x >= 0 and y >= 0:
            self._barPostionX = x
            self._barPostionY = y

    def setOffset(self, x, y):
        self._offsetX = x
        self._offsetY = y

    def setSpeed(self, speed):
        if speed > 0:
            self._speed = speed

    def getBarPostionX(self):
        return self._barPostionX

    def getBarPostionY(self):
        return self._barPostionY

    def getMyNumber(self):
        return self._myNumber

    def blockPostionUpdate( self):
        for block in self.blockList:
            vector = block.getVector()
            x = vector[0] * 30
            y = vector[1] * 30
            block.setPostion(x + self._barPostionX, y + self._barPostionY)
            block.move(x - self._offsetX, y - self._offsetY)

    def deleteBlock(self, block):
        block.hide()
        self.blockList.remove(block)
        print self.blockList
        if len(self.blockList) == 0:
            return True
        else:
            return False

    def downBar(self):
        x = self.getBarPostionX()
        y = self.getBarPostionY() + self._speed
        self.setBarPostion(x, y)
        self.blockPostionUpdate()
        self.move(x, y)

    def rotate(self):
        for block in self.blockList:
            newMatrix = np.dot(self.rotateMatrix, block.getVector())
            block.setVector(newMatrix[0,0], newMatrix[0,1])
        else:
            self.blockPostionUpdate()

    def moveRight(self):
        self._barPostionX = self._barPostionX + 30
        self.blockPostionUpdate()
        self.move(self._barPostionX, self._barPostionY)

    def moveLeft(self):
        self._barPostionX = self._barPostionX - 30
        self.blockPostionUpdate()
        self.move(self._barPostionX, self._barPostionY)

    #メイン画面の座標と、ウィジェットの座標変換
    def move(self, x, y):
        """
        オーバーライド
        """
        super(BaseBar, self).move(x + self._offsetX, y + self._offsetY)

    def isInWindow(self, maxX, maxY, minX, minY):
        for block in self.blockList:
            x = block.getPostionX()
            y = block.getPostionY()
            if x >  maxX or y >=  maxY or x <  minX or y <  minY:
                return False
        else:
            return True

    def testRotate(self):
        copyList = copy.deepcopy(self.blockList)
        for block in copyList:
            newMatrix = np.dot(self.rotateMatrix, block.getVector())
            block.setVector(newMatrix[0,0], newMatrix[0,1])
        else:
            return copyList

class TBar(BaseBar):
    def __init__(self, parent = None, x = 120, y = 0):
        super(TBar, self).__init__(parent)
        self._barPostionX = x
        self._barPostionY = y
        self.setFixedSize(90, 90)
        self.show()

        #座標変換用の定数の設定
        self.setOffset(-30, -30)
        self.move(self._barPostionX, self._barPostionY)

        #ブロックの初期化
        self.block1 = TBlock(self)
        self.block2 = TBlock(self)
        self.block3 = TBlock(self)
        self.block4 = TBlock(self)

        #位置ベクトの初期化
        """
         2
        314
        実際には上下逆
        """
        self.block1.setVector(0, 0)
        self.block2.setVector(0, 1)
        self.block3.setVector(-1, 0)
        self.block4.setVector(1, 0)

        #1を軸に設定
        self.block1.setPostion(self.getBarPostionX(), self.getBarPostionY())

        #ブロックをリストへ追加
        self.blockList = [self.block1, self.block2, self.block3, self.block4]

        self.blockPostionUpdate()

class KeyBar1(BaseBar):
    def __init__(self, parent = None, x = 120, y = 0):
        super(KeyBar1, self).__init__(parent)
        self._barPostionX = x
        self._barPostionY = y
        self.setFixedSize(90, 90)
        self.show()

        #座標変換用の定数の設定
        self.setOffset(-30, -30)
        self.move(self._barPostionX, self._barPostionY)

        #ブロックの初期化
        self.block1 = KeyBlock1(self)
        self.block2 = KeyBlock1(self)
        self.block3 = KeyBlock1(self)
        self.block4 = KeyBlock1(self)

        #位置ベクトの初期化
        """
         24
        31
        実際には上下逆
        """
        self.block1.setVector(0, 0)
        self.block2.setVector(0, 1)
        self.block3.setVector(-1, 0)
        self.block4.setVector(1, 1)

        #1を軸に設定
        self.block1.setPostion(self.getBarPostionX(), self.getBarPostionY())

        #ブロックをリストへ追加
        self.blockList = [self.block1, self.block2, self.block3, self.block4]

        self.blockPostionUpdate()

class KeyBar2(BaseBar):
    def __init__(self, parent = None, x = 120, y = 0):
        super(KeyBar2, self).__init__(parent)
        self._barPostionX = x
        self._barPostionY = y
        self.setFixedSize(90, 90)
        self.show()

        #座標変換用の定数の設定
        self.setOffset(-30, -30)
        self.move(self._barPostionX, self._barPostionY)

        #ブロックの初期化
        self.block1 = KeyBlock2(self)
        self.block2 = KeyBlock2(self)
        self.block3 = KeyBlock2(self)
        self.block4 = KeyBlock2(self)

        #位置ベクトの初期化
        """
        32
         14
        実際には上下逆
        """
        self.block1.setVector(0, 0)
        self.block2.setVector(0, 1)
        self.block3.setVector(-1, 1)
        self.block4.setVector(1, 0)

        #1を軸に設定
        self.block1.setPostion(self.getBarPostionX(), self.getBarPostionY())

        #ブロックをリストへ追加
        self.blockList = [self.block1, self.block2, self.block3, self.block4]

        self.blockPostionUpdate()

class LBar1(BaseBar):
    def __init__(self, parent = None, x = 120, y = 0):
        super(LBar1, self).__init__(parent)
        self._barPostionX = x
        self._barPostionY = y
        self.setFixedSize(90, 90)
        self.show()

        #座標変換用の定数の設定
        self.setOffset(-30, -30)
        self.move(self._barPostionX, self._barPostionY)

        #ブロックの初期化
        self.block1 = LBlock1(self)
        self.block2 = LBlock1(self)
        self.block3 = LBlock1(self)
        self.block4 = LBlock1(self)

        #位置ベクトの初期化
        """
        4
        213
        実際には上下逆
        """
        self.block1.setVector(0, 0)
        self.block2.setVector(-1, 0)
        self.block3.setVector(1, 0)
        self.block4.setVector(-1, 1)

        #1を軸に設定
        self.block1.setPostion(self.getBarPostionX(), self.getBarPostionY())

        #ブロックをリストへ追加
        self.blockList = [self.block1, self.block2, self.block3, self.block4]

        self.blockPostionUpdate()

class LBar2(BaseBar):
    def __init__(self, parent = None, x = 120, y = 0):
        super(LBar2, self).__init__(parent)
        self._barPostionX = x
        self._barPostionY = y
        self.setFixedSize(90, 90)
        self.show()

        #座標変換用の定数の設定
        self.setOffset(-30, -30)
        self.move(self._barPostionX, self._barPostionY)

        #ブロックの初期化
        self.block1 = LBlock2(self)
        self.block2 = LBlock2(self)
        self.block3 = LBlock2(self)
        self.block4 = LBlock2(self)

        #位置ベクトの初期化
        """
          4
        213
        実際には上下逆
        """
        self.block1.setVector(0, 0)
        self.block2.setVector(-1, 0)
        self.block3.setVector(1, 0)
        self.block4.setVector(1, 1)

        #1を軸に設定
        self.block1.setPostion(self.getBarPostionX(), self.getBarPostionY())

        #ブロックをリストへ追加
        self.blockList = [self.block1, self.block2, self.block3, self.block4]

        self.blockPostionUpdate()

class RectBar(BaseBar):
    def __init__(self, parent = None, x = 120, y = 0):
        super(RectBar, self).__init__(parent)
        self._barPostionX = x
        self._barPostionY = y
        self.setFixedSize(90, 90)
        self.show()

        #座標変換用の定数の設定
        self.setOffset(-30, -30)
        self.move(self._barPostionX, self._barPostionY)

        #ブロックの初期化
        self.block1 = RectBlock(self)
        self.block2 = RectBlock(self)
        self.block3 = RectBlock(self)
        self.block4 = RectBlock(self)

        #位置ベクトの初期化
        """
        43
        21
        実際には上下逆
        """
        self.block1.setVector(0, 0)
        self.block2.setVector(-1, 0)
        self.block3.setVector(0, 1)
        self.block4.setVector(-1, 1)

        #1を軸に設定
        self.block1.setPostion(self.getBarPostionX(), self.getBarPostionY())

        #ブロックをリストへ追加
        self.blockList = [self.block1, self.block2, self.block3, self.block4]

        self.blockPostionUpdate()

    def rotate(self):
        """
        オーバーライド
        """
        pass

class TetlisBar(BaseBar):
    def __init__(self, parent = None, x = 120, y = 0):
        super(TetlisBar, self).__init__(parent)
        self._barPostionX = x
        self._barPostionY = y
        self.setFixedSize(150, 150)
        self.show()

        #座標変換用の定数の設定
        self.setOffset(-60, -60)
        self.move(self._barPostionX, self._barPostionY)

        #ブロックの初期化
        self.block1 = TetlisBlock(self)
        self.block2 = TetlisBlock(self)
        self.block3 = TetlisBlock(self)
        self.block4 = TetlisBlock(self)

        #位置ベクトの初期化
        """
        4213
        実際には上下逆
        """
        self.block1.setVector(0, 0)
        self.block2.setVector(-1, 0)
        self.block3.setVector(1, 0)
        self.block4.setVector(-2, 0)

        #1を軸に設定
        self.block1.setPostion(self.getBarPostionX(), self.getBarPostionY())

        #ブロックをリストへ追加
        self.blockList = [self.block1, self.block2, self.block3, self.block4]

        self.blockPostionUpdate()

def main():
    app = QtGui.QApplication(sys.argv)
    t = TBar()
    sys.exit(app.exec_())

if __name__ == '__main__':
    main()
