import os
import shlex
import sys

if sys.version_info >= (3, 9):
  List  = list
else:
  from typing import List

from pathlib import Path
from setuptools import setup
from subprocess import check_output
from typing import Optional


__here__ = Path(__file__).absolute().parent


version_file_path = __here__ / "il2fb" / "commons" / "version.py"
exec(compile(version_file_path.read_text(), version_file_path, "exec"))


def maybe_get_shell_output(command: str) -> str:
  try:
    args = shlex.split(command)
    with open(os.devnull, "w") as devnull:
      return check_output(args, stderr=devnull).strip().decode()
  except Exception:
    pass


def maybe_get_current_branch_name() -> Optional[str]:
  return maybe_get_shell_output("git rev-parse --abbrev-ref HEAD")


def maybe_get_current_commit_hash() -> Optional[str]:
  return maybe_get_shell_output("git rev-parse --short HEAD")


def parse_requirements(file_path: Path) -> List[str]:
  requirements = list()

  if not file_path.exists():
    return requirements

  with file_path.open("rt") as f:
    for line in f:
      line = line.strip()

      # check if comment or empty
      if not line or line.startswith("#"):
        continue

      # check if is inclusion of other requirements file
      elif line.startswith("-r"):
        name = Path(line.split(" ", 1)[1])
        path = file_path.parent / name
        subrequirements = parse_requirements(path)
        requirements.extend(subrequirements)

      # assume standard requirement
      else:
        requirements.append(line)

  return requirements


README = (__here__ / "README.rst").read_text()

STABLE_BRANCH_NAME  = "master"
CURRENT_COMMIT_HASH = maybe_get_current_commit_hash()
CURRENT_BRANCH_NAME = maybe_get_current_branch_name()
IS_CURRENT_BRANCH_STABLE = (CURRENT_BRANCH_NAME == STABLE_BRANCH_NAME)
BUILD_TAG = (
  f".{CURRENT_BRANCH_NAME}.{CURRENT_COMMIT_HASH}"
  if not IS_CURRENT_BRANCH_STABLE and CURRENT_COMMIT_HASH
  else ""
)

REQUIREMENTS_DIR_PATH = __here__ / "requirements"

INSTALL_REQUIREMENTS = parse_requirements(REQUIREMENTS_DIR_PATH / "dist.txt")
SETUP_REQUIREMENTS   = parse_requirements(REQUIREMENTS_DIR_PATH / "setup.txt")
TEST_REQUIREMENTS    = parse_requirements(REQUIREMENTS_DIR_PATH / "test.txt")

setup(
  name="il2fb-commons",
  version=VERSION,
  description=(
    "Common helpers and data structures for projects related to "
    "«IL-2 Sturmovik: Forgotten Battles» flight simulator"
  ),
  long_description=README,
  long_description_content_type="text/x-rst",
  keywords=[
    "il2", "il-2", "fb", "forgotten battles", "commons", "commons",
    "structure", "structures",
  ],
  license="MIT",
  url=f"https://github.com/IL2HorusTeam/il2fb-commons/tree/v{VERSION}",

  author="Oleksandr Oblovatnyi",
  author_email="oblovatniy@gmail.com",

  packages=[
    "il2fb.commons",
  ],
  namespace_packages=[
    "il2fb",
  ],

  python_requires=">=3.8",
  install_requires=INSTALL_REQUIREMENTS,
  setup_requires=SETUP_REQUIREMENTS,
  tests_require=TEST_REQUIREMENTS,
  test_suite="tests",

  classifiers=[
    "Development Status :: 5 - Production/Stable",
    "Intended Audience :: Developers",
    "License :: OSI Approved :: MIT License",
    "Natural Language :: English",
    "Operating System :: MacOS :: MacOS X",
    "Operating System :: Microsoft :: Windows",
    "Operating System :: POSIX",
    "Programming Language :: Python :: 3",
    "Topic :: Software Development :: Libraries",
  ],

  options={
    'egg_info': {
      'tag_build': BUILD_TAG,
      'tag_date':  False,
    },
  },

  include_package_data=True,
  zip_safe=False,
)
