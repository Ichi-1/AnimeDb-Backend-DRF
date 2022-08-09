import itertools
import random



def silly_username_generator():
    adjective = ['Chocolate', 'Sloppy', 'Firce', 'Jolly', 'Vengeful', 'Outstanding', 'Hungry', 'Sleepy', 'Blue', 'Yellow', 'Hidden', 'Red', 'Angry']
    noun = ['Elephant', 'Platypus', 'Duck', 'Chimpanzee', 'Kangaroo', 'Crocodile', 'Camel', 'Tiger', 'Lion', 'Bear', 'Panda', 'Cat']
    l1 = len(adjective) 
    l2 = len(noun)

    random_adjective_number = random.randint(0, l1-1)
    random_noun_number = random.randint(0, l2-1)

    random_adjective = adjective[random_adjective_number]
    random_noun = noun[random_noun_number]
   
    return f'{random_adjective} {random_noun}'