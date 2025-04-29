import random
class GA:
    def __init__(self,T,k):
        self.target=T
        self.k=k
        self.max_gen=10
        self.gen=0
        self.found=False
        self.pos=None
        self.start()
    def start(self):
       while self.gen<=self.max_gen and self.found is False:
        
        self.population=[[random.randint(0,9)for j in range(self.k)]for i in range(20)]
       
        self.fitness=[self.score(self.population[i])for i in range(20)]
        self.difference=[self.diff(self.fitness[i])for i in range(20)]
        
        for i in range(len(self.difference)):
           if self.difference[i]==0:
              self.pos=i
              self.found=True
              break
           else:
             self.gen+=1
             self.max=self.maxdif(self.difference)
             self.secondmax=self.smax(self.max,self.difference)
             self.low=self.low_diff(self.difference)
             self.sloo=self.sl(self.low,self.difference)
             self.cross(self.population[self.low],self.population[self.sloo],self.k)
             break
       if self.found:
          print("combination found in after",self.gen,"iteration and that list is",self.population[self.pos])
       else:
          print("Not found in iteration")
       

    def score(self,population):
        sum=0
        for i in range(2):
            sum+=population[i]
        return sum
    def diff(self,fitvalue):
        dif=0
        dif=abs(fitvalue-self.target)
        return dif
    def maxdif(self,diff):
       max=0
       for i in range(len(diff)):
          if diff[i]>max:
             max=i
       return max
    
    def smax(self,maxindex,diff):
       sm=0
       for i in range(len(diff)):
          if i==maxindex:
             continue
          if diff[i]>sm:
             sm=i
       return sm
    def low_diff(self,diff):
       min=float('inf')
       for i in range(len(diff)):
          if diff[i]<min:
             min=i
       return min
    def sl(self,minindex,diff):
       sl=float('inf')
       for i in range(len(diff)):
          if i==minindex:
             continue
          if diff[i]<sl:
             sl=i
       return sl
    
    def cross(self,parent1,parent2,g):
     child1=parent1[:g//2]+parent2[g//2:]
     child2=parent2[:g//2]+parent1[g//2:]
     self.mututation(child1,child2,g)

    def mututation(self,ch1,ch2,g):
      for i in range(2):
        ch1[i]=random.randint(0,9)
        ch2[i]=random.randint(0,9)
      
      self.population[self.max]=ch1
      self.population[self.secondmax]=ch2

target=int(input("Enter the target value:"))
k=int(input("Enter the length:"))
ga=GA(target,k)
