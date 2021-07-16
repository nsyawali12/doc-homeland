print("hellow world")

import json

people_string = '''
{
  "people": [
    {
      "name": "John Smith",
      "phone": "615-555-7164",
      "emails": ["johnsmith@gmail.com","johnsmith@work-place.com"],
      "has_license": false
    },
    {
      "name": "Jane Doe",
      "phone": "560-555-5153",
      "emails": null,
      "has_lincese": true
    }
  ]
}
''' 

data = json.loads(people_string)

# print(data)
# print(type(data))
# print(data)

print(type(data['people']))

for person in data['people']:
  print(person['name'])

#dump for deleting
for person in data['people']:
  del person['phone']

## String phone has been deleted or dump
# indent for seeing with indentation result of the data
new_string = json.dumps(data, indent=2, sort_keys=True)
print(new_string)
