import os, json, platform

from django.shortcuts import render
from django.http import HttpResponse
from rest_framework.decorators import api_view

def get_graph_full_path(author_name, graph_name):
    default_data_dir = os.environ.get('GRAPH_STORY_DATA_DIR')
    if not default_data_dir:
        default_data_dir = 'C:\\AK\\Temp\\graph_story_data'
    return os.path.join(default_data_dir, author_name, graph_name)

def delete_folder(folder, recursive=True, force=True):
    if 'windows' in platform.system().lower():
        os.system(f'rmdir /s /q {folder}')
    else:
        os.system(f'rm -rf {folder}')

@api_view(['GET',])
def index(request):
    return HttpResponse('Hello API')

@api_view(['GET', 'POST', 'PUT', 'DELETE',])
def graph(request, graph_name):
    cwd = os.getcwd()
    request_body = json.loads(request.body.decode('utf-8', errors='ignore'))
    branch_name = request_body.get('branch')
    author_name = request_body.get('author')
    if not author_name:
        author_name = 'guest'
    folder_full_path = get_graph_full_path(author_name, graph_name)
    dot_file_full_path = os.path.join(folder_full_path, 'graph.dot')
    response = HttpResponse('Request not processed')
    
    if request.method == 'GET':
        content = ''
        os.chdir(folder_full_path)
        if branch_name:
            os.system(f'git checkout -b {branch_name}')
            with open(dot_file_full_path, 'r') as f:
                content = f.read()
        else:
            # HttpResponse(open('path/to/file', 'rb').read())
            content = 'dump'
        response = HttpResponse(content)
    
    elif request.method == 'PUT':
        dot_content = request_body.get('dot')
        commit_message = request_body.get('message')
        if not os.path.exists(folder_full_path):
            os.makedirs(folder_full_path)
            os.chdir(folder_full_path)
            os.system('git init')
        if branch_name:
            os.chdir(folder_full_path)
            os.system(f'git checkout -B {branch_name}')
        with open(dot_file_full_path, 'w') as f:
            f.write(dot_content)
        os.system('git stage *')
        os.system(f'git commit -m "{commit_message}"')
        response = HttpResponse('Graph Updated')
    
    elif request.method == 'POST':
        merge_to = request_body.get('merge_to')
        os.chdir(folder_full_path)
        os.system(f'git checkout -B {merge_to}')
        os.system(f'git merge -s theirs {branch_name}')
        return HttpResponse(f'Merged {branch_name} > {merge_to} in graph')
    
    elif request.method == 'DELETE':
        delete_msg = ''
        if branch_name:
            if branch_name == 'master':
                delete_msg = 'master branch is not supposed to be deleted'
            else:
                os.chdir(folder_full_path)
                os.system(f'git checkout master')
                os.system(f'git branch -d {branch_name}')
                delete_msg = f'Deleted {branch_name} branch'
        else:
            delete_folder(folder_full_path)
            delete_msg = 'Deleted graph'
        response = HttpResponse(delete_msg)
    
    else:
        response = HttpResponse('Unsupported Method')
    
    os.chdir(cwd)
    return response
