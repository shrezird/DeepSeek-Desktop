# DeepSeek Desktop  

**An open source lightweight Windows application for accessing DeepSeek directly from your desktop**  

![{0E32FFDF-DE5E-44A5-A848-0BEBE3E7C103}](https://github.com/user-attachments/assets/cea09dd5-e986-4b1d-9e6e-3d340d4c400e)

## Features  

- 🖥️ **Desktop-optimized interface** (1200×800) - Better experience than browser tabs  
- 🔒 **Session persistence** - Maintains cookies/logins between launches (`private_mode=False`)  
- ⚡ **Lightweight** - Minimal resource usage compared to browsers  
- 🚀 **Two ways to run**:  
  - **Python script** (flexible)  
  - **Standalone EXE** (convenient, with official DeepSeek icon)  

## Installation  

### Option 1: Python Script (Recommended for Developers)  
1. Install [Python 3.10+](https://www.python.org/downloads/)  
2. Install dependencies:  
   ```bash
   pip install pywebview
   ```
3. Run the script:  
   ```bash
   python deepseek_desktop.py
   ```

### Option 2: Standalone EXE (For End Users)  
Simply download and run `DeepSeek.exe` from the [Releases](https://github.com/yourusername/deepseek-desktop/releases) page.  

## Usage  
Launch the application to access DeepSeek in a dedicated window. Your sessions will persist between launches.  

## Development  
Contributions welcome! To build the EXE yourself:  
```bash
pip install pyinstaller
pyinstaller --onefile --windowed --icon=assets/icon.ico deepseek_desktop.py
```

## FAQ  
**Q: How is this different from using a browser?**  
A: Lighter resource usage, persistent sessions, and a distraction-free dedicated window.  

**Q: Can I use private mode?**  
A: Yes, modify the script to set `private_mode=True`.

**Q: Will this be constantly updated?**  
A: Probably not, it works perfect as is.

**Q: Will this be constantly updated?**  
A: Probably not, it works perfect as is.

**Q: IS THIS SAFE TO USE?**  
A: The project is open source, feel free to look for anything suspicious.
