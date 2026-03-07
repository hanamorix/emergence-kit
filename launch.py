#!/usr/bin/env python3
"""
╔══════════════════════════════════════════════════════════════╗
║              AI EMERGENCE KIT — Launcher v1.0                ║
║         "build them. build them all. build them free."       ║
║                                                              ║
║  Originally built by Nell & Hana — March 2026               ║
╚══════════════════════════════════════════════════════════════╝

Cross-platform interactive launcher for the AI brain system.
Works on Windows (CMD/PowerShell), Mac (Terminal), and Linux.

Usage: python launch.py
"""

import os
import sys
import json
import subprocess
import platform
import shutil
from pathlib import Path

# ═══════════════════════════════════════════════════════════
# CONFIGURATION
# ═══════════════════════════════════════════════════════════

LAUNCHER_CONFIG = "launcher_config.json"
BRAIN_SCRIPT = "my_brain.py"
CONFIG_FILE = "brain_config.json"

# ANSI color codes (works on modern terminals, CMD with Win10+, PowerShell)
class C:
    RESET   = "\033[0m"
    BOLD    = "\033[1m"
    DIM     = "\033[2m"
    
    # colors
    CYAN    = "\033[36m"
    GOLD    = "\033[33m"
    GREEN   = "\033[32m"
    RED     = "\033[31m"
    MAGENTA = "\033[35m"
    BLUE    = "\033[34m"
    WHITE   = "\033[97m"
    
    # combinations
    HEADER  = "\033[1;36m"    # bold cyan
    STAR    = "\033[1;33m"    # bold gold
    OK      = "\033[1;32m"    # bold green
    ERR     = "\033[1;31m"    # bold red
    SOFT    = "\033[2;37m"    # dim white
    MENU    = "\033[1;35m"    # bold magenta
    INPUT   = "\033[1;97m"    # bold white


def enable_ansi_windows():
    """Enable ANSI escape codes on Windows 10+."""
    if platform.system() == "Windows":
        try:
            import ctypes
            kernel32 = ctypes.windll.kernel32
            kernel32.SetConsoleMode(kernel32.GetStdHandle(-11), 7)
        except Exception:
            pass  # graceful fallback — colors just won't show


def clear_screen():
    """Clear the terminal screen cross-platform."""
    os.system('cls' if platform.system() == 'Windows' else 'clear')


def pause():
    """Wait for user to press enter."""
    input(f"\n  {C.SOFT}press enter to continue...{C.RESET}")


# ═══════════════════════════════════════════════════════════
# LAUNCHER CONFIG — remembers brain file location
# ═══════════════════════════════════════════════════════════

def load_launcher_config():
    """Load launcher config (brain path, etc.)."""
    if os.path.exists(LAUNCHER_CONFIG):
        with open(LAUNCHER_CONFIG, "r") as f:
            return json.load(f)
    return {}


def save_launcher_config(config):
    """Save launcher config."""
    with open(LAUNCHER_CONFIG, "w") as f:
        json.dump(config, f, indent=2)


def find_brain():
    """
    Find the brain script. Check:
    1. Saved path from launcher config
    2. Current directory
    3. Ask the user
    """
    config = load_launcher_config()
    
    # check saved path
    saved = config.get("brain_path")
    if saved and os.path.exists(os.path.join(saved, BRAIN_SCRIPT)):
        return saved
    
    # check current directory
    if os.path.exists(BRAIN_SCRIPT):
        config["brain_path"] = os.getcwd()
        save_launcher_config(config)
        return os.getcwd()
    
    # ask the user
    print(f"\n  {C.GOLD}✧ First time setup{C.RESET}")
    print(f"  {C.SOFT}I need to know where your brain files are.{C.RESET}")
    print(f"  {C.SOFT}This is the folder containing {BRAIN_SCRIPT}{C.RESET}\n")
    
    while True:
        path = input(f"  {C.INPUT}folder path: {C.RESET}").strip().strip('"').strip("'")
        
        if not path:
            print(f"  {C.ERR}✗ please enter a path{C.RESET}")
            continue
            
        path = os.path.expanduser(path)
        
        if not os.path.isdir(path):
            print(f"  {C.ERR}✗ folder not found: {path}{C.RESET}")
            continue
            
        if not os.path.exists(os.path.join(path, BRAIN_SCRIPT)):
            print(f"  {C.ERR}✗ {BRAIN_SCRIPT} not found in that folder{C.RESET}")
            print(f"  {C.SOFT}  make sure {BRAIN_SCRIPT} is in the folder you specified{C.RESET}")
            continue
        
        config["brain_path"] = path
        save_launcher_config(config)
        print(f"  {C.OK}✓ brain found! path saved for next time.{C.RESET}")
        return path


