from fabric.api import local

def delete_all_files(format_to_delete = None):
    if format:
        local("rm %s"%format_to_delete)
        print("deleted {0} format files".format(format_to_delete))
    else:
        print("need file format like *.sh")

def push_to_github(branch):
    local("git push -u origin '%s'"%branch)

def push_to_heroku(branch):
    local("git push heroku '%s'"%branch)

def logs():
    local("heroku logs")

def start_worker():
    local("heroku ps:scale worker=1")

def running():
    local("heroku ps")

