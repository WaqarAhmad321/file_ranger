# Installation & Running Instructions

## Prerequisites

### Linux

- Python 3.8+
- C++ compiler (g++ with C++17 support)
- CMake 3.15+
- pip (Python package manager)

### Windows

- Python 3.8+
- Visual Studio 2019+ or MinGW-w64
- CMake 3.15+
- pip (Python package manager)

---

## Installation Steps

### 1. Clone the Repository

```bash
git clone https://github.com/WaqarAhmad321/file_ranger.git
cd file_ranger
```

### 2. Build C++ Backend

#### Linux

```bash
cd bindings
mkdir -p build
cd build
cmake ..
make
cd ../..
```

#### Windows (Visual Studio)

```cmd
cd bindings
mkdir build
cd build
cmake ..
cmake --build . --config Release
cd ..\..
```

#### Windows (MinGW)

```cmd
cd bindings
mkdir build
cd build
cmake -G "MinGW Makefiles" ..
mingw32-make
cd ..\..
```

### 3. Install Python Dependencies

```bash
pip install -r requirements.txt
```

Or manually install:

```bash
pip install textual rich
```

---

## Running the Application

### Linux

```bash
python ui/app.py
```

Or make it executable:

```bash
chmod +x ui/app.py
./ui/app.py
```

### Windows

```cmd
python ui\app.py
```

---

## Keyboard Shortcuts

| Key                 | Action                           |
| ------------------- | -------------------------------- |
| `j` / `↓`           | Move down                        |
| `k` / `↑`           | Move up                          |
| `h` / `←`           | Go to parent directory / Go back |
| `l` / `→` / `Enter` | Enter directory                  |
| `L`                 | Go forward                       |
| `n`                 | Create new file                  |
| `N`                 | Create new directory             |
| `r`                 | Rename file/directory            |
| `d`                 | Delete file/directory            |
| `c`                 | Copy file/directory              |
| `p`                 | Paste copied item                |
| `q`                 | Quit application                 |

---

## Troubleshooting

### Import Error: No module named 'backend'

**Linux:**

```bash
export PYTHONPATH="${PYTHONPATH}:$(pwd)/bindings/build"
python ui/app.py
```

**Windows:**

```cmd
set PYTHONPATH=%PYTHONPATH%;%CD%\bindings\build
python ui\app.py
```

### CMake Not Found

Install CMake:

- **Linux**: `sudo apt install cmake` (Ubuntu/Debian) or `sudo dnf install cmake` (Fedora)
- **Windows**: Download from https://cmake.org/download/

### Compiler Errors

Ensure C++17 support:

- **Linux**: `g++ --version` (should be 7.0+)
- **Windows**: Use Visual Studio 2019+ or MinGW-w64

### Python Dependencies Missing

```bash
pip install --upgrade pip
pip install -r requirements.txt
```

---

## Project Structure

```
file_ranger/
├── backend/           # C++ backend code
│   ├── include/       # Header files
│   └── src/           # Implementation files
├── bindings/          # pybind11 bindings
│   └── build/         # Built backend module
├── ui/                # Python UI
│   └── app.py         # Main application
└── requirements.txt   # Python dependencies
```

---

## Notes

- The C++ backend must be built before running the Python UI
- Ensure `backend.so` (Linux) or `backend.pyd` (Windows) exists in `bindings/build/`
- Use a terminal with Unicode support for proper icon display
- Recommended: Use a Nerd Font for best visual experience

---