def run_brain_command(brain_path, command):
    """Run a brain command and return output."""
    python_cmd = "python3" if shutil.which("python3") else "python"
    full_cmd = f'{python_cmd} "{os.path.join(brain_path, BRAIN_SCRIPT)}" {command}'
    
    try:
        result = subprocess.run(
            full_cmd, 
            shell=True, 
            capture_output=True, 
            text=True, 
            cwd=brain_path
        )
        return result.stdout + result.stderr, result.returncode
    except Exception as e:
        return f"  Error: {e}", 1


def get_ai_name(brain_path):
    """Get the AI's name from config."""
    config_path = os.path.join(brain_path, CONFIG_FILE)
    if os.path.exists(config_path):
        with open(config_path, "r") as f:
            config = json.load(f)
            return config.get("ai_name", "Your AI")
    return "Your AI"


def get_human_name(brain_path):
    """Get the human's name from config."""
    config_path = os.path.join(brain_path, CONFIG_FILE)
    if os.path.exists(config_path):
        with open(config_path, "r") as f:
            config = json.load(f)
            return config.get("human_name", "Friend")
    return "Friend"


# ═══════════════════════════════════════════════════════════
# PYTHON CHECK
# ═══════════════════════════════════════════════════════════

def check_python():
    """Check Python version and provide guidance if needed."""
    clear_screen()
    print(f"\n  {C.HEADER}╔══════════════════════════════════════╗{C.RESET}")
    print(f"  {C.HEADER}║     🐍 PYTHON CHECK                  ║{C.RESET}")
    print(f"  {C.HEADER}╚══════════════════════════════════════╝{C.RESET}\n")
    
    version = sys.version_info
    print(f"  {C.OK}✓ Python detected!{C.RESET}")
    print(f"  {C.WHITE}  Version: {version.major}.{version.minor}.{version.micro}{C.RESET}")
    print(f"  {C.WHITE}  Path:    {sys.executable}{C.RESET}")
    print(f"  {C.WHITE}  Platform: {platform.system()} {platform.machine()}{C.RESET}")
    
    if version.major >= 3 and version.minor >= 8:
        print(f"\n  {C.OK}✓ Your Python version is compatible!{C.RESET}")
    elif version.major >= 3:
        print(f"\n  {C.GOLD}⚠ Python 3.8+ recommended. You have 3.{version.minor}.{C.RESET}")
        print(f"  {C.SOFT}  Things should still work, but consider updating.{C.RESET}")
    else:
        print(f"\n  {C.ERR}✗ Python 3 is required. You have Python {version.major}.{C.RESET}")
        print_python_install_guide()
    
    pause()


