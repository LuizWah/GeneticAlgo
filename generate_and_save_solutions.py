import Alg_genetico
import time

NUMBER_SOLUTIONS = 5
MAX_SATISFACTION = 212179.0
def make_solutions(NUMBER_SOLUTIONS):

    for i in range(NUMBER_SOLUTIONS):
        start = time.time()
        
        name_sol_file = "1hsolution" + str(i)

        solution = Alg_genetico.main()

        f = open("solution.txt", "a")
            
        f.write(f"{name_sol_file}\n\nVec A: {solution.xA}\n")
        f.write(f"Vec B: {solution.xB}\n")
        f.write(f"Ambus A: {solution.non_zeros_A}\n")
        f.write(f"Ambus B: {solution.non_zeros_B}\n")


        f.write(f"Rank: {solution.rank} / {MAX_SATISFACTION}\n")
        f.write(f"Percentage of coverage: {solution.rank / MAX_SATISFACTION}\n")
        Alg_genetico.plot_sol(solution, name_sol_file)
        
        end = time.time()
        f.write(f"Time of execution: start: {start} end: {end}\n--------------------------------------------------------------\n\n\n\n\n\n")
        
        
        
make_solutions(NUMBER_SOLUTIONS)