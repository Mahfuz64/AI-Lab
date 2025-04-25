import random
import math
class point_coordination:
    def __init__(self,x,y):
        self.x=x
        self.y=y
        self.cluster=None

class kmean:
     def __init__(self,p,c):
         self.point=p
         self.cluster=c
         self.start()
     def generate_data_file(self, points, centroids, filename="data.txt"):
           with open(filename, "w") as f:
            f.write("Generated Data for K-Means Clustering\n")
            f.write("======================================\n\n")
            f.write("Points (x, y):\n")
            for p in points:
                f.write(f"{p.x},{p.y}\n")
            f.write("\nInitial Centroids (x, y):\n")
            for c in centroids:
                f.write(f"{c.x},{c.y}\n")

     def start(self):
         GRID_SIZE = 10 

         point_c = [point_coordination(random.randint(0, GRID_SIZE - 1), random.randint(0, GRID_SIZE - 1))for i in range(self.point)]

         centriod = [point_coordination(random.randint(0, GRID_SIZE - 1), random.randint(0, GRID_SIZE - 1))
            for _ in range(self.cluster)]
         self.generate_data_file(point_c,centriod)
         while True:
             centriod_c=[point_coordination(centriod[i].x,centriod[i].y)for i in  range(self.cluster)]

             for i in range(self.point):
                 min_distance=float('inf')
                 for j in range(self.cluster):
                     dst=abs(point_c[i].x-centriod[j].x)+abs(point_c[i].y-centriod[j].y)
                     if dst<min_distance:
                         point_c[i].cluster=j
                         min_distance=dst
             for i in range(self.cluster):
                 x,y,f=0,0,0
                 for j in range(self.point):
                     if point_c[j].cluster==i:
                         x+=point_c[j].x
                         y+=point_c[j].y
                         f+=1
                 if f!=0:
                     centriod[i].x=x//f
                     centriod[i].y=y//f
             chk=0
             for i in range(self.cluster):
                 chk+=abs(centriod[i].x-centriod_c[i].x)+abs(centriod_c[i].y-centriod[i].y)
             if chk==0:
                 break
         grid=[[0 for i in range(10)]for j in range(10)]
        
         for c in centriod:
          grid [c.x][c.y] = 'c'


         for p in point_c:
          if grid[p.y][p.x] != 'c':
            grid[p.y][p.x] = 1
         print("0 Means No data,1 means data available and C means Centroid")
         for i in range(GRID_SIZE):
              for j in range(GRID_SIZE):
                  print(grid[i][j],end=" ")
              print()  


point=int(input("Enter the point:"))
cluster=int(input("Enter the cluster no:"))
k=kmean(point,cluster)
                     

                     
         
         
    