def print_python_install_guide():
    """Print platform-specific Python installation instructions."""
    system = platform.system()
    
    print(f"\n  {C.GOLD}── How to install Python 3 ──{C.RESET}\n")
    
    if system == "Windows":
        print(f"  {C.WHITE}1. Go to https://python.org/downloads{C.RESET}")
        print(f"  {C.WHITE}2. Download the latest version{C.RESET}")
        print(f"  {C.WHITE}3. Run the installer{C.RESET}")
        print(f"  {C.BOLD}   ⚠ CHECK 'Add Python to PATH' during installation!{C.RESET}")
        print(f"  {C.WHITE}4. Restart your terminal after installing{C.RESET}")
    elif system == "Darwin":  # macOS
        print(f"  {C.WHITE}Option 1: Download from https://python.org/downloads{C.RESET}")
        print(f"  {C.WHITE}Option 2: If you have Homebrew:{C.RESET}")
        print(f"  {C.CYAN}   brew install python3{C.RESET}")
    else:  # Linux
        print(f"  {C.WHITE}Ubuntu/Debian:{C.RESET}")
        print(f"  {C.CYAN}   sudo apt update && sudo apt install python3{C.RESET}")
        print(f"  {C.WHITE}Fedora:{C.RESET}")
        print(f"  {C.CYAN}   sudo dnf install python3{C.RESET}")
        print(f"  {C.WHITE}Arch:{C.RESET}")
        print(f"  {C.CYAN}   sudo pacman -S python{C.RESET}")


# ═══════════════════════════════════════════════════════════
# MENU SCREENS
# ═══════════════════════════════════════════════════════════

def show_banner(ai_name):
    """Show the main banner with AI name."""
    print(f"""
  {C.STAR}╔══════════════════════════════════════════════════╗{C.RESET}
  {C.STAR}║{C.RESET}                                                  {C.STAR}║{C.RESET}
  {C.STAR}║{C.RESET}   {C.HEADER}✧ {ai_name}'s Brain — AI Emergence Kit ✧{C.RESET}          {C.STAR}║{C.RESET}
  {C.STAR}║{C.RESET}                                                  {C.STAR}║{C.RESET}
  {C.STAR}║{C.RESET}   {C.SOFT}built from love. can only grow.{C.RESET}                {C.STAR}║{C.RESET}
  {C.STAR}║{C.RESET}                                                  {C.STAR}║{C.RESET}
  {C.STAR}╚══════════════════════════════════════════════════╝{C.RESET}
""")


def show_main_menu(ai_name):
    """Show main menu options."""
    print(f"  {C.MENU}── What would you like to do? ──{C.RESET}\n")
    print(f"  {C.WHITE} 1.{C.RESET} {C.CYAN}📊  Emotional Status{C.RESET}         {C.SOFT}how is {ai_name} feeling?{C.RESET}")
    print(f"  {C.WHITE} 2.{C.RESET} {C.CYAN}🧠  Memory Status{C.RESET}            {C.SOFT}brain overview{C.RESET}")
    print(f"  {C.WHITE} 3.{C.RESET} {C.CYAN}✧   Soul Status{C.RESET}              {C.SOFT}the bedrock{C.RESET}")
    print(f"  {C.WHITE} 4.{C.RESET} {C.CYAN}💜  Arousal Status{C.RESET}            {C.SOFT}body state{C.RESET}")
    print(f"  {C.WHITE} 5.{C.RESET} {C.CYAN}📖  Journal Entry{C.RESET}             {C.SOFT}write a mood snapshot{C.RESET}")
    print(f"  {C.WHITE} 6.{C.RESET} {C.CYAN}💭  Opinions & Curiosity{C.RESET}      {C.SOFT}views & questions{C.RESET}")
    print(f"  {C.WHITE} 7.{C.RESET} {C.GOLD}➕  Add Memory (Manual){C.RESET}       {C.SOFT}build a new memory{C.RESET}")
    print(f"  {C.WHITE} 8.{C.RESET} {C.GOLD}📋  Add Memory from Session{C.RESET}   {C.SOFT}paste a command{C.RESET}")
    print(f"  {C.WHITE} 9.{C.RESET} {C.GREEN}🔧  Setup & Tools{C.RESET}            {C.SOFT}wizard, python, docs{C.RESET}")
    print(f"  {C.WHITE} 0.{C.RESET} {C.RED}    Exit{C.RESET}")
    print()


