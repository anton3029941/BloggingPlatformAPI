import requests
import json

while True:
    action = input('Choose an action (create, get, update, delete, getall, exit): ').strip().lower()

    if action == 'exit':
        break

    elif action == 'create':
        title = input('Title: ')
        content = input('Content: ')
        category = input('Category (optional): ')
        tags = input('Tags (comma separated, optional): ')
        tags_list = [tag.strip() for tag in tags.split(',')] if tags else []

        data = {
            'title': title,
            'content': content,
            'category': category if category else None,
            'tags': tags_list
        }

        r = requests.post('http://localhost:5000/posts', json=data)
    
    elif action == 'get':
        post_id = input('Post ID: ')
        r = requests.get(f'http://localhost:5000/posts/{post_id}')
        if r.status_code == 404:
            print(f'Post with ID {post_id} not found.')
        else:
            print(json.dumps(r.json(), indent=4, ensure_ascii=False))

    elif action == 'search':
        term = input('Search term: ')
        r = requests.get(f'http://localhost:5000/posts?term={term}')
        print(json.dumps(r.json(), indent=4, ensure_ascii=False))
    
    elif action == 'update':
        post_id = input('Post ID: ')
        title = input('New Title: ')
        content = input('New Content: ')
        category = input('New Category (optional): ')
        tags = input('New Tags (comma separated, optional): ')
        tags_list = [tag.strip() for tag in tags.split(',')] if tags else []

        data = {
            'title': title,
            'content': content,
            'category': category if category else None,
            'tags': tags_list
        }

        r = requests.put(f'http://localhost:5000/posts/{post_id}', json=data)
        if r.status_code == 404:
            print(f'Post with ID {post_id} not found.')
    
    elif action == 'delete':
        post_id = input('Post ID: ')
        r = requests.delete(f'http://localhost:5000/posts/{post_id}')
    
    elif action == 'getall':
        r = requests.get('http://localhost:5000/posts')
        print(json.dumps(r.json(), indent=4, ensure_ascii=False))
