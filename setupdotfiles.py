#!/usr/bin/env python
import os
import subprocess

def run_command(command):
    subprocess.run(command, shell=True, check=True)

def main():
    # Actualizar el sistema
    run_command("sudo pacman -Syu")

    # Instalar Yay
    run_command("git clone https://aur.archlinux.org/yay.git")
    run_command("cd yay && makepkg -si && cd .. && rm -rf yay")

    # Instalar dependencias para BSPWM, SXHKD, y otros paquetes
    run_command("yay -S bspwm sxhkd picom rofi feh TerminalEmulator")

    # Configurar el directorio de configuración para BSPWM y SXHKD
    os.makedirs(os.path.expanduser("~/.config/bspwm"), exist_ok=True)
    os.makedirs(os.path.expanduser("~/.config/sxhkd"), exist_ok=True)

    # Copiar archivos de configuración de BSPWM y SXHKD
    run_command("cp /usr/share/doc/bspwm/examples/bspwmrc ~/.config/bspwm/")
    run_command("cp ./config/sxhkd/sxhkdrc ~/.config/sxhkd/")  # Mover sxhkdrc de config a .config

    # Añadir la configuración para ejecutar el gestor de ventanas al inicio
    run_command('echo "exec bspwm" > ~/.xinitrc')

    # Dar permisos de ejecución a los archivos de configuración
    run_command('chmod +x ~/.config/bspwm/bspwmrc')
    run_command('chmod +x ~/.config/sxhkd/sxhkdrc')

    # Mover la carpeta eww a ~/.config/eww
    os.makedirs(os.path.expanduser("~/.config/eww"), exist_ok=True)
    run_command("cp ./config/eww/* ~/.config/eww/")

    # Mover la carpeta picom a ~/.config/picom
    os.makedirs(os.path.expanduser("~/.config/picom"), exist_ok=True)
    run_command("cp ./config/picom/picom.conf ~/.config/picom/")

    # Mover todos los fonts a /usr/share/fonts
    run_command("sudo cp ./fonts/* /usr/share/fonts/")

    # Iniciar eww y picom en el archivo de configuración de bspwm
    with open(os.path.expanduser("~/.config/bspwm/bspwmrc"), "a") as bspwmrc:
        bspwmrc.write("$HOME/.local/bin/eww -c $HOME/.config/eww/bar --restart open bar &\n")
        bspwmrc.write("picom --config $HOME/.config/picom/picom.conf &\n")
        bspwmrc.write("sxhkd &\n")

    # Iniciar sxhkd
    with open(os.path.expanduser("~/.xinitrc"), "a") as xinitrc:
        xinitrc.write("sxhkd &\n")

    # Mostrar mensaje de finalización
    print("Instalación completada. Reinicia tu sistema o ejecuta startx para iniciar BSPWM.")

if __name__ == "__main__":
    main()

