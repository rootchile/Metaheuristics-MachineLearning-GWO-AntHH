import os
package = "PyGithub"
try:
    from github import Github
except:
    os.system("pip install "+ package)

import base64
from github import Github
from github import InputGitTreeElement

def pushGithub(repo,resultadoPath,message):

    g = Github('TOKEN GITREPO')

    repo = g.get_user().get_repo(repo)
    file_list = [resultadoPath]
    #borramos el archivo primero
    try:
        contents = repo.get_contents(resultadoPath, ref="master")
        repo.delete_file(contents.path, "Eliminamos archivo", contents.sha, branch="master")
    except:
        delete=0

    file_names = [resultadoPath]
    commit_message = message

    master_ref = repo.get_git_ref('heads/master')
    master_sha = master_ref.object.sha
    base_tree = repo.get_git_tree(master_sha)
    element_list = list()
    for i, entry in enumerate(file_list):
        with open(entry) as input_file:
            data = input_file.read()
        #if entry.endswith('.png'):
        #    data = base64.b64encode(data)
        element = InputGitTreeElement(file_names[i], '100644', 'blob', data)
        element_list.append(element)
    tree = repo.create_git_tree(element_list, base_tree)
    parent = repo.get_git_commit(master_sha)
    commit = repo.create_git_commit(commit_message, tree, [parent])
    master_ref.edit(commit.sha)

    return True
