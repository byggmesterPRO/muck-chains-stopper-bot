#!/usr/bin/python3
# this bot was made by u/hananelroe on reddit
# import needed libraries
import thefuzz.fuzz as fuzz
import praw
import unicodedata
import time
import datetime
import random
import sys
import DA_SECRETS

# print the version
print(f"\u001b[31;1mpraw: v{str(praw.__version__)}\033[0m")

# every m*** to get checked with the comments
Muck_list = ["muck", "muck.", "muck!", "muck?", "mֳ¼ck", "mֳ¼ck.", "mֳ¼ck!", "mukc", "mֳ¼ck?", "m\*ck",
             "kcum", "׀¼uck", "much", "mcuk"]

# list of blocked users to skip checking them
Blocked_users = []         # to use you need to write the user name without the "u/"
Enable_Blocking = False    # make it True to enable blocking users

# bot information:
client_id      = DA_SECRETS.client_id
client_secret  = DA_SECRETS.client_secret
username       = DA_SECRETS.username
password       = DA_SECRETS.password
user_agent     = "u/hananelroe's and u/HoseanRC's comment chains breaker bot"

# details about the bot to send after every comment
content  = "\n______\n ^(I'm just a simple bot that wants to stop muck chains, [here is my github page](https://github.com/hananelroe/muck-chains-stopper-bot)\
, you can see my source code and submit my issues there)\n\n ^(I'm a collaboration between [Hananelroe](https://www.reddit.com/u/Hananelroe) and [HoseanRC]\
(https://www.reddit.com/u/HoseanRC))\n\n^([visit my website](https://www.reddit.com/r/Damnthatsinteresting/comments/ovp6t1/never_gonna_give_you_up_by_rick_astley_remastered))"

# comment to send for every comment it receives
shut     = "#**SHUT**"    # shut comment for m***
bad_bot  = "WHY?"         # WHY? comment for "bad bot"
good_bot = "thanks! :)"   # thanks comment for "good bot"

fixed_comment = ""        # fixing comments to get better muck results
temp_blocked  = []        # list of temporarily blocked users
block_time    = []        # list of the time users got blocked

mucks         = 0         # number of mucks counted

mucks_counter = 0
yesterday_Mucks = 0
mucks_count_content1 = "**you have summoned me to show you the state of this sub**\n\ntoday I have counted **"  # the Asterisks are for bolding the counters' numbers
mucks_count_content2 = "** mucks.\n\nyesterday I have counted **"
mucks_count_disclaimer = "^(I don't reply to all mucks, but I do count both mucks that are a part of a chain and mucks that aren't, and the count resets every day.) \n\n^(if you've noticed a problem or want to contribute to my code, [here is my GitHub page](https://github.com/hananelroe/muck-chains-stopper-bot))"
help_request = "\n\n ### **IMPORTANT: the bot was supposed to restart the mucks count every day, but my programmer didn't manage to implement it yet. if you have an idea how to program it, consider [contributing to the project](https://github.com/hananelroe/muck-chains-stopper-bot)**"


class Empty():  # Empty class for parent function
    def __init__(self):
        self.body = None  # a fake "body" attribute
    pass     # ignore being empty


def parent(child_comment):      # gets comment's parent (aka the comment it replyed to)
                                # and returns a fake empty comment if it didn't find one

    parent_comment = Empty()         # create empty object for the fake comment
    parent_comment.author = Empty()  # add empty object for name for the author of the fake comment
    parent_comment.author.name = ""  # add the fake comment's author name
    try:
        if str(type(child_comment.parent())) == "<class 'praw.models.reddit.comment.Comment'>":   # check if it's a comment
            parent_comment = child_comment.parent()    # if it did find the comment, it will
                                                       # save it, otherwise it will raise error
    finally:
        return parent_comment   # at the end returns the same output as comment.parent()
                                # but it will return empty comment instead of any error

def noglyph(s):  # removes any glyph from a character (ex. ý -> y, Ŕ -> R)
    return ''.join(c for c in unicodedata.normalize('NFD', s)
                   if unicodedata.category(c) != 'Mn')

