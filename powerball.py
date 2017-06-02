from collections import Counter
import random

class Employee(object):
    def __init__(self, fname, lname, numbers, powerball):
        self._fname = fname
        self._lname = lname
        self._numbers = numbers
        self._powerball = powerball

    def fname(self):
        return self._fname

    def lname(self):
        return self._lname

    def numbers(self):
        return self._numbers

    def powerball(self):
        return self._powerball

class EmployeeBuilder(object):
    def __init__(self, num_min, num_max, pb_min, pb_max):
        self.num_min = num_min
        self.num_max = num_max
        self.pb_min = pb_min
        self.pb_max = pb_max

    def _validate_number(self, num, num_min, num_max, num_list):
        if "." in num:
            # Input is either a float or a garbage string
            raise Exception("Please enter a whole number.")
        try:
            num = int(num)
        except Exception as e:
            raise Exception("Please enter a whole number.")
        if num < num_min or num > num_max:
            raise Exception("Please enter a number between " + str(num_min) + " and " + str(num_max))
        if num in num_list:
            raise Exception("Please enter a unique number.")

    def buildEmployee(self):
        # Python 2
        # TODO: Should names be validated?
        fname = raw_input("Enter your first name: ")
        lname = raw_input("Enter your last name: ")

        select_verbiage = ["1st #", "2nd #", "3rd #", "4th #", "5th #"]

        numbers = []
        count = 0
        while count < 5:
            prompt = "select " + select_verbiage[count]
            range_with_exclusions = str(self.num_min) + " thru " + str(self.num_max)
            if len(numbers) > 0:
                range_with_exclusions += " excluding "
                if len(numbers) == 1:
                    range_with_exclusions += str(numbers[0])
                else:
                    range_with_exclusions += ", ".join(str(i) for i in numbers[0:-1])
                    range_with_exclusions += ", and " + str(numbers[-1])
            prompt += " (" + range_with_exclusions + "): "
            num = raw_input(prompt)
            try:
                self._validate_number(num, self.num_min, self.num_max, numbers)
                numbers.append(int(num))
                count += 1
            except Exception as e:
                print e

        pb = 0
        pb_valid = False
        pb_prompt = "select Power Ball # (" + str(self.pb_min) + " thru " + str(self.pb_max) + "): "
        while not pb_valid:
            pb = raw_input(pb_prompt)
            try:
                self._validate_number(pb, self.pb_min, self.pb_max, [])
                pb = int(pb)
                pb_valid = True
            except Exception as e:
                print e

        return Employee(fname, lname, numbers, pb)

def generateWinningNumbers(employee_list, num_min, num_max, pb_min, pb_max):
    num_list = []
    pb_list = []
    for e in employee_list:
        num_list += e.numbers()
        pb_list.append(e.powerball())

    # list of numbers ordered by the frequency of their occurrence
    ordered_num_frequencies = Counter(num_list).most_common()
    ordered_pb_frequencies = Counter(pb_list).most_common()

    winning_numbers = []
    for win_index in xrange(0, 5):
        # walk the ordered list starting at index 0
        # track the frequency of the first number
        # get a subset of all numbers with that same frequency, as long as frequency > 1
        # if more than zero numbers appears with the same frequency, randomly select a winning number from that subset,
        # and remove that number from the frequency list so it is not reconsidered 
        # if not, select a totally random number
        same_freq = []
        freq = ordered_num_frequencies[0][1]
        for i in xrange(0, len(ordered_num_frequencies)):
            if ordered_num_frequencies[i][1] > 1 and ordered_num_frequencies[i][1] == freq:
                same_freq.append(ordered_num_frequencies[i][0])
            else:
                break
        if len(same_freq) > 0:
            num = same_freq[random.randint(0, len(same_freq)-1)]
            winning_numbers.append(num)
            index = 0
            for i in xrange(0, len(ordered_num_frequencies)):
                if ordered_num_frequencies[i][0] == num:
                    index = i
                    break 
            del ordered_num_frequencies[index]
        else:
            random_winner = random.randint(num_min, num_max)
            # make sure we dont select the same random number twice
            # count up until it's unique
            # unless we hit num_max, then wrap around to num_min and keep counting
            while random_winner in winning_numbers:
                random_winner += 1
                if random_winner > num_max:
                    random_winner = num_min
            winning_numbers.append(random_winner)

    winning_numbers = sorted(winning_numbers)

    # pretty much the same as above
    # but we don't have to worry about changing the frequency list
    # because we're only selecting one number as the powerball number
    same_freq = []
    freq = ordered_pb_frequencies[0][1]
    for i in xrange(0, len(ordered_pb_frequencies)):
        if ordered_pb_frequencies[i][1] > 1 and ordered_pb_frequencies[i][1] == freq:
            same_freq.append(ordered_pb_frequencies[i][0])
        else:
            break
    if len(same_freq) > 0:
        winning_numbers.append(same_freq[random.randint(0, len(same_freq)-1)])
    else:
        winning_numbers.append(random.randint(pb_min, pb_max))

    return winning_numbers


num_min = 1
num_max = 69
pb_min = 1
pb_max = 26

employees = []
eb = EmployeeBuilder(num_min, num_max, pb_min, pb_max)

mainMenuText = ("#########################\n" +
                "#  POWERBALL MAIN MENU  #\n" +
                "#                       #\n" +
                "#  1 - Generate Ticket  #\n" +
                "#  2 - Winning Numbers  #\n" +
                "#  3 - Exit             #\n" +
                "#                       #\n" +
                "#########################")

menuSelection = ""
while menuSelection != "2":
    print "\n"
    print mainMenuText
    menuSelection = raw_input("Enter selection: ")
    if menuSelection == "1":
        employees.append(eb.buildEmployee())
    elif menuSelection == "2":
        if len(employees) < 1:
            print "Please enter at least one employee."
            menuSelection = ""
            continue
        print "\n"
        for e in employees:
            print e.fname(), e.lname(), " ".join(str(i) for i in e.numbers()), "Powerball:", e.powerball()
        winning_numbers = generateWinningNumbers(employees, num_min, num_max, pb_min, pb_max)
        print "\n"
        print "Powerball winning number:"
        print "\n"
        print " ".join(str(x) for x in winning_numbers[0:5]), "Powerball:", str(winning_numbers[5])
    elif menuSelection == "3":
        exit(0)
    else: 
        print "Invalid selection"
