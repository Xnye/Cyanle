# main.py
import pygame
from pages.menu import Menu

class Game:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((800, 600))
        pygame.display.set_caption("CYANLE -REVIVAL- v0.2")
        self.scenes = {
            "menu": Menu,
        }
        self.current_scene = None
        self.switch_scene("menu")  # 初始场景为主菜单

    def switch_scene(self, scene_name):
        """切换场景的核心方法"""
        scene_class = self.scenes.get(scene_name)
        if scene_class:
            self.current_scene = scene_class()

    def run(self):
        clock = pygame.time.Clock()
        running = True
        while running:
            # 处理事件
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                if self.current_scene:
                    self.current_scene._handle_events(event)

            # 更新和渲染当前场景
            if self.current_scene:
                self.current_scene._update()
                self.current_scene._render()

            clock.tick(60)

        pygame.quit()

if __name__ == "__main__":
    game = Game()
    game.run()