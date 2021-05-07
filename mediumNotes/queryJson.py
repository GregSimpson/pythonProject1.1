
import jmespath
persons = {
    "persons": [
        { "name": "erik", "age": 38 },
        { "name": "john", "age": 45 },
        { "name": "rob", "age": 14 }
    ]
}

print ( jmespath.search('persons[*].age', persons) )
# [38, 45, 14]


person2 = {
    "persons": [
        { "name": "erik", "age": 38, "other": "this" },
        { "name": "john", "age": 45, "other": "that" },
        { "name": "rob", "age": 14, "other": "other" }
    ]
}

print ( jmespath.search('persons[*].name', person2) )
print ( jmespath.search('persons[*].age', person2) )
print ( jmespath.search('persons[*].other', person2) )

