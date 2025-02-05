# pages/__init__.py
import pygame

class SceneBase:
    def __init__(self):
        self.next_scene = self  # 默认不切换场景
    
    def handle_events(self, event):
        """处理事件（需子类实现）"""
        pass
    
    def update(self):
        """更新逻辑（需子类实现）"""
        pass
    
    def draw(self, screen):
        """渲染界面（需子类实现）"""
        pass
