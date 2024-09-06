import os
import subprocess
from SCons.Script import Import

Import("env")
print("Installing disassembly generation...")


def generate_file_disassembly(file_path, ext, env):
    objdump=env.subst("${OBJCOPY}").replace("objcopy","objdump")
    build_dir=env.subst("${BUILD_DIR}")

    asm_path = os.path.splitext(file_path)[0] + '.s'
    cmd = (f"{objdump} -drwG -S {file_path} > {asm_path}")
    subprocess.run(cmd, shell=True, check=True)
    print("Generated", os.path.relpath(asm_path, build_dir))
    

def find_lib_dirs(root_folder):
    lib_paths = []
    for top_level_dir in os.listdir(root_folder):
        top_level_path = os.path.join(root_folder, top_level_dir)
        if os.path.isdir(top_level_path) and top_level_dir.startswith("lib"):
            lib_paths.append(top_level_path)
    return lib_paths


def find_object_files_in_dir(root_folder):
    object_files = []    
    for dirpath, dirnames, filenames in os.walk(root_folder):
        for filename in filenames:
            if filename.endswith(".o"):
                object_files.append(os.path.join(dirpath, filename))
    return object_files


def find_object_files_in_lib_dirs(root_folder):
    lib_dirs = find_lib_dirs(root_folder)
    object_files = []
    for lib_dir in lib_dirs:
        object_files.extend(find_object_files_in_dir(lib_dir))
    return object_files


def generate_elf_disassembly(env):
    build_dir=env.subst("${BUILD_DIR}")
    program_name=env.subst("${PROGNAME}")
    generate_file_disassembly(os.path.join(build_dir, f"{program_name}.elf"), '.elf', env)
    

def generate_obj_disassemblies(env):
    build_dir=env.subst("${BUILD_DIR}")
    object_paths = find_object_files_in_dir(build_dir)
    for object_path in object_paths:
        generate_file_disassembly(object_path, '.o', env)


def generate_disassembly_during_build(source, target, env):
    generate_elf_disassembly(env)
    # generate_obj_disassemblies(env)


def generate_disassembly_from_task(source, target, env):
    generate_elf_disassembly(env)
    generate_obj_disassemblies(env)
    

env.AddPostAction("buildprog", generate_disassembly_during_build)
env.AddCustomTarget("generate_disassembly", "buildprog", generate_disassembly_from_task, "Disassemble All Build Artifacts")