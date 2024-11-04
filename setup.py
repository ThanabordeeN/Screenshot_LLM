from cx_Freeze import setup, Executable

setup(
    name="Screenshot_LLM",
    version="1.0.1",
    description="Screenshot_LLM",
    options={
        'build_exe': {
            'include_files': ['icon.ico'],  # Include the icon file
        }
    },
    executables=[Executable("main.py", 
                            base="Win32GUI", 
                            icon="icon.ico", 
                            target_name="Screenshot_LLM.exe" ,
                            shortcut_name="Screenshot_LLM")],
)
