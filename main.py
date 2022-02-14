from hashlib import md5
from fpdf import FPDF
from numpy import array
from pandas import DataFrame, read_csv

# this class will deal with all formalities related to administration
class admin:
    #test modification for github
    #test Git with GitHub
    def __init__(self, username, password):

        # cars.csv will load as self.carData
        self.carData = read_csv("cars.csv")
        
        # customer.csv will load as self.customerData
        self.customerData = read_csv("customer.csv")
        
        # self.username self.password will authorize access to other details
        self.username = username
        self.password = password

    def customCheck(self):

        # This function will authorize the access
        # the password is hashed via md5
        # the hash for admin is '21232f297a57a5a743894a0e4a801fc3'
        hashing = lambda string: md5(string.encode()).hexdigest()
        return hashing(self.username) == hashing('admin') and hashing(self.password) == hashing('admin')

    def showCarsDetail(self):

        # This function will show the car details saved in cars.csv
        return self.carData

    def showCustomersDetails(self):

        # This function will show the customers details saved in customers.csv
        return self.customerData

    def get_customer_data(self, NIC):
        
        # This function will get the customer details saved in customers.csv
        # identified by unique NIC number
        
        try:
            
            # self.customerData is saved in df as a pandas Dataframe
            df = self.customerData
            # NIC will be set as the index to identify each entry
            df.set_index('NIC', inplace=True)
            # loc[NIC] is used to return the all data of the customer
            return df.loc[NIC]

        except KeyError:
            
            # if there is no customer with specified NIC then the result is invalid
            return '\nInvalid NIC number'

    def get_bill(self, NIC):

        try:
            # This funtion will show the Total Bill
            df = self.get_customer_data(NIC)
            return f"\n***********Total bill***********\n\nname: {df['name']}\nNIC: {NIC}\ncost per km: $ {df['fair']}\ndistance: {df['distance']} km\nvehicle: {df['vehicle']}\nfair: $ {df['fair']*df['distance']}"
        except:
            return '\nInvalid NIC number'

