from random import sample, random, seed
import math

#Bernoulli trial
def bernoulli(p):
    r = random()
    return r <= p

#sample from exponential distribution
def exp(lambda_):
    r = random()
    return -math.log(1-r)/lambda_

class Individual:
    def __init__(self, id_):
        self.id_ = id_
        #SIR
        self.state = 'S' 
        #infectious time left, in days 
        self.inf_t = None

    def infect(self, duration):
        self.state = 'I'
        self.inf_duration = duration

    #jump to the next day
    def next_day(self):
        if self.infected():
            #reduce the infectious period with one day
            self.inf_duration = self.inf_duration - 1
            #infectious time is over
            if self.inf_duration <= 0:
                self.inf_duration = None
                self.state = 'R'

    def infected(self):
        return self.state == 'I' 

    def susceptible(self):
        return self.state == 'S' 

def log_infection(ind, t):
    print("infect:"+"t="+str(t)+",id="+str(ind.id_)+",dur="+str(ind.inf_duration))

#seed the random number generator
#seed(1)

population = []
N=100
for i in range(N):
    population.append(Individual(i))

#contacts of individual i, 
#here (for now) we assume that we have 5 random contact per day
def contacts(i):
    #select everyone but yourself
    selection = [j for j in population if j.id_ != i.id_]
    #sample 5 individuals from the selection
    return sample(selection, 5)

#probability that a contact results in an infection
beta=0.2

#expected infectious duration, in days
exp_duration = 6

#random sample individuals to seed
for p in sample(population, 2):
    p.infect(exp(1.0/exp_duration))
    log_infection(p, 0)

#simulate for 100 days
days = 100
for t in range(1, days):
    for i in population:
        if i.infected():
            for c in contacts(i):
                if c.susceptible() and bernoulli(beta):
                    duration = exp(1.0/exp_duration) 
                    c.infect(duration)
                    log_infection(c, t)
        i.next_day()
