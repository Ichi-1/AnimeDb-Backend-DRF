import random
from django.core.exceptions import ValidationError


def validate_size_image(file_obj):
    mb_limit = 2
    if file_obj.size > mb_limit * 1024 * 1024:
        raise ValidationError(f'Size limit: {mb_limit} Mb')


def silly_username_generator():
    adjective = ["Tricky", "Lovely", "Chocolate", "Sloppy", "Firce", "Jolly", "Vengeful", "Outstanding", "Hungry", "Sleepy", "Blue", "Yellow", "Hidden", "Red", "Angry", "Charming", "Marvelous", "Amazing"]
    noun = ["Elephant", "Platypus", "Duck", "Chimpanzee", "Kangaroo", "Crocodile", "Camel", "Tiger", "Lion", "Bear", "Panda", "Cat", "Koala", "Lizard", "Bunny", "Dolphin", "Mamoth"]
    l1 = len(adjective)
    l2 = len(noun)

    random_adjective_number = random.randint(0, l1-1)
    random_noun_number = random.randint(0, l2-1)

    random_adjective = adjective[random_adjective_number]
    random_noun = noun[random_noun_number]

    return f"{random_adjective} {random_noun}"
