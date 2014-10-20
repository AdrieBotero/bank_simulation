"""
Created on Oct 5, 2014

@author: andreas
"""
from Teller import Teller
from EventItem import EventItem
from Queue import PriorityQueue

from random import randint


def main():
    total_service_time = 0
    clock = 0
    time_limit = 2000
    total_inter_arrival_time = 0
    max_queue_length = 0
    customer_count = 0
    maximum_customer_wait_time = 0
    total_customer_wait_time = 0

    # input number on tellers
    number_of_tellers = raw_input("Enter number of tellers ")

    queue_of_events = PriorityQueue()

    # place an arrival node onto the Event Queue
    #generate service time

    inter_arrival = randint(1, 5)
    total_inter_arrival_time += inter_arrival
    tmp_arrival = EventItem(inter_arrival + clock, randint(5, 11), -1)
    queue_of_events.put((tmp_arrival.time_of_day, tmp_arrival))
    total_service_time += tmp_arrival.service_time

    #generating tellers

    tellers = []
    first_snapshot = False
    second_snapshot = False
    third_snapshot = False

    for number in range(0, int(number_of_tellers)):
        tellers.append(Teller(number))

    while clock < time_limit:
        if not first_snapshot and clock > 500:
            print_snapshot(clock, queue_of_events, tellers)
            first_snapshot = True
        elif not second_snapshot and clock > 1000:
            print_snapshot(clock, queue_of_events, tellers)
            second_snapshot = True
        elif not third_snapshot and clock > 1500:
            print_snapshot(clock, queue_of_events, tellers)
            third_snapshot = True

        temp_event = queue_of_events.get()[1]  # remove first item of queue
        for teller in tellers:
            if teller.line_of_customers.empty():  # checking if queue of teller is empty
                teller.idle_time += (temp_event.time_of_day - clock)
        clock = temp_event.time_of_day  # updating clock to time of day
        if temp_event.type_of_event == -1:
            shortest_teller_line = tellers[0]
            for teller in tellers:
                if shortest_teller_line.line_of_customers.qsize() > teller.line_of_customers.qsize():
                    shortest_teller_line = teller
            # shortest_teller_line.line_of_customers.put(shortest_teller_line, teller) #check this statement
            shortest_teller_line.line_of_customers.put((temp_event.time_of_day, temp_event))

            if shortest_teller_line.line_of_customers.qsize() == 1:
                time_of_day = clock + temp_event.service_time
                departure = EventItem(time_of_day, temp_event.service_time,
                                      shortest_teller_line.number)  # placing event inside queue
                queue_of_events.put((departure.time_of_day, departure))

            #generating new arrival

            inter_arrival = randint(1, 5)
            total_inter_arrival_time += inter_arrival
            tmp_arrival = EventItem(inter_arrival + clock, randint(5, 11), -1)
            queue_of_events.put((tmp_arrival.time_of_day, tmp_arrival))
            total_service_time += tmp_arrival.service_time

            if shortest_teller_line.line_of_customers.qsize() > max_queue_length:
                max_queue_length = shortest_teller_line.line_of_customers.qsize()
                #next departure node
        else:
            # add 1 to the customer
            customer_count += 1

            # remove customer from the indicated queue
            teller = tellers[temp_event.type_of_event]
            customer = teller.line_of_customers.get()[1]
            # calculate the wait time for this customer as
            customer_wait_time = clock - (customer.time_of_day + customer.service_time)
            total_customer_wait_time += customer_wait_time
            if customer_wait_time > maximum_customer_wait_time:
                maximum_customer_wait_time = customer_wait_time

            if not teller.line_of_customers.empty():
                time_of_day = clock + queue_peek(teller.line_of_customers)[1].service_time
                departure = EventItem(time_of_day, temp_event.service_time, teller.number)  # placing event inside queue
                queue_of_events.put((departure.time_of_day, departure))
    customers_left_in_queue = 0
    for teller in tellers:
        customers_left_in_queue += teller.line_of_customers.qsize()
    print_snapshot(clock, queue_of_events, tellers)
    print_results(customer_count, total_inter_arrival_time, total_service_time, tellers, maximum_customer_wait_time,
                  max_queue_length, customers_left_in_queue, total_customer_wait_time)


def print_results(customer_count, total_inter_arrival_time, total_service_time, tellers, maximum_customer_wait_time,
                  max_queue_length, customer_left_in_queue, total_customer_wait_time):
    # The total number of customer processed
    print "The total number of customers processed: {0}".format(customer_count)
    # The average inter-arrival time (to verify your program)
    print "The average inter-arrival time: {0:.2f}".format((float(total_inter_arrival_time) / float(customer_count)))
    # The average service time
    print "Average service time: {0:.2f}".format((float(total_service_time) / float(customer_count)))
    # The average wait time per customer
    print "Average wait time per customer {0:.2f}".format((float(total_customer_wait_time) / customer_count))
    # Percent of idle time for each of the cashier
    print "Percentage idle time for each of the cashier:"
    for teller in range(0, len(tellers)):
        print"\tTeller {0}, {1:.2f}%".format(teller, float(tellers[teller].idle_time) / 2000. * 100.)
    # The maximum customer wait time
    print "Maximum Customer wait time: {0}".format(maximum_customer_wait_time)
    # The maximum queue length of any customer queue
    print "Maximum Queue Length of any Teller's queue : {0}".format(max_queue_length)
    # The total number of people left in the queue at the end of the simulation.
    print "Total number of people left in the queue at the end of the simulation {0}".format(customer_left_in_queue)


def print_snapshot(clock, queue_of_events, tellers):
    # print out the numbers of customers in each queue
    # print the number of items in the event queue
    # out put clock time
    print "State Simulation:"
    print "At time: {0}".format(clock)
    print "Items in the event Queue {0} ".format(queue_of_events.qsize())
    print "Number of Customers in each queue: "
    for teller in range(0, len(tellers)):
        print"\tTeller {0}, {1}".format(teller, tellers[teller].line_of_customers.qsize())
    print "\n"


def queue_peek(queue):
    count = 1
    first_item = None
    while count <= queue.qsize():
        if count == 1:
            first_item = queue.get()
            queue.put(first_item)
        else:
            queue.put(queue.get())
        count += 1
    return first_item


if __name__ == '__main__':
    main()