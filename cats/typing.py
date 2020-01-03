"""Typing test implementation"""

from utils import *
from ucb import main, interact, trace
from datetime import datetime


###########
# Phase 1 #
###########


def choose(paragraphs, select, k):
    """Return the Kth paragraph from PARAGRAPHS for which SELECT called on the
    paragraph returns true. If there are fewer than K such paragraphs, return
    the empty string.
    """
    # BEGIN PROBLEM 1
    return [k for k in paragraphs if select(k)][k] if k < len([k for k in paragraphs if select(k)]) else ('')
     # END PROBLEM 1


def about(topic):
    """Return a select function that returns whether a paragraph contains one
    of the words in TOPIC.

    >>> about_dogs = about(['dog', 'dogs', 'pup', 'puppy'])
    >>> choose(['Cute Dog!', 'That is a cat.', 'Nice pup!'], about_dogs, 0)
    'Cute Dog!'
    >>> choose(['Cute Dog!', 'That is a cat.', 'Nice pup.'], about_dogs, 1)
    'Nice pup.'
    """
    assert all([lower(x) == x for x in topic]), 'topics should be lowercase.'
    # BEGIN PROBLEM 2
    def about_helper(x):
        y=False
        for i in range(len(topic)):
            for n in split(lower(remove_punctuation(x))):
                if topic[i] in n and len(topic[i])==len(n):
                    y=True
        return y
    return about_helper
    # END PROBLEM 2


def accuracy(typed, reference):
    """Return the accuracy (percentage of words typed correctly) of TYPED
    when compared to the prefix of REFERENCE that was typed.

    >>> accuracy('Cute Dog!', 'Cute Dog.')
    50.0
    >>> accuracy('A Cute Dog!', 'Cute Dog.')
    0.0
    >>> accuracy('cute Dog.', 'Cute Dog.')
    50.0
    >>> accuracy('Cute Dog. I say!', 'Cute Dog.')
    50.0
    >>> accuracy('Cute', 'Cute Dog.')
    100.0
    >>> accuracy('', 'Cute Dog.')
    0.0
    """
    typed_words = split(typed)
    reference_words = split(reference)
    # BEGIN PROBLEM 3
    total=0
    for i in range(len(reference_words)):
        if i>=len(typed_words):
            if len(typed_words)==0:
                return 0.0
            return (total/len(typed_words))*100
        elif typed_words[i]==reference_words[i]:
            total+=1
    return (total/len(typed_words))*100
    
    # END PROBLEM 3


def wpm(typed, elapsed):
    """Return the words-per-minute (WPM) of the TYPED string."""
    assert elapsed > 0, 'Elapsed time must be positive'
    # BEGIN PROBLEM 4
    if len(typed)==0:
        return 0.0
    words = len(typed)/5
    return (words/elapsed)*60

    # END PROBLEM 4

def autocorrect(user_word, valid_words, diff_function, limit):
    """Returns the element of VALID_WORDS that has the smallest difference
    from USER_WORD. Instead returns USER_WORD if that difference is greater
    than or equal to LIMIT.
    """
    # BEGIN PROBLEM 5
    test = valid_words[0]
    final = False
    for word in valid_words:
        var = diff_function(user_word, word, limit)
        if user_word==word:
            return user_word
        if var <= limit:
            final =True
            if var < diff_function(user_word, test, limit):
                test = word
    if final:
        return test
    return user_word
        
    # END PROBLEM 5


def swap_diff(start, goal, limit):
    """A diff function for autocorrect that determines how many letters
    in START need to be substituted to create GOAL, then adds the difference in
    their lengths.
    """
    # BEGIN PROBLEM 6
    i = 0
    def helper(i,k):
        if k > limit:
            return limit + 1
        if i >= min(len(goal), len(start)):
            return k
        elif start[i] != goal[i]:
            k += 1
        return helper(i+1,k)
    k=0
    help= helper(i,k)
   
    if len(start)==len(goal):
        return help
    else:
        diff = abs(len(goal)-len(start))
        return diff + help
    
    
    #assert False, 'Remove this line'
    # END PROBLEM 6

