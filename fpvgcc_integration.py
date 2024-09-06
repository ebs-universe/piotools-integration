import os
import subprocess
from SCons.Script import Import

Import("env")
print("Installing fpvgcc integration...")

try:
    import fpvgcc
except ImportError:
    env.Execute("$PYTHONEXE -m pip install fpvgcc")


def run_fpv_gcc_task(options, env):
    build_dir=env.subst("${BUILD_DIR}")
    program_name=env.subst("${PROGNAME}")
    platform_name=env.subst("${PIOPLATFORM}")
    mapfile = os.path.join(build_dir, f"{program_name}.{platform_name}.map") 
    cmd = f"fpvgcc {options} {mapfile}"    
    env.Execute(cmd)

# Task for --sar
def fpv_sar(source, target, env):
    run_fpv_gcc_task("--sar", env)

# Task for --sobj all
def fpv_sobj(source, target, env):
    run_fpv_gcc_task("--sobj all", env)

# Task for --ssym all
def fpv_ssym(source, target, env):
    run_fpv_gcc_task("--ssym all", env)

# Task for --ssec
def fpv_ssec(source, target, env):
    run_fpv_gcc_task("--ssec", env)

# Task for --uf
def fpv_uf(source, target, env):
    run_fpv_gcc_task("--uf", env)

# Task for --uregions
def fpv_uregions(source, target, env):
    run_fpv_gcc_task("--uregions", env)

# Task for --usections
def fpv_usections(source, target, env):
    run_fpv_gcc_task("--usections", env)


# Register the tasks
env.AddCustomTarget("fpv_sar", "buildprog", fpv_sar, title="Memory Footprint per Archive", description="Run fpv-gcc with --sar")
env.AddCustomTarget("fpv_sobj", "buildprog", fpv_sobj, title="Memory Footprint per Object File", description="Run fpv-gcc with --sobj all")
env.AddCustomTarget("fpv_ssym", "buildprog", fpv_ssym, title="Memory Footprint per Symbol", description="Run fpv-gcc with --sobj all")
env.AddCustomTarget("fpv_ssec", "buildprog", fpv_ssec, title="Memory Footprint per Object File, per Section", description="Run fpv-gcc with --ssec")
env.AddCustomTarget("fpv_uf", "buildprog", fpv_uf, title="Used Files", description="Run fpv-gcc with --uf")
env.AddCustomTarget("fpv_uregions", "buildprog", fpv_uregions, title="Used Regions", description="Run fpv-gcc with --uregions")
env.AddCustomTarget("fpv_usections", "buildprog", fpv_usections, title="Used Sections", description="Run fpv-gcc with --usections")
