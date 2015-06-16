#def fact(n: Integer) -> Integer:
#  if n <= 1:
#      return 1
#  else:
#    result = 1
#    for i in range(1, n):
#        result = result * i
#        0
#    return result

#def is_male_name(name: String) -> Bool:
#    return ends_with(name, 'ss')

#def is_female_name(name: String) -> Bool:
#    return ends_with(name, 'tta')

#def chance(known_male: Integer, known_female: Integer, names: [String]) -> Integer: # Float:
#  male_names_count = count(names, is_male_name)
#  female_names_count = count(names, is_female_name)
#  unknown_male = male_names_count - known_male
#  unknown_female = female_names_count - known_female
#  return unknown_female
  #male_chance = 1.0 / to_float(fact(unknown_male))
  #female_chance = 1.0 / to_float(fact(unknown_female))
  #return male_chance * female_chance

#z = split_w(read("2")) # not list_string
z = map(lambda e: to_int(e), ["e"])
print(str(z))
#known = map(to_int, split_w(read("\n")))
#known_male = known[0]
#known_female = known[1]
#names = split_w(read("\n"))
#z = chance(known_male, known_female, names) 
#print(add(str(to_int(z * 100.0)), '%'))