# this class will deal with all formalities related to booking of car
class booking:

    def __init__(self):
        
        # cars.csv will load as self.carData
        self.carData = read_csv("cars.csv")
        
        # customer.csv will load as self.customerData
        self.customerData = read_csv("customer.csv")

    def carDetailsBy(self):
        
        # The primary purpose of this function is to show all the details
        # according to desired format (filtered or sorted)
        
        decision = int(input('\nFor sorted details 0, for filtered details 1: '))
        
        if decision not in (0,1):
            print("\nInvalid option")
            return self.carDetailsBy()

        elif decision == 0:

            # user is required to enter desired service to be sorted and also the order
            service = int(input('\nEnter filter [type 0, company 2, cost 4]: '))
            
            if service not in (0,2,4):
                print("\nInvalid option")
                return self.carDetailsBy()

            ascending = eval(input('ascending (True or False) : '))

            # to avoid compuational complexitites Dataframe
            # is converted into 2D list and sorted in the sepecified manner
            # and reterned as a Dataframe
            lst = [list(i) for i in array(self.carData)]
            quickSort(lst, 0, len(lst)-1, service, ascending)
            return DataFrame(lst)
        
        # user is required to enter desired service to be filtered and also the value
        service = int(input('\nEnter filter [type 0, company 2, cost 4]: '))
        
        if service not in (0,2,4):
            print("\nInvalid option")
            return self.carDetailsBy()
        
        service_name = input('search here : ')

        # if service is cost then it should be an integer
        if service == 4:
            service_name = int(service_name)

        # to avoid compuational complexitites Dataframe
        # is converted into 2D list and sorted in the sepecified manner
        # and reterned as a Dataframe
        lst = [list(i) for i in array(self.carData)]
        quickSort(lst, 0, len(lst)-1, service)
        return DataFrame(binary_search(lst, service_name, service))

    def book(self):

        # This function will book the car for the user
        # user is required to enter asked data inorder to book a car
    
        name = input('\nEnter name: ')
        NIC = input('Enter NIC number: ')
        place = input('Enter the place: ')
        distance = input('Enter distance car will travel in km: ')
        vehicle = input('Enter vehicle: ')
        rent_span = input('How long do you want to rent it? :')
        time = input('Enter the renting Date and Time (yyyy, dd, mm, hr, mn): ').split(", ")
        check = input('\nDo you want to submit it (y/n): ')
        
        # if user continue to submit then
        # he/she will not be required to fill anything more
        # else the program will exit
        if check == 'y':
            print('\ncongratulations your booking is finished.')
        else: 
            return

        # self.carData is saved in dcar as a pandas Dataframe
        dcar = self.carData
        # model year will be set as the index to identify each entry
        dcar.set_index('model year', inplace=True)
        # loc['model year'] is used to return the cost and type of vehicle
        costPerKm = dcar.loc[vehicle]['cost']
        vehicleType = dcar.loc[vehicle]['type']
        
        # Every thing entered is saved into the last line of the csv file
        df = DataFrame({
            'NIC' : NIC,
            'name' : name,
            'place' : place,
            'fair' : costPerKm,
            'distance' : distance,
            'vehicle' : vehicle,
            'type' : vehicleType
        }, index = [-1])
        df.to_csv("customer.csv", index = False, mode = 'a', header = False)

        print('\nA copy of your Booking Details will be saved in the folder.')
        
        # Months Lists 
        month_= {
            1:'Jan',2:'Feb', 3:'Mar', 4:'Apr',
            5:'May', 6:'June', 7:'July', 8:'Aug',
            9:'Sep', 10:'Oct', 11:'Nov', 12:'Dec'
        }

        # peice of code below will create a pdf of invioce in the D:\2nd semester\DSA\project
        
        pdf = FPDF()
        pdf.add_page()
        pdf.set_left_margin(20)
        pdf.set_font("Arial", size = 15)

        pdf.cell(300, 12, txt = "Car Rental System", ln = 1, align = 'L')
        pdf.cell(200, 10, txt = "", ln = 2, align = 'C')
        pdf.set_font("Arial", size = 12)
        pdf.cell(200, 10, txt = "Booking Details", ln = 3, align = 'L')
        
        pdf.set_font("Arial", size = 10)
        pdf.cell(100, 8, txt = f"Name: {name}", ln = 4, align = 'L') 
        pdf.cell(100, 10, txt = f"NIC: {NIC}", ln = 5, align = 'L')
        pdf.cell(100, 10, txt = f"Car Booked: {vehicle}", ln = 6, align = 'L')
        pdf.cell(100, 10, txt = f"Place: {place}", ln = 7, align = 'L')
        pdf.cell(100, 10, txt = f"Pick-up Time: {month_[int(time[2])]} {time[1]}, {time[0]} | {time[3]}:{time[4]}:00", ln = 9, align = 'L')
        pdf.cell(100, 10, txt = f"Renting Span: {rent_span}", ln = 10, align = 'L')
        pdf.cell(100, 10, txt = f"Allowed Running: {distance} km", ln = 11, align = 'L')
        pdf.cell(100, 10, txt = f"Total Charge: {int(distance) * int(costPerKm)}", ln = 12, align = 'L')
        
        pdf.set_font("Arial", size = 6)
        pdf.cell(100, 10, txt = "Late delivery of car may result in additional charges.", ln = 13, align = 'L')

        pdf.output(f"D:/2nd semester/DSA/project/{NIC}_booking_details.pdf",'F')


# partition and quickSort will help to sort the 2D list in desired order
def partition(A, start, end, col, ascending):
    pivot, pindex = A[end][col], start
    if ascending:
        for i in range(start, end):
            if A[i][col] <= pivot:
                A[i], A[pindex] = A[pindex], A[i]
                pindex += 1
        A[end], A[pindex] = A[pindex], A[end]
    else:
        for i in range(start, end):
            if A[i][col] >= pivot:
                A[i], A[pindex] = A[pindex], A[i]
                pindex += 1
        A[end], A[pindex] = A[pindex], A[end]
    return pindex