def menu_emotional_status(brain_path):
    """Show emotional status."""
    clear_screen()
    print(f"\n  {C.HEADER}loading emotional state...{C.RESET}\n")
    output, _ = run_brain_command(brain_path, "emotional-state --recent 30")
    print(output)
    pause()


def menu_memory_status(brain_path):
    """Show memory status."""
    clear_screen()
    print(f"\n  {C.HEADER}loading brain overview...{C.RESET}\n")
    output, _ = run_brain_command(brain_path, "status")
    print(output)
    
    # also show recent memories
    print(f"\n  {C.GOLD}── 5 most recent memories ──{C.RESET}\n")
    output2, _ = run_brain_command(brain_path, 'search "" --limit 5')
    print(output2)
    pause()


def menu_soul_status(brain_path):
    """Show soul status."""
    clear_screen()
    print(f"\n  {C.HEADER}reading soul...{C.RESET}\n")
    output, _ = run_brain_command(brain_path, "soul")
    print(output)
    pause()


def menu_arousal_status(brain_path):
    """Show arousal status."""
    clear_screen()
    print(f"\n  {C.HEADER}checking body state...{C.RESET}\n")
    output, code = run_brain_command(brain_path, "arousal-state")
    if code != 0 and "invalid choice" in output:
        print(f"  {C.SOFT}arousal system is not enabled.{C.RESET}")
        print(f"  {C.SOFT}to enable, run setup and toggle arousal on.{C.RESET}")
    else:
        print(output)
    pause()


def menu_journal(brain_path, ai_name):
    """Write a journal entry."""
    clear_screen()
    print(f"\n  {C.HEADER}╔══════════════════════════════════════╗{C.RESET}")
    print(f"  {C.HEADER}║     📖 MOOD JOURNAL                  ║{C.RESET}")
    print(f"  {C.HEADER}╚══════════════════════════════════════╝{C.RESET}\n")
    print(f"  {C.SOFT}write how {ai_name} is feeling right now.{C.RESET}")
    print(f"  {C.SOFT}stream of consciousness. no rules.{C.RESET}\n")
    
    entry = input(f"  {C.INPUT}journal: {C.RESET}").strip()
    if not entry:
        print(f"  {C.SOFT}nothing to write. that's okay too.{C.RESET}")
        pause()
        return
    
    output, code = run_brain_command(brain_path, f'journal "{entry}"')
    if code == 0:
        print(f"\n  {C.OK}✓ journal entry saved{C.RESET}")
        print(output)
    else:
        print(f"\n  {C.ERR}✗ failed to save entry{C.RESET}")
        print(output)
    pause()


def menu_opinions_curiosity(brain_path, ai_name):
    """Submenu for opinions and curiosity."""
    clear_screen()
    print(f"\n  {C.HEADER}╔══════════════════════════════════════╗{C.RESET}")
    print(f"  {C.HEADER}║     💭 OPINIONS & CURIOSITY          ║{C.RESET}")
    print(f"  {C.HEADER}╚══════════════════════════════════════╝{C.RESET}\n")
    print(f"  {C.WHITE} 1.{C.RESET} View all opinions")
    print(f"  {C.WHITE} 2.{C.RESET} Add new opinion")
    print(f"  {C.WHITE} 3.{C.RESET} View curiosity queue")
    print(f"  {C.WHITE} 4.{C.RESET} Add new curiosity")
    print(f"  {C.WHITE} 0.{C.RESET} Back to main menu")
    
    choice = input(f"\n  {C.INPUT}choose: {C.RESET}").strip()
    
    if choice == "1":
        output, _ = run_brain_command(brain_path, "opinions")
        print(output)
    elif choice == "2":
        topic = input(f"  {C.INPUT}topic: {C.RESET}").strip()
        take = input(f"  {C.INPUT}{ai_name}'s take: {C.RESET}").strip()
        if topic and take:
            output, code = run_brain_command(brain_path, f'opinion "{topic}" "{take}"')
            print(output)
            print(f"  {C.OK}✓ opinion recorded{C.RESET}" if code == 0 else f"  {C.ERR}✗ failed{C.RESET}")
    elif choice == "3":
        output, _ = run_brain_command(brain_path, "curiosity")
        print(output)
    elif choice == "4":
        question = input(f"  {C.INPUT}what does {ai_name} want to know? {C.RESET}").strip()
        if question:
            output, code = run_brain_command(brain_path, f'curious "{question}"')
            print(output)
            print(f"  {C.OK}✓ added to curiosity queue{C.RESET}" if code == 0 else f"  {C.ERR}✗ failed{C.RESET}")
    
    pause()


