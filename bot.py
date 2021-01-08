import requests
from bot_config import NUMBER_OF_USERS, MAX_POSTS_PER_USER, MAX_LIKES_PER_USER, BASE_URL
from faker import Faker
from random import randrange, shuffle
from operator import itemgetter

fake = Faker()


def get_token(username, password):
    data = {"username": username,
            "password": password}

    r = requests.post(f"{BASE_URL}token/", json=data)
    return r.json()['access']


def create_user():
    data = {"username": fake.profile()['username'],
            "email": fake.company_email(),
            "password": fake.password(),
            "from_bot": True}

    r = requests.post(f"{BASE_URL}users/", json=data)
    return r.json()['username'], data['password']


def create_user_posts(token):
    posts_id = []
    posts_number = randrange(MAX_POSTS_PER_USER)
    for _ in range(posts_number):
        data = {"title": fake.sentence(),
                "body": fake.text()}
        header = {"Authorization": f"Bearer {token}"}
        r = requests.post(f"{BASE_URL}posts/", json=data, headers=header)
        posts_id.append(r.json()['pk'])

    return posts_id


def get_users_by_ids(ids):
    result = []
    for id in ids:
        r = requests.get(f"{BASE_URL}users/{id}/")
        result.append(r.json())
    return result


def get_users_with_zero_liked_post():
    users_id = set()
    r = requests.get(f"{BASE_URL}posts/")
    for post in r.json():
        if len(post['liked_by']) == 0:
            users_id.add(post['owner'])

    users = get_users_by_ids(users_id)
    return users


def get_posts_id_to_like(current_user, users_with_zero_liked_post):
    result = []
    for user in users_with_zero_liked_post:
        # Skipp to avoid self posts like
        if user['username'] == current_user:
            continue
        result.extend(user['posts'])
    shuffle(result)
    return result


def perform_likes(user, posts_id):
    token = get_token(user['username'], user['password'])
    current_likes = 0
    for id in posts_id:
        if current_likes >= MAX_LIKES_PER_USER:
            return  # Finnish if limit riched

        header = {"Authorization": f"Bearer {token}"}
        requests.get(f"{BASE_URL}posts/{id}/like/", headers=header)

        current_likes += 1


users_with_posts = []

for _ in range(0, NUMBER_OF_USERS):
    username, password = create_user()
    token = get_token(username, password)
    created_posts = create_user_posts(token)
    users_with_posts.append({"username": username,
                             "password": password,
                             "created_posts": created_posts,
                             "number_of_posts": len(created_posts)})


users_sorted_by_posts_number = sorted(users_with_posts,
                                      key=itemgetter('number_of_posts'))


for user in users_sorted_by_posts_number:
    users_with_zero_liked_post = get_users_with_zero_liked_post()
    posts_to_like = get_posts_id_to_like(
        user['username'], users_with_zero_liked_post)

    if len(posts_to_like):
        perform_likes(user, posts_to_like)
