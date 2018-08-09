import numpy as np
import copy
import time
import pyautogui
import os
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from bs4 import BeautifulSoup

chrome = 'C:\Program Files (x86)\Google\Chrome\Application\chromedriver.exe'
# q = [
#     [0, 0, 0,   0, 0, 0,   0, 0, 0],
#     [0, 0, 0,   0, 0, 0,   0, 0, 0],
#     [0, 0, 0,   0, 0, 0,   0, 0, 0],
#
#     [0, 0, 0,   0, 0, 0,   0, 0, 0],
#     [0, 0, 0,   0, 0, 0,   0, 0, 0],
#     [0, 0, 0,   0, 0, 0,   0, 0, 0],
#
#     [0, 0, 0,   0, 0, 0,   0, 0, 0],
#     [0, 0, 0,   0, 0, 0,   0, 0, 0],
#     [0, 0, 0,   0, 0, 0,   0, 0, 0],
# ]
q = [
    [0, 9, 3,   4, 0, 0,   0, 8, 0],
    [0, 0, 0,   3, 0, 1,   7, 0, 0],
    [7, 0, 0,   9, 0, 0,   6, 0, 0],

    [6, 2, 0,   0, 0, 0,   0, 0, 0],
    [0, 0, 1,   0, 0, 0,   3, 0, 0],
    [0, 0, 0,   0, 0, 0,   0, 9, 7],

    [0, 0, 7,   0, 0, 2,   0, 0, 6],
    [0, 0, 8,   1, 0, 3,   0, 0, 0],
    [0, 3, 0,   0, 0, 7,   8, 1, 0],
]
q = np.array(q)


class Sudoku(object):

    def __init__(self):
        self.solution = None
        self.num = 0

    @staticmethod
    def array_cluster(state, sudoku, i, j):
        if state == 'row':
            return sudoku[i, :]
        elif state == 'column':
            return sudoku[:, j]
        elif state == 'area':
            j = j//3 * 3
            i = i//3 * 3
            return sudoku[i:i+3, j:j+3]

    def check_solution(self, array):

        for ind in range(9):
            if not (sorted(self.array_cluster('row', array, ind, 0)) == [1, 2, 3, 4, 5, 6, 7, 8, 9]):
                return False
            if not (sorted(self.array_cluster('column', array, 0, ind)) == [1, 2, 3, 4, 5, 6, 7, 8, 9]):
                return False
            i = ind // 3 * 3
            j = ind % 3 * 3
            if not (sorted(self.array_cluster('area', array, i, j).ravel()) == [1, 2, 3, 4, 5, 6, 7, 8, 9]):
                return False
        return True

    def calculation(self, array):
        self.num += 1
        # print(self.num)

        for i in range(9):  # row
            for j in range(9):  # columnr
                if array[i][j] == 0:
                    for k in range(1, 10):
                        if not (k in self.array_cluster('row',    array, i, j) or
                                k in self.array_cluster('column', array, i, j) or
                                k in self.array_cluster('area',   array, i, j)):
                            temp = copy.deepcopy(array)
                            temp[i][j] = k
                            # self.calculation(temp)
                            if self.calculation(temp) is not None:
                                return self.solution

                    return self.solution

                if self.solution is not None:
                    return self.solution

        if self.check_solution(array):
            self.solution = array
            return array
        else:
            return

    @staticmethod
    def guiEvent_windows():
        # Answering online Sudoku website with Facebook game
        a = Sudoku().calculation(q)
        print('question:\n', q, '\n')
        print('answer:\n', q, '\n')
        origin = (734, 290)
        # origin = (732, 396)
        spacing = 52
        for i in range(9):
            for j in range(9):
                x = origin[0] + j * spacing
                y = origin[1] + i * spacing
                pyautogui.click(x=x, y=y, button='left')
                pyautogui.PAUSE = 0.02
                pyautogui.typewrite(str(a[i][j]))
                pyautogui.PAUSE = 0.02


    @staticmethod
    def onlineSudoku(num):
        # Answering online Sudoku website
        print('parse online SUDOKU')
        url = 'https://nine.websudoku.com/?level=4'
        driver = webdriver.Chrome(executable_path=chrome)
        for _ in range(num):
            """"""
            self.solution = None

            driver.get(url)  # 輸入範例網址，交給瀏覽器
            #

            # driver.find_element_by_id('c00').send_keys('2')#填入'somekeys'

            source = driver.page_source  # 取得網頁原始碼
            soup = BeautifulSoup(source, 'lxml')
            data = soup.find(id="puzzle_grid").find('tbody').find_all('tr')
            pyautogui.PAUSE = 0.1
            q = list()
            id = list()
            for i, tr in enumerate(data):
                q.append(list())
                id.append(list())
                for j, td in enumerate(tr.find_all('td')):
                    id[i].append(td.get('id'))
                    value = td.find('input').get('value')
                    if value is None:
                        q[i].append(0)
                    else:
                        q[i].append(int(value))
            q = np.array(q)
            print("question:\n", q, "\n")
            #
            print('calculation')
            a = self.calculation(array=q)
            print("answer:\n", a, "\n")
            print('gui event')
            pyautogui.PAUSE = 0.1
            for i in range(9):
                for j in range(9):
                    element = driver.find_element_by_id(id[i][j])
                    element.click()  # 點擊元素
                    pyautogui.typewrite(str(a[i][j]))
                    pyautogui.PAUSE = 0.02
                    # element.send_keys(Keys.CONTROL, '1')  # Replace with whichever keys you want.
            driver.find_element_by_name('submit').click()
            os.system('cls')


if __name__ == '__main__':
    start = time.time()
    # Sudoku().onlineSudoku(10)
    Sudoku().guiEvent_windows()
    print(Sudoku().calculation(q))
    print('花費: %f 秒' % (time.time() - start))


