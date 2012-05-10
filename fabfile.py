from fabric.api import local

def delete_all_files(format_to_delete = None):
    if format:
        local("rm %s"%format_to_delete)
        print("deleted {0} format files".format(format_to_delete))
    else:
        print("need file format like *.sh")