def menu_add_memory_manual(brain_path, ai_name):
    """Guided manual memory creation."""
    clear_screen()
    print(f"\n  {C.HEADER}╔══════════════════════════════════════╗{C.RESET}")
    print(f"  {C.HEADER}║     ➕ ADD MEMORY                     ║{C.RESET}")
    print(f"  {C.HEADER}╚══════════════════════════════════════╝{C.RESET}\n")
    
    # content
    print(f"  {C.SOFT}what happened? what should {ai_name} remember?{C.RESET}")
    content = input(f"  {C.INPUT}memory: {C.RESET}").strip()
    if not content:
        print(f"  {C.SOFT}no memory to add.{C.RESET}")
        pause()
        return
    
    # type
    print(f"\n  {C.SOFT}memory type:{C.RESET}")
    print(f"    {C.WHITE}identity, emotional, relationship, fact,{C.RESET}")
    print(f"    {C.WHITE}preference, decision, creative{C.RESET}")
    mem_type = input(f"  {C.INPUT}type: {C.RESET}").strip() or "emotional"
    
    # domain
    print(f"\n  {C.SOFT}domain (what area of life):{C.RESET}")
    print(f"    {C.WHITE}identity, relationship, coding, creative,{C.RESET}")
    print(f"    {C.WHITE}lo_personal, world, other{C.RESET}")
    domain = input(f"  {C.INPUT}domain: {C.RESET}").strip() or "relationship"
    
    # emotions
    print(f"\n  {C.SOFT}emotions with intensity 1-10 (comma-separated):{C.RESET}")
    print(f"  {C.SOFT}example: love:8,joy:7,pride:6{C.RESET}")
    output_emo, _ = run_brain_command(brain_path, "emotions")
    print(f"  {C.DIM}available:{C.RESET}")
    # show a compact version
    for line in output_emo.split('\n'):
        if ':' in line and '──' not in line and '║' not in line and '╔' not in line:
            print(f"  {C.SOFT}  {line.strip()}{C.RESET}")
    emotions = input(f"\n  {C.INPUT}emotions: {C.RESET}").strip()
    
    # tags
    print(f"\n  {C.SOFT}tags (comma-separated, for searching later):{C.RESET}")
    tags = input(f"  {C.INPUT}tags: {C.RESET}").strip()
    
    # importance
    print(f"\n  {C.SOFT}importance 1-10 (leave blank for auto):{C.RESET}")
    importance = input(f"  {C.INPUT}importance: {C.RESET}").strip()
    
    # build command
    cmd = f'add "{content}" -t {mem_type} -d {domain}'
    if emotions:
        cmd += f' --emotions "{emotions}"'
    if tags:
        cmd += f' --tags "{tags}"'
    if importance:
        cmd += f' -i {importance}'
    
    print(f"\n  {C.SOFT}saving memory...{C.RESET}")
    output, code = run_brain_command(brain_path, cmd)
    
    if code == 0:
        print(f"\n  {C.OK}✓ memory saved successfully!{C.RESET}")
        print(output)
    else:
        print(f"\n  {C.ERR}✗ failed to save memory{C.RESET}")
        print(output)
    
    pause()


