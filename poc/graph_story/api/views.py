import os, json, platform, subprocess, secrets

from django.shortcuts import render
from django.http import HttpResponse
from django.contrib.auth.models import User, UserManager
from rest_framework.decorators import api_view

from .models import Token, Graph


def get_graph_paths(token_title, graph_name):
    default_data_dir = os.environ.get('GRAPH_STORY_DATA_DIR')
    if not default_data_dir:
        default_data_dir = 'C:\\AK\\Temp\\graph_story_data'
    graph_path = os.path.join(token_title, graph_name)
    return default_data_dir, graph_path

def delete_folder(folder, recursive=True, force=True):
    if 'windows' in platform.system().lower():
        os.system(f'rmdir /s /q {folder}')
    else:
        os.system(f'rm -rf {folder}')

def generate_new_token():
    return secrets.token_urlsafe(48)


@api_view(['PUT', 'POST', 'DELETE',])
def user(request, user_name):
    response = HttpResponse('Request not processed')
    
    request_body = json.loads(request.body.decode('utf-8', errors='ignore'))
    user_pass = request_body.get('pass')
    user_token = request_body.get('token')
    user_email = request_body.get('email')
    if not user_email:
        user_email = ''
    
    try:
        searched_user = User.objects.get(username=user_name)
    except User.DoesNotExist as e:
        searched_user = None
        response = HttpResponse('User Does Not Exist')
    if request.method == 'POST':
        new_user = User.objects.create(username=user_name, password=user_pass, email=user_email)
        new_token = generate_new_token()
        Token.objects.create(token=new_token, owner=new_user)
        response = HttpResponse(new_token)
    elif request.method == 'PUT':
        if searched_user:
            is_valid_token = Token.objects.filter(token=user_token, owner=searched_user).exists()
            if is_valid_token:
                if user_pass:
                    print(searched_user.password)
                    print(user_pass)
                    searched_user.password=user_pass
                    print(searched_user.password)
                if user_email:
                    print(searched_user.email)
                    print(user_email)
                    searched_user.email=user_email
                    print(searched_user.email)
                searched_user.save()
                response = HttpResponse('User Updated')
    elif request.method == 'DELETE':
        if searched_user:
            is_valid_token = Token.objects.filter(token=user_token, owner=searched_user).exists()
            if is_valid_token:
                searched_user.is_active = False
                searched_user.save()
        response = HttpResponse('isActive = False')
    return response


@api_view(['GET',])
def index(request):
    return HttpResponse('Hello API')


@api_view(['GET', 'PUT', 'POST', 'DELETE',])
def graph(request, graph_name):
    response = HttpResponse('Request not processed')
    cwd = os.getcwd()
    
    request_body = json.loads(request.body.decode('utf-8', errors='ignore'))
    branch_name = request_body.get('branch')
    commit_hash = request_body.get('commit')
    dot_content = request_body.get('dot')
    commit_message = request_body.get('message')
    token_provided = request_body.get('token')
    try:
        graph_token = Token.objects.get(token=token_provided)
        
        folder_root, graph_default_path = get_graph_paths(str(graph_token.id), graph_name)
        try:
            graph_to_work = Graph.objects.get(name=graph_name, token=graph_token.id)
            graph_path = graph_to_work.folder
        except Graph.DoesNotExist as e:
            graph_to_work = None
            graph_path = graph_default_path
        folder_full_path = os.path.join(folder_root, graph_path)
        dot_file_full_path = os.path.join(folder_full_path, 'graph.dot')
        
        if request.method == 'GET':
            if graph_to_work:
                content = {}
                os.chdir(folder_full_path)
                if branch_name:
                    os.system(f'git checkout {branch_name}')
                    if commit_hash:
                        os.system(f'git checkout {commit_hash}')
                    history = subprocess.check_output(['git', 'log', '--oneline']).decode('utf-8', errors='ignore')
                    content['history'] = history
                    with open(dot_file_full_path, 'r') as f:
                        content['dot'] = f.read()
                else:
                    # dump: HttpResponse(open('path/to/file', 'rb').read())
                    branches = subprocess.check_output(['git', 'branch']).decode('utf-8', errors='ignore')
                    content = branches
                response = HttpResponse(json.dumps(content))
            else:
                response = HttpResponse('Graph Not Found')
        
        elif request.method == 'POST':
            if not os.path.exists(folder_full_path):
                os.makedirs(folder_full_path)
            os.chdir(folder_full_path)
            if not graph_to_work:
                os.system('git init')
                Graph.objects.create(name=graph_name, description='', folder=graph_path, token=graph_token)
            if branch_name:
                checkout_exit_code = os.system(f'git checkout {branch_name}')
                if checkout_exit_code != 0:
                    os.system(f'git checkout -b {branch_name}')
            with open(dot_file_full_path, 'w') as f:
                f.write(dot_content)
            os.system('git stage *')
            os.system(f'git commit -m "{commit_message}"')
            response = HttpResponse('Graph Updated')
        
        elif request.method == 'PUT':
            merge_to = request_body.get('merge_to')
            os.chdir(folder_full_path)
            os.system(f'git checkout {branch_name}')
            os.system(f'git merge -s ours {merge_to}')
            os.system(f'git checkout {merge_to}')
            os.system(f'git merge {branch_name}')
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
                    branches = subprocess.check_output(['git', 'branch']).decode('utf-8', errors='ignore')
                    delete_msg = f'{branches}'
            else:
                delete_folder(folder_full_path)
                if graph_to_work:
                    graph_to_work.delete()
                delete_msg = 'Deleted graph'
            response = HttpResponse(delete_msg)
        
        else:
            response = HttpResponse('Unsupported Method')
    except Token.DoesNotExist as e:
        response = HttpResponse('Token Not Found')
    
    os.chdir(cwd)
    return response


