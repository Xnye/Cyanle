import pygame
import pygame.freetype

class MenuButton:
    def __init__(self, x, y, width, height, 
                 normal_color, hover_color,
                 normal_fcolor, hover_fcolor,
                 text, func, font, font_size, type = None):
        # 几何属性
        self.rect = pygame.Rect(x, y, width, height)
        self.base_width = width
        
        # 颜色属性
        self.color_states = {
            "normal": (normal_color, normal_fcolor),
            "hover": (hover_color, hover_fcolor)
        }
        
        # 功能属性
        self.text = text
        self.func = func
        self.type = type
        
        # 状态属性
        self.current_state = "normal"
        self.delta_x = 0  # 动态宽度变化量
        
        # 字体处理
        self.font = pygame.freetype.Font(font, font_size)
        self.cached_surfaces = {
            "normal": self._render_text(*self.color_states["normal"]),
            "hover": self._render_text(*self.color_states["hover"])
        }

    def _render_text(self, bg_color, fg_color):
        """预渲染文本表面"""
        return self.font.render(self.text, fgcolor=fg_color, bgcolor=bg_color)[0]

    def handle_event(self, event, disabled_rect = None):
        """优化后的事件处理"""
        mouse_pos = pygame.mouse.get_pos()
        
        if not disabled_rect:
            is_hovered = self.rect.collidepoint(mouse_pos)
        else:
            is_hovered = self.rect.collidepoint(mouse_pos) and not disabled_rect.collidepoint(mouse_pos)
        
        # 状态更新
        self.current_state = "hover" if is_hovered else "normal"
        
        # 处理点击
        if event.type == pygame.MOUSEBUTTONDOWN and is_hovered:
            self.func()

    def draw(self, surface):
        """优化后的渲染方法"""
        current_rect = self.rect.copy()
        current_rect.width = self.base_width + self.delta_x
        
        # 绘制背景
        pygame.draw.rect(
            surface, 
            self.color_states[self.current_state][0], 
            current_rect
        )
        
        # 动态宽度动画
        if self.current_state == "hover":
            self.delta_x = min(self.delta_x + 8 / (1 + self.delta_x / 3), 20)
        else:
            self.delta_x = max(self.delta_x * 0.85, 0)
        
        # 绘制文本（使用预渲染表面）
        text_surface = self.cached_surfaces[self.current_state]
        text_rect = text_surface.get_rect(center=current_rect.center)
        surface.blit(text_surface, text_rect)

class ButtonManager:
    def __init__(self):
        self.buttons = []
        
    def add_button(self, button):
        self.buttons.append(button)
        
    def handle_events(self, event, disabled_rect = None):
        if event.type in (pygame.MOUSEBUTTONDOWN, pygame.MOUSEMOTION):
            for button in self.buttons:
                button.handle_event(event, disabled_rect)
                
    def draw(self, surface):
        for button in self.buttons:
            button.draw(surface)
            
    def delete_type(self, type):
        self.buttons = [button for button in self.buttons if button.type != type]