#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
抖音滚动助手 - 通过多媒体键控制鼠标滚轮
按下"下一曲"键时，模拟鼠标中键向下滑动
"""

import time
import threading
from pynput import keyboard, mouse
from pynput.keyboard import Key


class DouyinScrollController:
    def __init__(self):
        self.mouse_controller = mouse.Controller()
        self.keyboard_listener = None
        self.is_running = False
        self.scroll_amount = 3  # 滚动的幅度，可以调整
        
    def on_key_press(self, key):
        """处理键盘按键事件"""
        try:
            # 检查是否是方向键下键
            if key == Key.down:
                print("⬇️ 检测到方向键下键，开始滚动...")
                self.scroll_down()
                
        except AttributeError:
            # 某些键可能没有相应的属性
            pass
            
    def on_key_release(self, key):
        """处理键盘释放事件"""
        # 按ESC键退出程序
        if key == Key.esc:
            print("👋 程序退出")
            self.stop()
            return False
            
    def scroll_down(self):
        """模拟鼠标中键向下滚动"""
        try:
            # 模拟鼠标滚轮向下滚动
            self.mouse_controller.scroll(0, -self.scroll_amount)
            print(f"⬇️ 向下滚动 {self.scroll_amount} 单位")
        except Exception as e:
            print(f"❌ 滚动失败: {e}")
            
    def start(self):
        """启动键盘监听"""
        print("🚀 抖音滚动助手已启动")
        print("📝 使用说明：")
        print("   • 按下键盘的'方向键下键' (↓) 来向下滚动")
        print("   • 按下 ESC 键退出程序")
        print("   • 请确保目标窗口处于活动状态")
        print("⏳ 等待按键...")
        
        self.is_running = True
        
        # 创建键盘监听器
        self.keyboard_listener = keyboard.Listener(
            on_press=self.on_key_press,
            on_release=self.on_key_release
        )
        
        # 启动监听器
        self.keyboard_listener.start()
        
        # 保持程序运行
        try:
            while self.is_running:
                time.sleep(0.1)
        except KeyboardInterrupt:
            self.stop()
            
    def stop(self):
        """停止程序"""
        self.is_running = False
        if self.keyboard_listener:
            self.keyboard_listener.stop()
            
    def set_scroll_amount(self, amount):
        """设置滚动幅度"""
        self.scroll_amount = amount
        print(f"📏 滚动幅度已设置为: {amount}")


def main():
    """主函数"""
    controller = DouyinScrollController()
    
    # 可以在这里调整滚动幅度
    # controller.set_scroll_amount(5)  # 增加滚动幅度
    
    try:
        controller.start()
    except Exception as e:
        print(f"❌ 程序启动失败: {e}")
        print("💡 请确保已安装所需依赖: pip install pynput")


if __name__ == "__main__":
    main() 