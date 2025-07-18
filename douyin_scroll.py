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
    def __init__(self, debug_mode=False):
        self.mouse_controller = mouse.Controller()
        self.keyboard_listener = None
        self.is_running = False
        self.scroll_amount = 3  # 滚动的幅度，可以调整
        self.debug_mode = debug_mode  # 调试模式开关
        self.ctrl_pressed = False  # 跟踪Ctrl键状态
        
    def on_key_press(self, key):
        """处理键盘按键事件"""
        try:
            # 添加调试信息
            if self.debug_mode:
                print(f"🔍 按键检测: {key}")
            
            # 跟踪Ctrl键状态
            if key == Key.ctrl_l or key == Key.ctrl_r:
                self.ctrl_pressed = True
                if self.debug_mode:
                    print("🔵 Ctrl键已按下")
            
            # 检查是否是方向键下键
            if key == Key.down:
                print("⬇️ 检测到方向键下键，开始滚动...")
                self.scroll_down()
            
            # 检查Ctrl+Q组合键
            elif hasattr(key, 'char') and key.char == 'q' and self.ctrl_pressed:
                print("👋 检测到Ctrl+Q组合键，程序退出")
                self.stop()
                return False
                
        except AttributeError:
            # 某些键可能没有相应的属性
            if self.debug_mode:
                print(f"⚠️ 未知按键: {key}")
            pass
        except Exception as e:
            print(f"❌ 按键处理异常: {e}")
            
    def on_key_release(self, key):
        """处理键盘释放事件"""
        try:
            # 添加调试信息
            if self.debug_mode:
                print(f"🔍 释放键检测: {key}")
            
            # 重置Ctrl键状态
            if key == Key.ctrl_l or key == Key.ctrl_r:
                self.ctrl_pressed = False
                if self.debug_mode:
                    print("🔴 Ctrl键已释放")
                
        except AttributeError:
            if self.debug_mode:
                print(f"⚠️ 未知释放键: {key}")
            pass
        except Exception as e:
            print(f"❌ 释放键处理异常: {e}")
            # 如果这里出现异常，也不要让程序崩溃
            pass
            
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
        print("   • 按下 Ctrl+Q 组合键退出程序")
        print("   • 请确保目标窗口处于活动状态")
        if self.debug_mode:
            print("   • 调试模式：会显示所有按键信息")
        print("⏳ 等待按键...")
        
        self.is_running = True
        
        try:
            # 创建键盘监听器
            self.keyboard_listener = keyboard.Listener(
                on_press=self.on_key_press,
                on_release=self.on_key_release
            )
            
            # 启动监听器
            self.keyboard_listener.start()
            print("✅ 键盘监听器启动成功")
            
            # 保持程序运行
            while self.is_running:
                time.sleep(0.1)
                
        except KeyboardInterrupt:
            print("⚠️ 检测到Ctrl+C，程序退出")
            self.stop()
        except Exception as e:
            print(f"❌ 键盘监听器启动失败: {e}")
            print("💡 可能的解决方案：")
            print("   • 以管理员身份运行程序")
            print("   • 检查是否有其他程序占用键盘监听")
            print("   • 重新安装pynput: pip install --upgrade pynput")
            self.stop()
            
    def reset_keyboard_state(self):
        """重置键盘状态"""
        self.ctrl_pressed = False
        if self.debug_mode:
            print("🔄 键盘状态已重置")
            
    def stop(self):
        """停止程序"""
        print("🛑 正在停止程序...")
        self.is_running = False
        self.reset_keyboard_state()  # 重置键盘状态
        if self.keyboard_listener:
            try:
                self.keyboard_listener.stop()
                print("✅ 键盘监听器已停止")
            except Exception as e:
                print(f"⚠️ 停止键盘监听器时出错: {e}")
            
    def set_scroll_amount(self, amount):
        """设置滚动幅度"""
        self.scroll_amount = amount
        print(f"📏 滚动幅度已设置为: {amount}")


def main():
    """主函数"""
    print("🎯 抖音滚动助手配置")
    print("💡 提示：程序启动后，使用 Ctrl+Q 组合键退出程序")
    print("是否开启调试模式？(显示所有按键信息)")
    debug_choice = input("输入 y 开启调试模式，其他任意键关闭: ").strip().lower()
    debug_mode = debug_choice == 'y'
    
    controller = DouyinScrollController(debug_mode=debug_mode)
    
    # 可以在这里调整滚动幅度
    # controller.set_scroll_amount(5)  # 增加滚动幅度
    
    try:
        controller.start()
    except Exception as e:
        print(f"❌ 程序启动失败: {e}")
        print("💡 请确保已安装所需依赖: pip install pynput")


if __name__ == "__main__":
    main() 