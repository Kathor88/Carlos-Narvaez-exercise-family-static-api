"""
Update this file to implement the following already declared methods:
- add_member: Should add a member to the self._members list
- delete_member: Should delete a member from the self._members list
- get_member: Should return a member from the self._members list
"""

class FamilyStructure:
    def __init__(self, last_name):
        self.last_name = last_name
        self._next_id = 1
        self._members = []

        # Automatically add the 3 required members upon initialization
        self.add_member({
            "first_name": "John",
            "age": 33,
            "lucky_numbers": [7, 13, 22]
        })
        self.add_member({
            "first_name": "Jane",
            "age": 35,
            "lucky_numbers": [10, 14, 3]
        })
        self.add_member({
            "first_name": "Jimmy",
            "age": 5,
            "lucky_numbers": [1]
        })

    # Internal helper to create unique, incremental IDs
    def _generate_id(self):
        generated_id = self._next_id
        self._next_id += 1
        return generated_id

    def add_member(self, member):
        # Assign an ID if one isn't provided (important for manual POST vs. system init)
        if "id" not in member or member["id"] is None:
            member["id"] = self._generate_id()
        
        # Ensure the last name always matches the family name
        member["last_name"] = self.last_name
        self._members.append(member)
        # Returning the dict with the ID is crucial for the automated test to avoid KeyErrors
        return member 

    def delete_member(self, id):
        # Search the list for a matching ID and remove the dictionary
        for index, member in enumerate(self._members):
            if member["id"] == id:
                self._members.pop(index)
                return True # Indicates successful deletion
        return False

    def get_member(self, id):
        # Search the list and return the matching member object
        for member in self._members:
            if member["id"] == id:
                return member
        return None

    def get_all_members(self):
        # Return the complete list of family members
        return self._members
