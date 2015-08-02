from enterprise import UIUCEnterpriseWebBot
import getpass
import time
import keyring
from keyring.backends.OS_X import Keyring


KEYCHAIN_SERVICE_NAME = "com.Hopsy.UIUCWebby"


def notify(bot, query):
    bot.add_course(query['crn'])


def get_password(username, service_name):
    keyring.set_keyring(Keyring())
    password = keyring.get_password(service_name, username)
    return password


def main():

    username = raw_input("Username: ")
    password = getpass.getpass()

    while getpass.getpass("Reenter password: ") != password:
        print "Password does not match. Try again."
        password = getpass.getpass()

    term = raw_input("Term (format: 1yyyym, example: 120158 for Fall, 2015): ")
    queries = list()

    print "Type in your major, course and crn to monitor the class."
    print "Type 'X' to indicate that your are done at any point."

    while 1:
        major = raw_input("Major (example ECE): ")

        if major == "X":
            break

        course = raw_input("Course (example 391): ")

        if course == "X":
            break

        crn = raw_input("CRN (example 54321): ")

        if crn == "X":
            break

        queries.append({"major": major, "course": course, "crn": crn})

    print "Starting..."

    ss = UIUCEnterpriseWebBot()
    ss.term = term
    ss.login(username=username, password=password)

    completed = list()

    while len(completed) != len(queries):

        # sleep for 30 seconds so that we don't bog down the UIUC enterprise
        # server. Please do not remove this line or reduce the time.
        time.sleep(30)

        for query in queries:
            classes = \
                ss.get_classes(major=query['major'], course=query['course'])

            print query['crn'] + ": " + str(classes[query['crn']])

            if classes[query['crn']]:
                notify(ss, query)
                completed.append(query)

    print "Done!"


if __name__ == "__main__":
    print(get_password('rsnair2', KEYCHAIN_SERVICE_NAME))