# Create a copy of a dictionary with the dict() function
thisdict = {
  "brand": "Ford",
  "model": "Mustang",
  "year": 1964
}
mydict = dict(thisdict)
print(mydict)

#using the loops to print the keys and values of a dictionary
print("\nUsing for loop to print keys and values of the dictionary:")
for key in thisdict:
    print(key, ":", thisdict[key])
    
    
    # A dictionary can contain dictionaries, this is called nested dictionaries. 
print("\nNested Dictionary Example:")
myfamily = {
    "child1": {
        "name": "Hamza",
        "year": 2004
    },
    "child2": {
        "name": "Amar",
        "year": 2017
    },
    "child3": {
        "name": "Hassan",
        "year": 2015
    }
    }
print(myfamily)

#Now using the for loop to print the nested dictionary
print("\nUsing for loop to print nested dictionary:")
for child, info in myfamily.items():
    print(child)
    for key, value in info.items():
        print(f"  {key}: {value}")
        
