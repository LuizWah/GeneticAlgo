import shape.POSSIBLE_LOCATIONS as POSSIBLE_LOCATIONS

dp = POSSIBLE_LOCATIONS.DISTRICTS_POINTS


keys = list(dp)

for i in range(len(dp)):
    dp[keys[i]][2] = float(dp[keys[i]][2])
    
f = open("POSSIBLE.py", "a")
    
for i in range( len(dp)):    
    s = f"'{i}' : {dp[keys[i]]},\n"
    f.write(s)
f.close()    