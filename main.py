import pygame
import pyautogui
import math
import tkinter as tk
from tkinter import ttk, messagebox

class SlitherControllerApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Slither.io Controller")
        self.root.geometry("300x150")
        self.root.resizable(False, False)
        
        # Variáveis de controle
        self.running = False
        self.controller_active = False
        
        # Inicializa pygame
        pygame.init()
        pygame.joystick.init()
        
        # Verifica se há controles conectados
        self.joystick = None
        if pygame.joystick.get_count() > 0:
            self.joystick = pygame.joystick.Joystick(0)
            self.joystick.init()
        
        # Cria a interface
        self.create_main_interface()
        
        # Configurações
        self.DEADZONE = 0.2
        self.RADIUS = 50
        self.UPDATE_INTERVAL = 0.01
        
        # Mapeamento de botões
        self.BUTTON_A = 0
        self.BUTTON_RB = 5
        self.BUTTON_START = 7
        self.AXIS_RT = 5
        
        # Variáveis de estado
        self.prev_run_pressed = False
        
        # Centraliza o mouse inicialmente
        self.screen_width, self.screen_height = pyautogui.size()
        self.center_x = self.screen_width // 2
        self.center_y = self.screen_height // 2
        pyautogui.moveTo(self.center_x, self.center_y)
        
        # Inicia o loop principal
        self.root.protocol("WM_DELETE_WINDOW", self.on_close)
        self.root.mainloop()
    
    def create_main_interface(self):
        # Frame principal
        main_frame = ttk.Frame(self.root, padding="10")
        main_frame.pack(fill=tk.BOTH, expand=True)
        
        # Botão Iniciar/Parar
        self.start_button = ttk.Button(
            main_frame, 
            text="Iniciar", 
            command=self.toggle_controller,
            width=15
        )
        self.start_button.pack(pady=10)
        
        # Botão Controles (alterado de "Comandos")
        self.commands_button = ttk.Button(
            main_frame,
            text="Controles",
            command=self.show_commands,
            width=15
        )
        self.commands_button.pack(pady=10)
        
        # Status
        self.status_label = ttk.Label(
            main_frame,
            text="Pronto para iniciar",
            foreground="gray"
        )
        self.status_label.pack(pady=5)
    
    def create_commands_window(self):
        self.commands_window = tk.Toplevel(self.root)
        self.commands_window.title("Controles do Slither.io")  # Nome alterado
        self.commands_window.geometry("450x250")  # Altura aumentada para 300
        
        commands_text = """Controles do Xbox para Slither.io:

• L3 (Analógico esquerdo): Controla a direção da cobrinha
• RB, RT e Botão A: Aceleram a cobrinha
• Botão START: Para a captação dos controles

Instruções:
1. Clique em INICIAR ou pressione START no controle
2. Use o analógico para controlar a direção
3. Use RB/RT/A para acelerar
4. Pressione START novamente para parar"""
        
        commands_label = ttk.Label(
            self.commands_window,
            text=commands_text,
            justify=tk.LEFT,
            padding=10,
            font=('Arial', 10)
        )
        commands_label.pack(fill=tk.BOTH, expand=True)
        
        close_button = ttk.Button(
            self.commands_window,
            text="Fechar",
            command=self.commands_window.destroy
        )
        close_button.pack(pady=5)
        
        self.commands_window.protocol("WM_DELETE_WINDOW", self.commands_window.destroy)
    
    def show_commands(self):
        if not self.running:
            self.create_commands_window()
    
    def toggle_controller(self):
        if not self.controller_active:
            self.start_controller()
        else:
            self.stop_controller()
    
    def start_controller(self):
        if self.joystick is None:
            messagebox.showerror("Erro", "Nenhum controle Xbox encontrado!")
            return
        
        self.controller_active = True
        self.start_button.config(text="Parar")
        self.commands_button.config(state=tk.DISABLED)
        self.status_label.config(text="Captando controles...", foreground="green")
        self.running = True
        self.controller_loop()
    
    def stop_controller(self):
        self.controller_active = False
        self.running = False
        self.start_button.config(text="Iniciar")
        self.commands_button.config(state=tk.NORMAL)
        self.status_label.config(text="Pronto para iniciar", foreground="gray")
        pyautogui.keyUp('space')  # Garante que a tecla space seja liberada
    
    def controller_loop(self):
        if not self.running:
            return
        
        try:
            pygame.event.pump()
            
            # Verifica se o botão START foi pressionado
            if self.joystick.get_button(self.BUTTON_START):
                self.stop_controller()
                return
            
            # Movimento do mouse
            axis_x = self.joystick.get_axis(0)
            axis_y = self.joystick.get_axis(1)
            
            if abs(axis_x) < self.DEADZONE and abs(axis_y) < self.DEADZONE:
                axis_x = 0
                axis_y = 0
            
            if axis_x != 0 or axis_y != 0:
                angle = math.atan2(axis_y, axis_x)
                mouse_x = self.center_x + self.RADIUS * math.cos(angle)
                mouse_y = self.center_y + self.RADIUS * math.sin(angle)
                pyautogui.moveTo(mouse_x, mouse_y)
            
            # Botões para espaço
            r2_value = self.joystick.get_axis(self.AXIS_RT)
            r2_pressed = r2_value > 0.5
            a_pressed = self.joystick.get_button(self.BUTTON_A)
            rb_pressed = self.joystick.get_button(self.BUTTON_RB)

            run_pressed = r2_pressed or a_pressed or rb_pressed
            
            if (run_pressed) and not (self.prev_run_pressed):
                pyautogui.keyDown('space')
            elif not (run_pressed) and (self.prev_run_pressed):
                pyautogui.keyUp('space')
            
            self.prev_run_pressed = run_pressed
            
        except Exception as e:
            print(f"Erro: {e}")
            self.stop_controller()
        
        # Agenda a próxima execução
        if self.running:
            self.root.after(int(self.UPDATE_INTERVAL * 1000), self.controller_loop)
    
    def on_close(self):
        self.running = False
        if messagebox.askokcancel("Sair", "Deseja realmente sair do Slither.io Controller?"):
            pygame.quit()
            self.root.destroy()

if __name__ == "__main__":
    root = tk.Tk()
    app = SlitherControllerApp(root)