def quickSort(A, start, end, col, ascending = True):
    if start >= end:
        return
    pIndex = partition(A, start, end, col, ascending)
    quickSort(A, start, pIndex - 1, col, ascending)
    quickSort(A, pIndex + 1, end, col, ascending)

# find is a modified binary search that will filter out the details
# it will return all the matches in a sorted list
def upper(lst, item, col): 
    low, high, ans = 0, len(lst) - 1, -1
    while low <= high: 
        guess = (low + high) // 2
        if lst[guess][col] <= item: 
            low = guess + 1 
        else: 
            ans = guess
            high = guess - 1
    return ans

def lower(lst, item, col):
    low, high, ans = 0, len(lst) - 1, -1
    while low <= high:
        guess = (low + high) // 2
        if lst[guess][col] >= item:
            high = guess - 1
        else:  
            ans = guess
            low = guess + 1
    return ans

def binary_search(lst, item, col):
    low, high = lower(lst, item, col), upper(lst, item, col)
    if high < 0:
        high = len(lst) - high - 1
    return [lst[i] for i in range(low+1,high)]

# all the sequential instruction will be executed in the main() function
def main():
    
    # user is required to specify to continue as admin or cusomer
    decision = int(input('\nEnter 0 for admin, 1 for customer: '))

    if decision == 0:
        
        # admin is required to enter username and password to be authorized
        username = input('\nEnter username here: ')
        password = input('Enter password here: ')
    
        # admin_ is an object that will do all the below functionalities
        admin_ = admin(username, password)

        # entered username and password will be checked
        # if passed then further proceeded else Invalid username and password
        if admin_.customCheck():

            while True:
                
                print("\nSelect the any of the following option:\n\n1. Cars Details\n2. Customers Details\n3. Specific Customer Detail (NIC required)\n4. Total Bill of Customer (NIC required)")
                
                # admin is required to chose option mentioned above
                choice = int(input('\nEnter here: '))

                if choice == 1:

                    # admin_ will show the deatails of cars
                    print(admin_.showCarsDetail())

                elif choice == 2:
                    # admin_ will show the deatails of customers
                    print(admin_.showCustomersDetails())
        
                elif choice == 3:

                    # admin is required to enter NIC of the customer
                    NIC = int(input('\nEnter NIC number here: '))
                    print()
                    # and get_customer_data will return the data of that customer
                    print(admin_.get_customer_data(NIC))
        
                elif choice == 4:

                    # admin is required to enter NIC of the customer for bill
                    NIC = int(input('\nEnter NIC number here: '))
                    # and get_bill will print the bill in console
                    print(admin_.get_bill(NIC))
        
                else:

                    # any of the invalid choice will return an error
                    print('\nInvalid Input')

                # admin wants to exit or not?
                if bool(input('\nDo you want to exit (y/n): ') == 'y') == 1:
                    break
    
        else:
            print('\nusername or password is incorrect')
    
    elif decision == 1:

        while True:
            # customer is required to enter his/her wish
            # in accordance to option given below
            choice = int(input('\nfor cars list 0, for booking 1: '))

            # customer is an object that will do all the below functionalities
            customer = booking()

            if choice == 0:

                # carDetailsBy is called to print the cars list
                print(customer.carDetailsBy())
                # if user is intrested in booking or not?
                decision = input('\nDo you want to book (y/n): ')
                choice = bool(decision == 'y')

            if choice == 1:

                # customer will book the car
                customer.book()
                # does customer want to book more or not?
                choice = input('\nDo you want to book more? (y/n): ')
                
                if choice == 'y':
                    
                    # customer will book more
                    continue
                
                else:
                    
                    # program will exit
                    print('\nThanks for visiting')
            
            elif choice == 0:
                decision = input('\nDo you want to go back (y/n): ')
                if decision == 'y':
                    continue
                print("\nThanks for visiting!")
                break
        
            elif choice != 0:
                print('\nInvalid Input')
                main()

    else:
        print('\nInvalid Input')
        main()

main()