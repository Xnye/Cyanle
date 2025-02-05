import pygame

def draw_fps_curve(fps_history, SCREEN_SIZE, screen, color):
        if len(fps_history) < 2:
            return

        # 动态调整垂直范围
        valid_fps = [fps for fps in fps_history if fps > 0]
        min_fps = min(valid_fps) if valid_fps else 0
        max_fps = max(valid_fps) if valid_fps else 60
        height_range = max_fps - min_fps or 1  # 避免除零错误

        points = [
            (
                int((i / len(fps_history)) * SCREEN_SIZE[0]),
                int(SCREEN_SIZE[1] - (fps - min_fps) / height_range * (SCREEN_SIZE[1] - 50))
            )
            for i, fps in enumerate(fps_history)
        ]

        if len(points) >= 2:
            pygame.draw.lines(screen, color, False, points, 2)