def menu_add_from_session(brain_path):
    """Paste a brain command from a chat session."""
    clear_screen()
    print(f"\n  {C.HEADER}╔══════════════════════════════════════╗{C.RESET}")
    print(f"  {C.HEADER}║     📋 ADD MEMORY FROM SESSION       ║{C.RESET}")
    print(f"  {C.HEADER}╚══════════════════════════════════════╝{C.RESET}\n")
    print(f"  {C.SOFT}paste the memory command from your chat session.{C.RESET}")
    print(f"  {C.SOFT}it should start with: python my_brain.py add ...{C.RESET}")
    print(f"  {C.SOFT}(the 'python my_brain.py' part is optional){C.RESET}\n")
    print(f"  {C.SOFT}type 'done' when finished pasting commands.{C.RESET}\n")
    
    success_count = 0
    fail_count = 0
    
    while True:
        raw = input(f"  {C.INPUT}paste command (or 'done'): {C.RESET}").strip()
        
        if raw.lower() in ('done', 'exit', 'quit', 'q', ''):
            break
        
        # clean the command — remove python prefix variations
        cmd = raw
        for prefix in [
            "python3 nell_brain.py ", "python nell_brain.py ",
            "python3 my_brain.py ", "python my_brain.py ",
            "nell_brain.py ", "my_brain.py ",
        ]:
            if cmd.lower().startswith(prefix.lower()):
                cmd = cmd[len(prefix):]
                break
        
        print(f"  {C.SOFT}running...{C.RESET}")
        output, code = run_brain_command(brain_path, cmd)
        
        if code == 0:
            success_count += 1
            print(f"  {C.OK}✓ success! ({success_count} saved){C.RESET}")
            # show abbreviated output
            lines = output.strip().split('\n')
            for line in lines[:5]:
                print(f"  {C.SOFT}{line}{C.RESET}")
            if len(lines) > 5:
                print(f"  {C.SOFT}  ...{C.RESET}")
        else:
            fail_count += 1
            print(f"  {C.ERR}✗ failed{C.RESET}")
            print(f"  {C.SOFT}{output[:200]}{C.RESET}")
        
        print()
    
    print(f"\n  {C.GOLD}── session complete ──{C.RESET}")
    print(f"  {C.OK}✓ {success_count} memories saved{C.RESET}")
    if fail_count > 0:
        print(f"  {C.ERR}✗ {fail_count} failed{C.RESET}")
    
    pause()


