import configparser
import os
import subprocess
from pathlib import Path

CONFIG_FNAME = ".report"
DEFAULT_REPORTS_SRC_DIRNAME = "reports_code"
DEFAULT_REPORTS_OUT_DIRNAME = "reports"


def get_git_repo_root():
    return (
        subprocess.Popen(
            ["git", "rev-parse", "--show-toplevel"], stdout=subprocess.PIPE
        )
        .communicate()[0]
        .rstrip()
        .decode("utf-8")
    )


def get_absolute_path(maybe_relative_path, parent_dir):
    dirpath = maybe_relative_path
    if os.path.isabs(dirpath):
        return dirpath
    return os.path.join(parent_dir, dirpath)


def read_config(config_dir):
    # for all of the cases, if path in the config is relative, turn it into absolute.
    config_path = Path.joinpath(config_dir, CONFIG_FNAME)
    config = configparser.ConfigParser()
    config.read(config_path)
    reports_src_dir = Path(config["DEFAULT"].get("REPORTS_SRC_DIR", None))
    if reports_src_dir:
        reports_src_dir = get_absolute_path(reports_src_dir, config_dir)
    reports_out_dir = Path(config["DEFAULT"].get("REPORTS_OUT_DIR", None))
    if reports_out_dir:
        reports_out_dir = get_absolute_path(reports_out_dir, config_dir)
    return Path(reports_src_dir), Path(reports_out_dir)


def get_src_out_dirs():
    # e.g. for home, append home etc.

    if Path.exists(Path(CONFIG_FNAME)):
        # First check if there is config in the current folder.
        reports_src_dir, reports_out_dir = read_config(Path("."))
    else:
        # If not and it's a git repo, go to root and look there.
        repo_root = get_git_repo_root()
        if repo_root and Path.exists(Path(repo_root).joinpath(Path(CONFIG_FNAME))):
            reports_src_dir, reports_out_dir = read_config(repo_root)
        else:
            # Check at home otherwise.
            homepath = Path.home()
            if Path.exists(Path.joinpath(homepath, CONFIG_FNAME)):
                reports_src_dir, reports_out_dir = read_config(homepath)

    # If none of the options above worked, use default values and create those in the current directory.
    if not reports_out_dir:
        reports_out_dir = Path(DEFAULT_REPORTS_OUT_DIRNAME)
    if not reports_src_dir:
        reports_src_dir = Path(DEFAULT_REPORTS_SRC_DIRNAME)

    # Create if directories do not exist.
    reports_src_dir.mkdir(parents=True, exist_ok=True)
    reports_out_dir.mkdir(parents=True, exist_ok=True)

    # return abs paths
    reports_src_dir = os.path.abspath(reports_src_dir)
    reports_out_dir = os.path.abspath(reports_out_dir)

    return reports_src_dir, reports_out_dir
