from setuptools import setup, find_packages
import os,site,sys


setup(name='pyreflect',
      version='0.1',
      description='A Reflection module for Java written in Python',
      url='https://github.com/cbonoz/cs230project',
      author='Pyreflect',
      author_email='chrisdistrict@gmail.com',
      license='MIT',
      packages=find_packages(),
      install_requires=["plyj"],
      use_2to3=True,
      zip_safe=False)

bash_file = os.path.expanduser("~/.bash_profile")


def create_alias():
    print("Creating Alias")
    try:
        # path = site.getsitepackages()[1]
        # version = str(sys.version_info.major) + "." + str(sys.version_info.minor)
        # pyr_path = path + "/pyreflect-0.1-py"+version+".egg/pyreflect/pyreflect.py"
        cdir = os.getcwd()
        for p in sys.path:
            if "pyreflect" in p and cdir not in p:
                print("aliasing: " + p)
                path = p
                break

        pyr_path = path + "/pyreflect/pyreflect.py"
        cmds = []
        # cmds.append("echo alias pyreflect=\\'\"python " + pyr_path + "\'\" >> " + bash_file)
        cmds.append("echo alias pyreflect=\\'python -m pyreflect.pyreflect\\' >> " + bash_file)
        cmds.append("source " + "~/.bash_profile")
        cmds.append("source " + bash_file)
        cmds.append("chmod +x " + pyr_path)
        for b in cmds:
            print(b)
            os.system(b)
        print("done")
    except Exception as e:
        print(e)
        print("Pyreflect installed in " + path)
        print("Will need to add to path")


# http://stackoverflow.com/questions/17460719/open-is-not-working-for-hidden-files-python
try:
    with open(bash_file, "r") as f:
        txt = f.read()
        if "pyreflect" not in txt:
            create_alias()
        else:
            print("Pyreflect already aliased")
       
        print("Invoke pyreflect with 'pyreflect' on the command line")
except Exception as e:
    print(e)
    pass



# # you may need setuptools instead of distutils

# setup(
#     # basic stuff here
#     scripts = [
#         'scripts/myscript.sh'
#     ]
# )