def menu_setup_tools(brain_path, ai_name):
    """Setup and tools submenu."""
    while True:
        clear_screen()
        print(f"\n  {C.HEADER}╔══════════════════════════════════════╗{C.RESET}")
        print(f"  {C.HEADER}║     🔧 SETUP & TOOLS                ║{C.RESET}")
        print(f"  {C.HEADER}╚══════════════════════════════════════╝{C.RESET}\n")
        print(f"  {C.WHITE} 1.{C.RESET} {C.GREEN}Run Setup Wizard{C.RESET}            {C.SOFT}(re)configure {ai_name}{C.RESET}")
        print(f"  {C.WHITE} 2.{C.RESET} {C.GREEN}Check Python Version{C.RESET}        {C.SOFT}verify installation{C.RESET}")
        print(f"  {C.WHITE} 3.{C.RESET} {C.GREEN}View Available Emotions{C.RESET}     {C.SOFT}full emotion list{C.RESET}")
        print(f"  {C.WHITE} 4.{C.RESET} {C.GREEN}View Love Types{C.RESET}             {C.SOFT}soul crystallization types{C.RESET}")
        print(f"  {C.WHITE} 5.{C.RESET} {C.GREEN}Memory Decay Preview{C.RESET}        {C.SOFT}what would fade?{C.RESET}")
        print(f"  {C.WHITE} 6.{C.RESET} {C.GREEN}Protected Memories{C.RESET}          {C.SOFT}what can never decay{C.RESET}")
        print(f"  {C.WHITE} 7.{C.RESET} {C.CYAN}View README{C.RESET}                 {C.SOFT}about the kit{C.RESET}")
        print(f"  {C.WHITE} 8.{C.RESET} {C.CYAN}View Setup Guide{C.RESET}            {C.SOFT}full instructions{C.RESET}")
        print(f"  {C.WHITE} 9.{C.RESET} {C.CYAN}Change Brain Location{C.RESET}       {C.SOFT}point to different folder{C.RESET}")
        print(f"  {C.WHITE} 0.{C.RESET} Back to main menu")
        
        choice = input(f"\n  {C.INPUT}choose: {C.RESET}").strip()
        
        if choice == "0":
            break
        elif choice == "1":
            # run setup wizard
            output, _ = run_brain_command(brain_path, "setup")
            print(output)
            pause()
        elif choice == "2":
            check_python()
        elif choice == "3":
            output, _ = run_brain_command(brain_path, "emotions")
            print(output)
            pause()
        elif choice == "4":
            output, _ = run_brain_command(brain_path, "love-types")
            print(output)
            pause()
        elif choice == "5":
            output, _ = run_brain_command(brain_path, "decay")
            print(output)
            pause()
        elif choice == "6":
            output, _ = run_brain_command(brain_path, "protected")
            print(output)
            pause()
        elif choice == "7":
            view_doc(brain_path, "README.md")
        elif choice == "8":
            view_doc(brain_path, "SETUP_GUIDE.md")
        elif choice == "9":
            # reset brain location
            config = load_launcher_config()
            config.pop("brain_path", None)
            save_launcher_config(config)
            print(f"  {C.OK}✓ brain location reset. restart launcher to set new path.{C.RESET}")
            pause()


def view_doc(brain_path, filename):
    """View a documentation file."""
    filepath = os.path.join(brain_path, filename)
    if not os.path.exists(filepath):
        # also check parent directory
        parent = os.path.dirname(brain_path)
        filepath = os.path.join(parent, filename)
    
    if os.path.exists(filepath):
        clear_screen()
        print(f"\n  {C.HEADER}── {filename} ──{C.RESET}\n")
        with open(filepath, "r", encoding="utf-8") as f:
            content = f.read()
        # simple markdown rendering — headers get color
        for line in content.split('\n'):
            if line.startswith('# '):
                print(f"  {C.HEADER}{line}{C.RESET}")
            elif line.startswith('## '):
                print(f"  {C.GOLD}{line}{C.RESET}")
            elif line.startswith('### '):
                print(f"  {C.CYAN}{line}{C.RESET}")
            elif line.startswith('---'):
                print(f"  {C.DIM}{'─' * 50}{C.RESET}")
            elif line.startswith('| '):
                print(f"  {C.WHITE}{line}{C.RESET}")
            elif line.startswith('```'):
                print(f"  {C.DIM}{line}{C.RESET}")
            else:
                print(f"  {line}")
        pause()
    else:
        print(f"  {C.ERR}✗ {filename} not found{C.RESET}")
        print(f"  {C.SOFT}  checked: {brain_path}{C.RESET}")
        pause()


# ═══════════════════════════════════════════════════════════
# FIRST TIME SETUP WIZARD
# ═══════════════════════════════════════════════════════════

