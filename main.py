import sys
import tkinter as tk
from tkinter import messagebox

import pygame


class GameState:
    def __init__(self, surface):
        self.board = [['', '', ''],
                      ['', '', ''],
                      ['', '', '']]
        self.surface = surface
        self.turn = 'X'
        self.delta = self.surface.get_rect().width // len(self.board)
        self.font = pygame.font.Font('font/Pixeltype.ttf', 130)

    def draw(self):
        width = self.surface.get_rect().width

        x = y = 0
        for row in range(len(self.board)):
            for column in range(len(self.board)):
                # Draw the lines
                x += self.delta
                y += self.delta
                pygame.draw.line(self.surface, (64, 64, 64), (x, 0), (x, width), 3)
                pygame.draw.line(self.surface, (64, 64, 64), (0, y), (width, y), 3)
                text = self.board[row][column]
                color = (0, 0, 128) if text == 'O' else (64, 64, 64)
                text_surface = self.font.render(text, False, color)
                centerx, centery = (column * self.delta) + (self.delta // 2), (row * self.delta) + (self.delta // 2)
                text_rect = text_surface.get_rect(center=(centerx, centery))
                self.surface.blit(text_surface, text_rect)
        pygame.display.update()

    def move(self, posx, posy):
        col = (posx // self.delta)
        row = (posy // self.delta)
        if self.valid_move(row, col):
            self.board[row][col] = self.turn

            if self.check_win():
                self.draw()
                # pygame.display.update()
                message_box('Game over', 'Player {} wins'.format(self.turn))
                self.reset()
            else:
                self.turn = 'X' if self.turn == 'O' else 'O'

    def valid_move(self, row, col):
        return self.board[row][col] == ''

    def check_win(self):
        turn = self.turn

        # Check rows
        for col in range(len(self.board)):
            if self.board[0][col] == turn and self.board[1][col] == turn and self.board[2][col] == turn:
                return True
        # check columns
        for row in range(len(self.board)):
            if self.board[row][0] == turn and self.board[row][1] == turn and self.board[row][2] == turn:
                return True
        # check positive slope diagonal
        for i in range(len(self.board)):
            if self.board[0][0] == turn and self.board[1][1] == turn and self.board[2][2] == turn:
                return True
        # check positive slope diagonal
        for i in range(len(self.board)):
            if self.board[0][2] == turn and self.board[1][1] == turn and self.board[2][0] == turn:
                return True

    def reset(self):
        self.board = [['', '', ''],
                      ['', '', ''],
                      ['', '', '']]
        self.turn = 'X'
        pygame.display.update()


def message_box(subject, content):
    root = tk.Tk()
    root.attributes('-topmost', True)
    root.withdraw()
    messagebox.showinfo(subject, content)
    try:
        root.destroy()
    except:
        pass


def main():
    pygame.init()
    surface = pygame.display.set_mode((300, 300))
    pygame.display.set_caption('X/O By Biniam')
    gs = GameState(surface)

    # main game loop
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                gs.move(event.pos[0], event.pos[1])
        surface.fill((255, 255, 255))
        gs.draw()


main()
