import pygame
import pyautogui
import time
import sys
import math

# Inicializa o pygame para leitura do controle
pygame.init()
pygame.joystick.init()

# Configurações
DEADZONE = 0.2  # Zona morta para evitar drift do analógico
RADIUS = 50  # Raio da circunferência em pixels
UPDATE_INTERVAL = 0.001  # Intervalo de atualização em segundos

# Mapeamento de botões do controle Xbox
BUTTON_A = 0
BUTTON_RB = 5
BUTTON_START = 7
AXIS_RT = 5

try:
    # Verifica se há controles conectados
    if pygame.joystick.get_count() == 0:
        print("Nenhum controle encontrado. Conecte um controle Xbox e tente novamente.")
        sys.exit()
    
    # Inicializa o primeiro controle encontrado
    joystick = pygame.joystick.Joystick(0)
    joystick.init()
    
    print(f"Controle conectado: {joystick.get_name()}")
    print("Pressione o botão START (Menu) para encerrar o programa.")
    print(f"Mouse limitado a uma circunferência de {RADIUS}px ao redor do centro da tela.")
    
    # Obtém as dimensões da tela
    screen_width, screen_height = pyautogui.size()
    center_x = screen_width // 2
    center_y = screen_height // 2
    
    # Move o mouse para o centro inicialmente
    pyautogui.moveTo(center_x, center_y)
    
    # Variáveis de estado
    prev_r2_pressed = False
    prev_r1_pressed = False
    prev_a_pressed = False
    
    running = True
    while running:
        pygame.event.pump()
        
        # Verifica se o botão START (Menu) foi pressionado para sair
        if joystick.get_button(BUTTON_START):
            running = False
        
        # Obtém os eixos do analógico esquerdo (L3)
        axis_x = joystick.get_axis(0)
        axis_y = joystick.get_axis(1)
        
        # Aplica deadzone
        if abs(axis_x) < DEADZONE and abs(axis_y) < DEADZONE:
            axis_x = 0
            axis_y = 0
        
        # Se o analógico está sendo movido
        if axis_x != 0 or axis_y != 0:
            # Calcula o ângulo da direção do analógico
            angle = math.atan2(axis_y, axis_x)
            
            # Calcula a posição na circunferência
            mouse_x = center_x + RADIUS * math.cos(angle)
            mouse_y = center_y + RADIUS * math.sin(angle)
            
            # Move o mouse para a posição calculada
            pyautogui.moveTo(mouse_x, mouse_y)
        
        # Verifica os botões R2, R1 e A
        r2_value = joystick.get_axis(AXIS_RT)
        r2_pressed = r2_value > 0.5
        
        r1_pressed = joystick.get_button(BUTTON_RB)
        a_pressed = joystick.get_button(BUTTON_A)
        
        # R2 pressionado - barra de espaço
        if r2_pressed and not prev_r2_pressed:
            pyautogui.keyDown('space')
        elif not r2_pressed and prev_r2_pressed:
            pyautogui.keyUp('space')
        
        # R1 pressionado - barra de espaço
        if r1_pressed and not prev_r1_pressed:
            pyautogui.keyDown('space')
        elif not r1_pressed and prev_r1_pressed:
            pyautogui.keyUp('space')
        
        # A pressionado - barra de espaço
        if a_pressed and not prev_a_pressed:
            pyautogui.keyDown('space')
        elif not a_pressed and prev_a_pressed:
            pyautogui.keyUp('space')
        
        # Atualiza os estados anteriores
        prev_r2_pressed = r2_pressed
        prev_r1_pressed = r1_pressed
        prev_a_pressed = a_pressed
        
        time.sleep(UPDATE_INTERVAL)

except Exception as e:
    print(f"Ocorreu um erro: {e}")
finally:
    pygame.quit()
    print("Programa encerrado.")