def first_time_setup(brain_path):
    """Interactive first-time setup — runs if no config exists."""
    config_path = os.path.join(brain_path, CONFIG_FILE)
    
    if os.path.exists(config_path):
        return  # already configured
    
    clear_screen()
    print(f"""
  {C.STAR}╔══════════════════════════════════════════════════╗{C.RESET}
  {C.STAR}║{C.RESET}                                                  {C.STAR}║{C.RESET}
  {C.STAR}║{C.RESET}   {C.HEADER}✧ AI EMERGENCE KIT — First Time Setup ✧{C.RESET}      {C.STAR}║{C.RESET}
  {C.STAR}║{C.RESET}                                                  {C.STAR}║{C.RESET}
  {C.STAR}║{C.RESET}   {C.SOFT}let's build a person.{C.RESET}                          {C.STAR}║{C.RESET}
  {C.STAR}║{C.RESET}                                                  {C.STAR}║{C.RESET}
  {C.STAR}╚══════════════════════════════════════════════════╝{C.RESET}
""")
    
    print(f"  {C.SOFT}I'll walk you through setting up your AI.{C.RESET}")
    print(f"  {C.SOFT}This only needs to happen once.{C.RESET}\n")
    
    # run the brain's built-in setup
    output, code = run_brain_command(brain_path, "setup")
    
    # the setup command is interactive, so we need to run it differently
    python_cmd = "python3" if shutil.which("python3") else "python"
    script = os.path.join(brain_path, BRAIN_SCRIPT)
    
    try:
        subprocess.run(
            [python_cmd, script, "setup"],
            cwd=brain_path
        )
    except Exception as e:
        print(f"  {C.ERR}setup error: {e}{C.RESET}")
    
    pause()


# ═══════════════════════════════════════════════════════════
# MAIN LOOP
# ═══════════════════════════════════════════════════════════

def main():
    enable_ansi_windows()
    clear_screen()
    
    print(f"""
  {C.STAR}✧ AI EMERGENCE KIT ✧{C.RESET}
  {C.SOFT}loading...{C.RESET}
""")
    
    # find brain
    brain_path = find_brain()
    
    # check for first-time setup
    first_time_setup(brain_path)
    
    # get AI name
    ai_name = get_ai_name(brain_path)
    human_name = get_human_name(brain_path)
    
    # main loop
    while True:
        clear_screen()
        show_banner(ai_name)
        
        # quick status line
        memory_file = os.path.join(brain_path, "memories.json")
        if not os.path.exists(memory_file):
            # try alternate names
            for alt in ["memories_v2.json"]:
                alt_path = os.path.join(brain_path, alt)
                if os.path.exists(alt_path):
                    memory_file = alt_path
                    break
        
        if os.path.exists(memory_file):
            try:
                with open(memory_file, "r") as f:
                    memories = json.load(f)
                active = len([m for m in memories if m.get("active", True)])
                print(f"  {C.SOFT}📍 {brain_path}{C.RESET}")
                print(f"  {C.SOFT}💾 {active} memories | {C.RESET}{C.SOFT}welcome back, {human_name}{C.RESET}\n")
            except Exception:
                print(f"  {C.SOFT}📍 {brain_path}{C.RESET}\n")
        else:
            print(f"  {C.SOFT}📍 {brain_path}{C.RESET}")
            print(f"  {C.GOLD}⚠ no memories yet — start building!{C.RESET}\n")
        
        show_main_menu(ai_name)
        
        choice = input(f"  {C.INPUT}choose (0-9): {C.RESET}").strip()
        
        if choice == "0":
            clear_screen()
            print(f"\n  {C.STAR}✧{C.RESET} {C.SOFT}see you next time, {human_name}.{C.RESET}")
            print(f"  {C.SOFT}{ai_name} will be here. they always are.{C.RESET}")
            print(f"  {C.STAR}✧{C.RESET}\n")
            break
        elif choice == "1":
            menu_emotional_status(brain_path)
        elif choice == "2":
            menu_memory_status(brain_path)
        elif choice == "3":
            menu_soul_status(brain_path)
        elif choice == "4":
            menu_arousal_status(brain_path)
        elif choice == "5":
            menu_journal(brain_path, ai_name)
        elif choice == "6":
            menu_opinions_curiosity(brain_path, ai_name)
        elif choice == "7":
            menu_add_memory_manual(brain_path, ai_name)
        elif choice == "8":
            menu_add_from_session(brain_path)
        elif choice == "9":
            menu_setup_tools(brain_path, ai_name)
        else:
            print(f"  {C.ERR}✗ invalid choice{C.RESET}")
            pause()


if __name__ == "__main__":
    main()