while True:
    # creating an authorized reddit instance from the given data
    reddit = praw.Reddit(client_id=client_id,
                         client_secret=client_secret,
                         username=username,
                         password=password,
                         user_agent=user_agent)

    # selects the subreddit to read the comments from
    subreddit = reddit.subreddit(DA_SECRETS.subreddit_name)

    print("\033[92monline\u001b[0m")  # prints green online

    try:

        # reads the comments from the subreddit
        for comment in subreddit.stream.comments(skip_existing=True):

            if len(block_time) > 0:               # if there was a temporarily blocked user
                while time.time() > (60 * 5) + block_time[0]:        # if the oldest available time
                                                                     # passed 5 minutes
                    block_time.pop(0)                                # remove it from the list
                    temp_blocked.pop(0)                              # remove the oldest item from temp_blocked
                    if len(block_time) == 0:    # if there wasn't anymore temporarily blocked users,
                        break                     # break the loop

            fixed_comment = noglyph("".join(dict.fromkeys(comment.body.lower()))).replace(" ","").replace("\n","")

            #fixed_comment = noglyph(                # removes every glyph from the comment
            #    "".join(dict.fromkeys(              # removes every repeated characters
            #    comment.body.lower())))             # convert all the characters to lowercase
            #    ).replace(" ","").replace("\n","")  # deletes spaces and line feeds (enter)

            print("\u001b[35;1m" + comment.body      # prints the original comment, the fixed one,
                + "\u001b[34;1m\t" + fixed_comment   # and the fixed comment similarity to "muck"
                + " \u001b[0m" + str(                # in percentage
                fuzz.ratio(fixed_comment, "muck")) + "%")

            # checks if Enable_Blocking is True and if the comment author is in Blocked_users list
            if comment.author.name in Blocked_users and Enable_Blocking:
                print("u/\033[31;1m" + comment.author.name + "\033[92mBLOCKED\033[0m")  # showing that its blocked
                continue # skips comment check

            elif comment.author.name in temp_blocked:                   # check if the comment's author was blocked temporarily
                print("u/\033[36m" + comment.author.name + "\nblocked temporarily for " + str(time.time() - block_time[temp_blocked.index(comment.author.name)] - (block_time[temp_blocked.index(comment.author.name)] % 1) + 1) + " seconds\033[0m")
                continue                                                # skip comment check

            elif comment.author.name == username:                       # check if the comment was the bot's comment
                print("u/\033[92m" + comment.author.name + "\033[0m")
                continue                                                # skip comment check
            else:
                print("u/\033[36;1m" + comment.author.name + "\033[0m")

            if parent(comment).author.name == username and comment.body.lower() == "bad bot":         # check if the comment was a reply to the bot
                                                                                                      # and if the comment was "bad bot"
                print("\033[92mbad bot MATCH! replying...\033[0m\n")
                try:
                    comment.parent().parent().parent().parent()    # check if the comment had more than 4 parents
                except:
                    comment.reply(bad_bot + content)               # if yes than comment bad_bot ("WHY?") with content
                else:
                    comment.reply(bad_bot)                         # else than comment bad_bot without content
                continue
            elif parent(comment).author.name == username and comment.body.lower() == "good bot":      # check if the comment was a reply to the bot
                                                                                                      # and if the comment was "good bot"
                print("\033[92mgood bot MATCH! replying...\u001b[0m\n")
                try:
                    comment.parent().parent().parent().parent()    # check if the comment had more than 4 parents
                except:
                    comment.reply(good_bot + content)              # if yes than comment good_bot ("thanks :)") with content
                else:
                    comment.reply(good_bot)                        # else than comment good_bot without content
                continue
            else:
                for item in Muck_list:                                   # checks for every m*** in Muck_list and select it as item
                    if fuzz.ratio(fixed_comment, item) > 74 and fixed_comment[0] in "mk":
                                                                         # check is the similarity of fixed_comment and item
                                                                         # is more than 74% and starts with "m" or "k"
                        mucks_counter += 1  # adds 1 muck to today's count

                        if comment.body != parent(comment).body:
                            break
                        mucks += 1   # count a muck
                        if mucks >= (4 + random.randint(0,1)):
                            mucks = 0
                            print("\033[92mMATCH! replying...\u001b[0m\n")   # prints "MATCH! replying..." in green
                            try:
                                comment.parent().parent().parent().parent()  # check if the comment had more than 4 parents
                            except:
                                comment.reply(shut + content + help_request)                # if yes than comment shut ("SHUT") with content
                            else:
                                comment.reply(shut + help_request)                          # else than comment shut without content

                            finally:                                         # than at the end
                                temp_blocked.append(comment.author.name)     # add the user to the temporarily blocked list
                                block_time.append(time.time())               # add the time to block_time list
                        else:
                            print("\033[92mMATCH! But not enough mucks, " + str(mucks) + " counted\u001b[0m\n")
                        break

                if comment.body.lower() == "u/danidevchainbreaker":  # when someone mentions the bot
                    comment.reply(mucks_count_content1 + str(mucks_counter) + mucks_count_content2 + str(yesterday_Mucks) + "** mucks. it gets worse...\n\n" + mucks_count_disclaimer + help_request)
#   suspended due to the count reset bugs:
#                    if int(yesterday_Mucks) < int(mucks_counter):  # if today there were more mucks than yesterday:
#                        print("\033[96m someone mentioned me!\033[0m \033[93m and it gets worse...\033[0m")
#                        comment.reply(mucks_count_content1 + str(mucks_counter) + mucks_count_content2 + str(yesterday_Mucks) + "** mucks. it gets worse...\n\n" + mucks_count_disclaimer)
#
#                    else:
#                        print("\033[96m someone mentioned me!\033[0m \033[92m and it gets better!\033[0m")
#                        comment.reply(mucks_count_content1 + str(mucks_counter) + mucks_count_content2  + str(yesterday_Mucks) + "** mucks. we're getting better!\n\n" + mucks_count_disclaimer)
                continue

    except KeyboardInterrupt:  # Ctrl-C - stop
        print("\u001b[31;1mBye!\u001b[0m")
        break
    except Exception as error:  # Any exception
        print(f"\u001b[31;1mError in line {sys.exc_info()[-1].tb_lineno}: {error}")  # prints error line and the error itself
        print("Trying to restart...\u001b[0m")