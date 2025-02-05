# pages/menu.py
from collections import deque
import pygame
from elements.button import ButtonManager, MenuButton
from elements.fps import draw_fps_curve
from pages import SceneBase

# 颜色常量
COLORS = {
    "gray_black": (12, 12, 18),
    "white": (250, 250, 254),
    "fps_curve": (100, 100, 100)
}

FONT_PATHS = {
    "geo": "assets/Geo-Regular.ttf",
    "pixel": "assets/fusion-pixel-10px-proportional-zh_hans.otf",
    "uni": "assets/unifont-16.0.01.otf"
}

SCREEN_SIZE = (800, 600)
FPS = 60

class Menu:
    def __init__(self):
        # 窗口初始化
        self.screen = pygame.display.set_mode(
            SCREEN_SIZE, 
            pygame.DOUBLEBUF | pygame.HWSURFACE
        )
        
        # 预加载字体
        self.fonts = {
            "title": pygame.freetype.Font(FONT_PATHS["geo"], 80),
            "version": pygame.freetype.Font(FONT_PATHS["geo"], 24),
            "fps": pygame.freetype.Font(FONT_PATHS["pixel"], 20),
            "button": pygame.freetype.Font(FONT_PATHS["pixel"], 18),
            "text": pygame.freetype.Font(FONT_PATHS["pixel"], 18)
        }
        
        # 游戏状态
        self.clock = pygame.time.Clock()
        self.fps_history = deque(maxlen=400)  # 限制历史记录长度
        self.running = True
        
        # UI 元素
        self.button_manager = ButtonManager()
        self.about_button_manager = ButtonManager()
        self._init_ui()
        self.about_window = False

    def _init_ui(self):
        """初始化界面元素"""
        self.button_params = {
            "normal_color": COLORS["gray_black"],
            "hover_color": COLORS["white"],
            "normal_fcolor": COLORS["white"],
            "hover_fcolor": COLORS["gray_black"],
            "font": FONT_PATHS["pixel"],
            "font_size": 18
        }
        
        buttons = [
            (30, 150, 280, 22, "开始游戏 | GameStart", lambda: print("GameStart")),
            (30, 180, 280, 22, "关于游戏 | About", lambda: setattr(self, 'about_window', True)),
            (30, 210, 280, 22, "退出游戏 | Quit", self.quit)
        ]
        
        for x, y, w, h, text, func in buttons:
            self.button_manager.add_button(
                MenuButton(x, y, w, h, **self.button_params, text=text, func=func)
            )
        self.about_button_manager.add_button(MenuButton(474, 400, 90, 22, **self.button_params, text="OK", func=lambda: setattr(self, 'about_window', False)))

    # 主游戏循环
    def _handle_events(self, event):
        if event.type == pygame.QUIT:
            self.quit()
            
        elif event.type in (pygame.MOUSEBUTTONDOWN, pygame.MOUSEMOTION):
            self.button_manager.handle_events(event, pygame.Rect(200, 140, 400, 300) if self.about_window else None)
            if self.about_window:
                self.about_button_manager.handle_events(event)
                
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                self.quit()

    # 主游戏循环
    def _update(self):
        self.fps_history.append(self.clock.get_fps())

    # 渲染界面
    def _render(self):
        def printf(t, text, x, y, style="text", color="white", fcolor=None):
            t.append((self.fonts[style].render(text, color, fcolor)[0], (x, y)))
        
        def drawf(t):
            for surface, pos in t:
                self.screen.blit(surface, pos)
        
        self.screen.fill((0, 0, 0))
        t = []
        printf(t, "CYANLE", 30, 30, "title")
        printf(t, "-REVIVAL-                v 0.2", 30, 85, "version")
        drawf(t)
        
        # draw_fps_curve(self.fps_history, SCREEN_SIZE, self.screen, COLORS["fps_curve"])
        self.button_manager.draw(self.screen)
        
        if self.about_window:
            self.screen.fill("white", (200, 140, 400, 300))
            self.screen.fill("black", (201, 141, 398, 298))
            t = []
            printf(t, "about", 220, 160)
            printf(t, "CYANLE -REVIVAL-", 220, 185)
            printf(t, "Made by Xnye", 220, 200)
            printf(t, "chatgpt怎么这么菜啊", 220, 215)
            drawf(t)
            self.about_button_manager.draw(self.screen)
        
        pygame.display.flip()

    def quit(self):
        pygame.quit()
        