def edit_diff(start, goal, limit):
    """A diff function that computes the edit distance from START to GOAL."""
    y=limit
    if len(start) == 0:
        return len(goal)
    elif len(goal)==0:
        return len(start)
  
    else:
        if start[0]==goal[0]:
            return edit_diff(start[1:], goal[1:], y)
        if y == 0:
            return 1
        add_diff = 1 + edit_diff(start, goal[1:], y-1)
        remove_diff = 1 + edit_diff(start[1:], goal, y-1)
        substitute_diff = 1 + edit_diff(start[1:], goal[1:], y-1)
        # BEGIN
        return min(add_diff, remove_diff, substitute_diff)
        # END
        


def final_diff(start, goal, limit):
    """A diff function. If you implement this function, it will be used."""
    assert False, 'Remove this line to use your final_diff function'




###########
# Phase 3 #
###########


def report_progress(typed, prompt, id, send):
    """Send a report of your id and progress so far to the multiplayer server."""
    # BEGIN PROBLEM 8
    correct_words = 0
    for i in range(len(typed)):
        if typed[i] == prompt[i]:
            correct_words += 1
        else:
            break
    send({'id': id, 'progress': correct_words/len(prompt)})
    return correct_words/len(prompt)
        # END PROBLEM 8
    


def fastest_words_report(word_times):
    """Return a text description of the fastest words typed by each player."""
    fastest = fastest_words(word_times)
    report = ''
    for i in range(len(fastest)):
        words = ','.join(fastest[i])
        report += 'Player {} typed these fastest: {}\n'.format(i + 1, words)
    return report


def fastest_words(word_times, margin=1e-5):
    """A list of which words each player typed fastest."""
    n_players = len(word_times)
    n_words = len(word_times[0]) - 1
    assert all(len(times) == n_words + 1 for times in word_times)
    assert margin > 0
    # BEGIN PROBLEM 9
    new_list = [[] for i in range(n_players)]
   
    for i in range(n_words):
        fastest_time = 60
        for x in range(n_players):
            time_diff = elapsed_time(word_times[x][i+1]) - elapsed_time(word_times[x][i])
            if time_diff < fastest_time:
                fastest_time = time_diff
        for y in range(n_players):
            time = elapsed_time(word_times[y][i+1]) - elapsed_time(word_times[y][i])
            if time - fastest_time <= margin:
                new_list[y].append(word(word_times[y][i+1]))
    return new_list
                
            
    
    
    
    
    #return word_times[0]
        
    # END PROBLEM 9


def word_time(word, elapsed_time):
    """A data abstrction for the elapsed time that a player finished a word."""
    return [word, elapsed_time]


def word(word_time):
    """An accessor function for the word of a word_time."""
    return word_time[0]


def elapsed_time(word_time):
    """An accessor function for the elapsed time of a word_time."""
    return word_time[1]


enable_multiplayer = True   # Change to True when you


##########################
# Command Line Interface #
##########################


def run_typing_test(topics):
    """Measure typing speed and accuracy on the command line."""
    paragraphs = lines_from_file('data/sample_paragraphs.txt')
    select = lambda p: True
    if topics:
        select = about(topics)
    i = 0
    while True:
        reference = choose(paragraphs, select, i)
        if not reference:
            print('No more paragraphs about', topics, 'are available.')
            return
        print('Type the following paragraph and then press enter/return.')
        print('If you only type part of it, you will be scored only on that part.\n')
        print(reference)
        print()

        start = datetime.now()
        typed = input()
        if not typed:
            print('Goodbye.')
            return
        print()

        elapsed = (datetime.now() - start).total_seconds()
        print("Nice work!")
        print('Words per minute:', wpm(typed, elapsed))
        print('Accuracy:        ', accuracy(typed, reference))

        print('\nPress enter/return for the next paragraph or type q to quit.')
        if input().strip() == 'q':
            return
        i += 1


@main
def run(*args):
    """Read in the command-line argument and calls corresponding functions."""
    import argparse
    parser = argparse.ArgumentParser(description="Typing Test")
    parser.add_argument('topic', help="Topic word", nargs='*')
    parser.add_argument('-t', help="Run typing test", action='store_true')

    args = parser.parse_args()
    if args.t:
        run_typing_test(args.topic)
